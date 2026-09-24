import os
import json
from PIL import ImageFont

# Global variables
SETTINGS_FILE = "settings.json"

DEFAULT_SETTINGS = {
    "font": "Figtree-Regular.ttf",
    "font_size": 16,
    "dark_mode": False
    }

AVAILABLE_FONTS = ["Figtree-Regular.ttf", "EBGaramond-Regular.ttf", "Literata_18pt-Regular.ttf", "Montserrat-Regular.ttf", "Roboto_Condensed-Regular.ttf"]



# Functions
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return DEFAULT_SETTINGS.copy()

    try:
        with open(SETTINGS_FILE, "r") as file:
            saved_settings = json.load(file)

        settings = DEFAULT_SETTINGS.copy()
        settings.update(saved_settings)

        return settings

    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(settings):
    with open(SETTINGS_FILE, "w") as file:
        json.dump(settings, file, indent=4)



# Font
def get_font(settings):
    base_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    font_dir = os.path.join(
        base_dir,
        "fonts"
    )

    font_path = os.path.join(
        font_dir,
        settings["font"]
    )

    return ImageFont.truetype(
        font_path,
        size=settings["font_size"]
    )



# Font size
def increase_font_size(settings):
    sizes = [14, 16, 18, 20, 22, 24, 28, 32]

    current = settings["font_size"]

    for size in sizes:
        if size > current:
            settings["font_size"] = size
            break

    save_settings(settings)


def decrease_font_size(settings):
    sizes = [14, 16, 18, 20, 22, 24, 28, 32]

    current = settings["font_size"]

    for size in reversed(sizes):
        if size < current:
            settings["font_size"] = size
            break

    save_settings(settings)


# Dark mode
def toggle_dark_mode(settings):
    settings["dark_mode"] = not settings["dark_mode"]

    save_settings(settings)