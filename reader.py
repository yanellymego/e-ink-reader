# Import libraries
from ebooklib import epub
from bs4 import BeautifulSoup
from display import W, H
from PIL import Image, ImageDraw, ImageOps

import io
import os
import display
import settings
import json

#
# Global Variables
#
PROGRESS_FILE = "progress.json"

#
# Helper Functions
#

# Progress functions
def load_progress():
    if not os.path.exists(PROGRESS_FILE):
        return {}

    try:
        with open(PROGRESS_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_progress(book_path, chapter, page):

    progress = load_progress()

    book_name = os.path.basename(book_path)

    progress[book_name] = {
        "chapter": chapter,
        "page": page
    }

    with open(PROGRESS_FILE, "w") as file:
        json.dump(progress, file, indent=4)


# EPUB Loading
def load_epub_sections(path):
    book = epub.read_epub(path)

    cover_bytes = extract_cover(book)
    print("COVER FOUND:", cover_bytes is not None)
    cover_image = build_cover_image(cover_bytes)

    chapters = []

    for item in book.get_items():
        if item.get_type() == 9:  # document (HTML content)
            print("SECTION:", item.get_name())
            soup = BeautifulSoup(item.get_content(), "html.parser")

            blocks = []

            # Extract meaningful structure
            for tag in soup.find_all(["h1", "h2", "h3", "p", "li"]):
                text = tag.get_text().strip()

                if not text:
                    continue

                if tag.name in ["h1", "h2", "h3"]:
                    blocks.append({
                        "type": "heading",
                        "text": text
                    })
                else:
                    blocks.append({
                        "type": "paragraph",
                        "text": text
                    })

            if blocks:
                chapters.append({
                    "title": item.get_name(),
                    "blocks": blocks
                })

    return chapters, cover_image


# Cover
def extract_cover(book):
    # STEP 1: try OPF metadata correctly
    try:
        meta = book.get_metadata('OPF', 'meta')
        for m in meta:
            attrs = m[1]
            if attrs.get("name") == "cover":
                cover_id = attrs.get("content")

                for item in book.get_items():
                    if item.get_id() == cover_id:
                        return item.get_content()
    except:
        pass

    # STEP 2: look for common cover file patterns
    for item in book.get_items():
        if item.get_type() == 6:
            name = item.get_name().lower()
            if any(x in name for x in ["cover", "front", "title"]):
                return item.get_content()

    # STEP 3: fallback — first image in book (VERY COMMON FIX)
    for item in book.get_items():
        if item.get_type() == 6:
            return item.get_content()

    return None


def build_cover_image(data):

    img = Image.open(io.BytesIO(data))
    img = img.convert("L")
    img = img.resize((W, H))

    return img


# Text processing 
def blocks_to_lines(blocks, font, draw, max_width):
    lines = []

    for block in blocks:

        if block["type"] == "heading":
            lines.append(("heading", block["text"]))
            continue

        words = block["text"].split()
        current = ""

        for word in words:
            test = current + " " + word if current else word

            if draw.textlength(test, font=font) <= max_width:
                current = test
            else:
                lines.append(("text", current))
                current = word

        if current:
            lines.append(("text", current))

        # paragraph spacing
        lines.append(("space", ""))

    return lines


# Pagination
def paginate_lines(lines, line_height, max_height):
    pages = []
    page = []
    used = 0

    for kind, text in lines:

        if kind == "space":
            used += line_height // 2
        else:
            used += line_height

        if used > max_height:
            pages.append(page)
            page = []
            used = 0

        page.append((kind, text))

    if page:
        pages.append(page)

    return pages

def invalidate_pages(chapters):
    for chapter in chapters:
        chapter.pop("pages", None)

# Rendering
def render_page(sections, section_index, page_index, reader_font):

    current_section = sections[section_index]
    pages = current_section["pages"]
    page = pages[page_index]

    def draw(draw, unused_font):

        foreground = display.get_foreground()

        # Header
        draw.text((10, 5),
                  f"{section_index+1}/{len(sections)}  {current_section['title']}",
                  font = reader_font,
                  fill = foreground)

        draw.text((10, 25),
                  f"Page {page_index+1}/{len(pages)}",
                  font = reader_font,
                  fill = foreground)

        y = 60
        line_height = reader_font.getmetrics()[0] + reader_font.getmetrics()[1] + 2

        for kind, text in page:
            if kind == "space":
                y += line_height // 2
                continue

            if y > (H - 10):
                break

            draw.text((10, y), text, font=reader_font, fill=foreground)
            y += line_height


    display.render(draw)


def prepare_chapter(chapter, draw, max_width, max_height, line_height, reader_font):
    lines = blocks_to_lines(chapter["blocks"], reader_font, draw, max_width)
    chapter["pages"] = paginate_lines(lines, line_height, max_height)


# Continue screen
def render_resume_screen(saved_position, book_title, resume_selection):
    def draw(draw, font):

        # Book title
        draw.text(
            (10, 40),
            book_title,
            font=display.font_title,
            fill=display.get_foreground()
        )

        # Question
        draw.text(
            (10, 110),
            "Continue reading?",
            font=display.font_menu,
            fill=display.get_foreground()
        )

        # Saved location
        chapter = saved_position["chapter"] + 1
        page = saved_position["page"] + 1

        draw.text(
            (10, 150),
            f"Chapter {chapter}, Page {page}",
            font=display.font_date,
            fill=display.get_foreground()
        )

        # Options
        options = [
            "Continue",
            "Start from beginning"
        ]

        selected = resume_selection

        y = 220

        for i, option in enumerate(options):

            box_x = 15
            box_width = display.W - 30
            box_height = 55

            if i == selected:
                draw.rectangle(
                    (
                        box_x,
                        y,
                        box_x + box_width,
                        y + box_height
                    ),
                    outline = display.get_foreground(),
                    width = 2
                )

            draw.text(
                (box_x + 12, y + 15),
                option,
                font = display.font_menu,
                fill = display.get_foreground()
            )

            y += 70

    display.render(draw)


# Book Controller
def open_book(path):
    reader_settings = settings.load_settings()

    reader_font = settings.get_font(reader_settings)

    chapters, cover_image = load_epub_sections(path)

    print("COVER RAW:", cover_image)

    temp_img = Image.new("L", (W, H))
    draw = ImageDraw.Draw(temp_img)

    max_width = W - 20
    max_height = H - 80

    line_height = reader_font.getmetrics()[0] + reader_font.getmetrics()[1] + 2

    progress = load_progress()

    book_name = os.path.basename(path)

    saved_position = progress.get(book_name)

    state = {
            "mode": "cover",
            "chapter": 0,
            "page": 0,
            "resume_selection": 0
    }
    
    if saved_position:
        state["mode"] = "resume"
    else:
        state["mode"] = "cover"

    def prepare_current_chapter():
        chapter = chapters[state["chapter"]]

        # Don't prepare it twice
        if "pages" in chapter:
            return

        prepare_chapter(chapter, draw, max_width, max_height, line_height, reader_font)

    def next_section():
        if state["chapter"] < len(chapters) - 1:
            state["chapter"] += 1
            state["page"] = 0

            prepare_current_chapter()
            render()

    def previous_section():
        if state["chapter"] > 0:
            state["chapter"] -= 1

            prepare_current_chapter()

            pages = chapters[state["chapter"]]["pages"]

            if len(pages) > 0:
                state["page"] = len(pages) - 1
            else:
                state["page"] = 0

            render()

    def render():
        if state["mode"] == "resume":

            render_resume_screen(
                saved_position,
                book_name,
                state["resume_selection"]
            )

            return

        if state["mode"] == "cover":
            image = Image.new("L", (W, H), 255)

            if cover_image:
                # ensure correct size
                img = cover_image.resize((W, H))

                # paste directly into framebuffer
                image.paste(img, (0, 0))
            else:
                draw = ImageDraw.Draw(image)
                draw.text((10, 10), "No Cover Found", font=display.font_menu, fill=0)

            if display.USE_SIMULATOR:
                display.simulator.show_image(image)
            else:
                display.epd.display_4Gray(
                    display.epd.getbuffer_4Gray(image)
                )         

            return

        prepare_current_chapter()
        
        render_page(
            chapters,
            state["chapter"],
            state["page"],
            reader_font
        )

    render()

    while True:
        key = input().lower()

        if state["mode"] == "resume":

            if key == "s":
                state["resume_selection"] = 1
                render()

            elif key == "w":
                state["resume_selection"] = 0
                render()

            elif key == "":

                if state["resume_selection"] == 0:
                    # Continue reading
                    state["chapter"] = saved_position["chapter"]
                    state["page"] = saved_position["page"]

                else:
                    # Start from beginning
                    state["chapter"] = 0
                    state["page"] = 0
                    state["mode"] = "cover"

                if state["resume_selection"] == 0:
                    state["mode"] = "reading"

                render()

            elif key == "q":
                return

            continue

        if state["mode"] == "cover":

            if key == "d":   # go from cover → book
                state["mode"] = "reading"
                state["chapter"] = 0
                state["page"] = 0
                render()

            elif key == "q":
                return
            
            continue

        if key == "dd":
            next_section()
            continue

        elif key == "aa":
            previous_section()
            continue

        elif key == "d":
            prepare_current_chapter()

            pages = chapters[state["chapter"]]["pages"]

            if state["page"] < len(pages) - 1:
                state["page"] += 1
            else:
                if state["chapter"] < len(chapters) - 1:
                    state["chapter"] += 1
                    state["page"] = 0

                    prepare_current_chapter()

        elif key == "a":
            # BACK TO COVER
            if state["chapter"] == 0 and state["page"] == 0:
                state["mode"] = "cover"
                render()
                continue

            # NORMAL PAGE BACK
            if state["page"] > 0:
                state["page"] -= 1

            else:
                # MOVE TO PREVIOUS CHAPTER SAFELY
                if state["chapter"] > 0:

                    state["chapter"] -= 1

                    prepare_current_chapter()

                    prev_pages = chapters[state["chapter"]]["pages"]

                    # SAFETY: handle empty chapter
                    if len(prev_pages) > 0:
                        state["page"] = len(prev_pages) - 1
                    else:
                        state["page"] = 0

        elif key == "q":

            save_progress(
                path,
                state["chapter"],
                state["page"]
            )
            return

        render()