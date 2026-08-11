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

#Draws text centered horizontally on the display.
def center_text(draw, text, y, font, fill=0): 
    bbox = draw.textbbox((0, 0), text, font=font) 
    text_width = bbox[2] - bbox[0] 
    x = (display.W - text_width) / 2 
    draw.text( (x, y), text, font=font, fill=fill )

def menu_state(index, MENU):
    def draw(draw, font):
        display.draw_header(draw)

        y = 60

        # Fixed dimensions for every menu option
        box_width = 190
        box_height = 45

        box_x = (display.W - box_width) / 2


        for i, item in enumerate(MENU):
            text = item["name"]

            # Get the dimensions of the text
            bbox = draw.textbbox(
                (0, 0),
                text,
                font=display.font_menu
            )

            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]

            # Center the text horizontally
            text_x = (display.W - text_width) / 2
            text_y = y + (box_height - text_height) / 2

            if i == index:
                # Rectangle surrounding selected option
                draw.rectangle(
                (
                    box_x,
                    y,
                    box_x + box_width,
                    y + box_height
                ),
                outline=0,
                width=2
            )

            
            draw.text(
                (text_x, text_y),
                text,
                font=display.font_menu,
                fill=0
            )
            y += 50

    display.render(draw)


def run_state(index):
    MENU[index]["action"]()

def update_clock():
    menu_state(menu_index)

# Main Functions
def menu():
    global menu_index

    menu_index = 0
    menu_state(menu_index, MENU)
    display.start_clock(update_clock)

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