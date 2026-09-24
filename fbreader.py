# Import Libraries
import os
import display
import subprocess

from pathlib import Path


# Global Variable
BOOKS_DIRECTORY = "protected books"
FBREADER_PATH = None #replace this with new path later on


#
# Load Books
#
book_list = []

for path in os.listdir(BOOKS_DIRECTORY):
    if Path(path).suffix.lower() == ".lcpl":
        # Remove .lcpl
        filename = Path(path).stem 

        # # Try to separate title and author 
        # if "--" in filename: 
        #     title, author = filename.split("--", 1) 
        #     title = title.strip() 
        #     author = author.strip()

        # else:
        #     title = filename.strip()
        #     author = "Unknown Author"

        book_list.append({"title": filename,
                          "author": "",
                          "type": "book",
                          "file_path": os.path.join(BOOKS_DIRECTORY, path)})

book_list.append({"title": "Back to Home",
                  "author": "",
                  "type": "action", 
                  "action": "RETURN"})

#
# Library Settings
#
VISIBLE_BOOKS = 4 # Number of books that can be displayed at once
BOOK_BOX_HEIGHT = 55 # Height of each book selection
BOOK_SPACING = 12 # Space between books


# Helper Functions
def center_text(draw, text, y, font, fill=0): 
    bbox = draw.textbbox( (0, 0), text, font=font) 
    text_width = bbox[2] - bbox[0] 
    x = (display.W - text_width) / 2 
    draw.text( (x, y), text, font=font, fill=fill)


def truncate_text(draw, text, font, max_width):
    ellipsis = "..."

    bbox = draw.textbbox(
        (0, 0),
        text,
        font=font
    )

    if bbox[2] - bbox[0] <= max_width:
        return text

    while True:

        text = text[:-1]

        test = text.rstrip() + ellipsis

        bbox = draw.textbbox(
            (0, 0),
            test,
            font=font
        )

        width = bbox[2] - bbox[0]

        if width <= max_width:
            return test


#
# FBReader Launcher
#
def open_with_fbreader(file_path):
    if FBREADER_PATH is None:
        print("FBReader path has not been configured.")
        return

    if not os.path.exists(FBREADER_PATH):
        print("FBReader executable not found:")
        print(FBREADER_PATH)
        return

    if not os.path.exists(file_path):
        print("Book file not found:")
        print(file_path)
        return

    try:
        subprocess.Popen([
            FBREADER_PATH,
            file_path
        ])

    except Exception as error:
        print("Could not launch FBReader:")
        print(error)

#
# Library Menu Display
#

def fbreader_menu_state(index, scroll_offset):
    def draw(draw, font):
        display.draw_header(draw)

        center_text(draw, "FBReader", 55, display.font_title)

        start_y = 100 

        end_index = min(scroll_offset + VISIBLE_BOOKS, len(book_list))

        visible_items = book_list[scroll_offset:end_index] 

        for visible_index, item in enumerate(visible_items): 
            actual_index = (scroll_offset + visible_index) 
            y = (start_y + visible_index * (BOOK_BOX_HEIGHT + BOOK_SPACING))
    
            box_x = 15 
            box_width = display.W - 30

            if actual_index == index: 
                draw.rectangle((box_x, y, box_x + box_width, y + BOOK_BOX_HEIGHT ), outline=0, width=2)

            # Book Title
            if item["type"] == "book":
                title = truncate_text(draw, item["title"], display.font_book_title, box_width - 24)
                draw.text((box_x + 12, y + 8), title, font=display.font_book_title, fill=0)
                # draw.text((box_x + 12, y + 34), item["author"], font=display.font_book_author, fill=0)

            else: 
                center_text(draw, item["title"], y + 16, display.font_menu)

        # Scroll indicator
        if len(book_list) > VISIBLE_BOOKS:
            current_position = index + 1 
            indicator = (f"{current_position} / {len(book_list)}") 
            bbox = draw.textbbox((0, 0), indicator, font=display.font_date)
            indicator_width = (bbox[2] - bbox[0]) 
            draw.text((display.W - indicator_width - 10, display.H - 25), indicator, font=display.font_date, fill=0)

    display.render(draw)


#
# Menu State
#
def run_state(index):
    item = book_list[index]

    if item["type"] == "action":
        if item["action"] == "RETURN":
            return True

    elif item["type"] == "book":
        ## enter new thing here
        return False

    return False

#
# Clock
#
def update_clock():
    fbreader_menu_state(menu_index,scroll_offset)

#
# Functions
#
def fbreader_menu():
    global menu_index
    global scroll_offset

    menu_index = 0
    scroll_offset = 0

    fbreader_menu_state(menu_index, scroll_offset)

    display.start_clock(update_clock)

    while True:
        user_input = input()

        if user_input == 's':
            if menu_index == (len(book_list) - 1):
                menu_index = 0
                scroll_offset = 0
            else:
                menu_index += 1
                # Scroll down if necessary 
                if (menu_index >= scroll_offset + VISIBLE_BOOKS): 
                    scroll_offset += 1

            fbreader_menu_state(menu_index, scroll_offset)

        
        if user_input == 'w':
            if menu_index == 0:
                menu_index = (len(book_list) - 1)
                scroll_offset = max(0, len(book_list) - VISIBLE_BOOKS)
            else:
                menu_index -= 1

                # Scroll up if necessary
                if menu_index < scroll_offset:
                    scroll_offset -= 1

            fbreader_menu_state(menu_index, scroll_offset)

        if user_input == '':
            should_exit = run_state(menu_index)

            if should_exit:
                return
            
            fbreader_menu_state(menu_index, scroll_offset)



def main():
    fbreader_menu()


if __name__ == "__main__":
    main()