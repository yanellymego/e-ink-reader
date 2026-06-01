# Import Libraries
import library
import display


# Scenes from other files
def open_library_screen():
    library.main()
     

# Constant Global Variable
MENU = [
    {"name": "Library", "action": open_library_screen},
    {"name": "Settings", "action": lambda: print("Settings not built yet")},
    {"name": "FBReader", "action": lambda: print("FBReader not built yet")}
] 


# Helper Functions
def menu_state(index, MENU):
    def draw(draw, font):
        draw.text((10, 10), "~ MENU ~", font=font, fill=0)

        y = 40

        for i, item in enumerate(MENU):
            if i == index:
                prefix = ">"
            else: 
                prefix = " "
            
            draw.text((10, y), f"{prefix} {item['name']}", font=font, fill=0)
            y += 25

    display.render(draw)


def run_state(index):
    MENU[index]["action"]()


# Main Functions
def menu():
    menu_index = 0

    menu_state(menu_index, MENU)
    while True:
        user_input = input()

        if user_input == 's':
            if menu_index == (len(MENU) - 1):
                menu_index = 0
            else:
                menu_index += 1
            menu_state(menu_index, MENU)
        
        if user_input == 'w':
            if menu_index == 0:
                menu_index = (len(MENU) - 1)
            else:
                menu_index -= 1
            menu_state(menu_index, MENU)

        if user_input == '':
            run_state(menu_index)        
            menu_state(menu_index, MENU)
    
def main():
    menu()
        
if __name__ == "__main__":
    main()