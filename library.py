# Import Libraries
import os
import menu
import display
import reader

from pathlib import Path


# Global Variable
book_list = []

for path in os.listdir("books"):
    if Path(path).suffix == ".epub":
        title = path.split("--")[0].strip()
        book_list.append({"title": title,
                          "type": "book",
                          "file_path": os.path.join("books", path)})

book_list.append({"title": "return to menu",
                  "type": "action", 
                  "action": "RETURN"})


# Helper Functions
def lib_menu_state(index):
    def draw(draw, font):
        draw.text((10, 10), "~ LIBRARY ~", font=font, fill=0)
    
        y = 40

        for i, item in enumerate(book_list):
            if i == index:
                prefix = "> "
            else: 
                prefix = "  "

            draw.text((10, y), f"{prefix} {item['title']}", font=font, fill=0)
            y += 25 
    
    display.render(draw)


def run_state(index):
    item = book_list[index]

    if item["type"] == "action":
        if item["action"] == "RETURN":
            return True

    elif item["type"] == "book":
        reader.open_book(item["file_path"])
        return False

    return False



# Functions
def library_menu():
    menu_index = 0

    lib_menu_state(menu_index)
    while True:
        user_input = input()

        if user_input == 's':
            if menu_index == (len(book_list) - 1):
                menu_index = 0
            else:
                menu_index += 1
            lib_menu_state(menu_index)
        
        if user_input == 'w':
            if menu_index == 0:
                menu_index = (len(book_list) - 1)
            else:
                menu_index -= 1
            lib_menu_state(menu_index)

        if user_input == '':
            lib_menu_state(menu_index)
            should_exit = run_state(menu_index)

            if should_exit:
                return
            
            lib_menu_state(menu_index)



def main():
    library_menu()


if __name__ == "__main__":
    main()