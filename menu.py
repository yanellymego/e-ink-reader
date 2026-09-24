# Import Libraries
import library
import display
import fbreader
import settings


# Scenes from other files
def open_library_screen():
    library.main()

def open_fbreader_screen():
    fbreader.main()

def open_settings_screen():
    settings_menu()

# Constant Global Variable
MENU = [
    {"name": "Library", "action": open_library_screen},
    {"name": "Settings", "action": open_settings_screen},
    {"name": "FBReader", "action": open_fbreader_screen}
] 


# Helper Functions

#Draws text centered horizontally on the display.
def center_text(draw, text, y, font, fill=display.get_foreground()): 
    bbox = draw.textbbox((0, 0), text, font=font) 
    text_width = bbox[2] - bbox[0] 
    x = (display.W - text_width) / 2 
    draw.text( (x, y), text, font=font, fill=fill)

def menu_state(index, MENU):
    def draw(draw, font):
        foreground = display.get_foreground()
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
                outline=foreground,
                width=2
            )

            
            draw.text(
                (text_x, text_y),
                text,
                font=display.font_menu,
                fill=foreground
            )
            y += 50

    display.render(draw)


def run_state(index):
    MENU[index]["action"]()

def update_clock():
    menu_state(menu_index, MENU)

def settings_menu():
    selected = 0

    while True:
        current_settings = settings.load_settings()

        font_name = current_settings["font"].replace(".ttf", "").replace("-", " ")
        font_size = current_settings["font_size"]

        options = [
            f"Font: {font_name}",
            f"Size: {font_size}",
            "Dark Mode",
            "Restore Defaults",
            "Back"
        ]

        while True:
            def draw(draw, font):
                foreground = display.get_foreground()

                display.draw_header(draw)

                draw.text(
                    (10, 60),
                    "Settings",
                    font=display.font_title,
                    fill=foreground
                )

                y = 120

                for i, option in enumerate(options):
                    if i == selected:
                        draw.rectangle(
                            (15, y, display.W - 15, y + 45),
                            outline=foreground,
                            width=2
                        )

                    draw.text(
                        (30, y + 10),
                        option,
                        font=display.font_menu,
                        fill=foreground
                    )

                    y += 55

            display.render(draw)

            key = input().lower()

            if key == "s":
                selected = (selected + 1) % len(options)

            elif key == "w":
                selected = (selected - 1) % len(options)

            elif key == "":
                if selected == 0:
                    change_font()
                    break

                elif selected == 1:
                    change_font_size()
                    break

                elif selected == 2:
                    current_settings = settings.load_settings()
                    settings.toggle_dark_mode(current_settings)

                elif selected == 3:
                    restore_default_settings()

                elif selected == 4:
                    return
            

def change_font():
    current_settings = settings.load_settings()

    fonts = settings.AVAILABLE_FONTS

    # Start on the currently selected font
    if current_settings["font"] in fonts:
        selected = fonts.index(current_settings["font"])
    else:
        selected = 0

    while True:
        def draw(draw, font):
            foreground = display.get_foreground()

            display.draw_header(draw)

            # y = 70
            draw.text(
                (10, 60),
                "Font",
                font=display.font_title,
                fill=foreground
            )

            y = 120

            for i, option in enumerate(fonts):

                if i == selected:

                    draw.rectangle(
                        (
                            15,
                            y,
                            display.W - 15,
                            y + 45
                        ),
                        outline=foreground,
                        width=2
                    )

                text = option.replace(".ttf", "").replace("-", " ")

                draw.text(
                    (30, y + 10),
                    text,
                    font=display.font_menu,
                    fill=foreground
                )

                y += 55

            # Back option
            if selected == len(fonts):
                draw.rectangle(
                    (80, y, display.W - 80, y + 45),
                    outline=foreground,
                    width=2
                )

            back_text = "Back"

            back_bbox = draw.textbbox(
                (0, 0),
                back_text,
                font=display.font_menu
            )

            back_width = back_bbox[2] - back_bbox[0]
            back_height = back_bbox[3] - back_bbox[1]

            back_x = (display.W - back_width) / 2
            back_y = y + (45 - back_height) / 2

            draw.text(
                (back_x, back_y),
                back_text,
                font=display.font_menu,
                fill=foreground
            )

        display.render(draw)

        key = input().lower()

        if key == "w":
            selected = (selected - 1) % (len(fonts) + 1)

        elif key == "s":
            selected = (selected + 1) % (len(fonts) + 1)

        elif key == "":
            # Back
            if selected == len(fonts):
                return

            # Save selected font
            current_settings["font"] = fonts[selected]
            settings.save_settings(current_settings)


def change_font_size():

    current_settings = settings.load_settings()

    sizes = [14, 16, 18, 20, 22, 24, 28, 32]

    # Start on the currently selected font size
    if current_settings["font_size"] in sizes:
        selected = sizes.index(current_settings["font_size"])
    else:
        selected = 0

    # Number of font sizes visible at once
    VISIBLE_SIZES = 4

    scroll_offset = max(
        0,
        selected - VISIBLE_SIZES + 1
    )

    while True:

        # Keep selected size visible
        if selected < scroll_offset:
            scroll_offset = selected

        elif selected >= scroll_offset + VISIBLE_SIZES:
            scroll_offset = selected - VISIBLE_SIZES + 1

        def draw(draw, font):

            foreground = display.get_foreground()

            display.draw_header(draw)

            draw.text(
                (10, 60),
                "Font Size",
                font=display.font_title,
                fill=foreground
            )

            y = 120

            # Only show visible font sizes
            end_index = min(
                scroll_offset + VISIBLE_SIZES,
                len(sizes)
            )

            visible_sizes = sizes[scroll_offset:end_index]

            for visible_index, option in enumerate(visible_sizes):

                actual_index = scroll_offset + visible_index

                if actual_index == selected:
                    draw.rectangle(
                        (
                            15,
                            y,
                            display.W - 15,
                            y + 45
                        ),
                        outline=foreground,
                        width=2
                    )

                draw.text(
                    (30, y + 10),
                    str(option),
                    font=display.font_menu,
                    fill=foreground
                )

                y += 55

            # Back option
            if selected == len(sizes):
                draw.rectangle(
                    (
                        80,
                        y,
                        display.W - 80,
                        y + 45
                    ),
                    outline=foreground,
                    width=2
                )

            back_text = "Back"

            back_bbox = draw.textbbox(
                (0, 0),
                back_text,
                font=display.font_menu
            )

            back_width = back_bbox[2] - back_bbox[0]
            back_height = back_bbox[3] - back_bbox[1]

            back_x = (display.W - back_width) / 2
            back_y = y + (45 - back_height) / 2

            draw.text(
                (back_x, back_y),
                back_text,
                font=display.font_menu,
                fill=foreground
            )

        display.render(draw)

        key = input().lower()

        if key == "w":

            selected = (
                selected - 1
            ) % (len(sizes) + 1)

        elif key == "s":

            selected = (
                selected + 1
            ) % (len(sizes) + 1)

        elif key == "":

            # Back
            if selected == len(sizes):
                return

            # Save selected font size
            current_settings["font_size"] = sizes[selected]
            settings.save_settings(current_settings)

def restore_default_settings():
    current_settings = settings.load_settings()

    current_settings = settings.DEFAULT_SETTINGS.copy()

    settings.save_settings(current_settings)

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