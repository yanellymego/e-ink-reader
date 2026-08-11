# Import libraries
from ebooklib import epub
from bs4 import BeautifulSoup
from display import W, H, font
from PIL import Image, ImageDraw, ImageOps

import io
import display

#
# Helper Functions
#

# EPUB Loading
def load_epub_sections(path):
    book = epub.read_epub(path)

    cover_bytes = extract_cover(book)
    print("COVER FOUND:", cover_bytes is not None)
    cover_image = build_cover_image(cover_bytes)

    chapters = []

    for item in book.get_items():
        if item.get_type() == 9:  # document (HTML content)
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


# Rendering
def render_page(sections, section_index, page_index):

    current_section = sections[section_index]
    pages = current_section["pages"]
    page = pages[page_index]

    def draw(draw, font):

        # Header
        draw.text((10, 5),
                  f"{section_index+1}/{len(sections)}  {current_section['title']}",
                  font=font,
                  fill=0)

        draw.text((10, 25),
                  f"Page {page_index+1}/{len(pages)}",
                  font=font,
                  fill=0)


        y = 60
        line_height = font.getmetrics()[0] + font.getmetrics()[1] + 2

        for kind, text in page:
            if kind == "space":
                y += line_height // 2
                continue

            if y > (H - 10):
                break

            draw.text((10, y), text, font=font, fill=0)
            y += line_height


    display.render(draw)


def prepare_chapter(chapter, draw, max_width, max_height, line_height):
    lines = blocks_to_lines(chapter["blocks"], font, draw, max_width)
    chapter["pages"] = paginate_lines(lines, line_height, max_height)
    

# Book Controller
def open_book(path):
    chapters, cover_image = load_epub_sections(path)

    print("COVER RAW:", cover_image)

    temp_img = Image.new("L", (W, H))
    draw = ImageDraw.Draw(temp_img)

    max_width = W - 20
    max_height = H - 80

    line_height = font.getmetrics()[0] + font.getmetrics()[1] + 2

    # # Build pages per chapter
    # for chapter in chapters:

    #     lines = blocks_to_lines(
    #         chapter["blocks"],
    #         font,
    #         draw,
    #         max_width
    #     )

    #     chapter["pages"] = paginate_lines(
    #         lines,
    #         line_height,
    #         max_height
    #     )

    state = {
        "mode": "cover",
        "chapter": 0,
        "page": 0
    }

    def prepare_current_chapter():
        chapter = chapters[state["chapter"]]

        # Don't prepare it twice
        if "pages" in chapter:
            return

        prepare_chapter(chapter, draw, max_width, max_height, line_height)    

    def render():
        if state["mode"] == "cover":
            image = Image.new("L", (W, H), 255)

            if cover_image:
                # ensure correct size
                img = cover_image.resize((W, H))
                img = ImageOps.invert(img)

                # paste directly into framebuffer
                image.paste(img, (0, 0))
            else:
                draw = ImageDraw.Draw(image)
                draw.text((10, 10), "No Cover Found", font=font, fill=0)

            display.render(lambda d, f: d.bitmap((0, 0), image, fill=0))
            return

        prepare_current_chapter()
        
        render_page(
            chapters,
            state["chapter"],
            state["page"]
        )

    render()

    while True:
        key = input().lower()

        if state["mode"] == "cover":

            if key == "d":   # go from cover → book
                state["mode"] = "reading"
                state["chapter"] = 0
                state["page"] = 0
                render()

            elif key == "q":
                return
            
            continue

        if key == "d":
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
            return

        render()