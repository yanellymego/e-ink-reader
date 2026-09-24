import os
import time
import threading
import settings

from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Toggle this depending on where you're running
USE_SIMULATOR = os.getenv("EREADER_SIM", "0") == "1"
# USE_SIMULATOR = True

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(BASE_DIR, "fonts")

font_date= ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-Regular.ttf"), size=17)
font_time = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-SemiBold.ttf"), size=17)
font_title = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-SemiBold.ttf"), size=28)
font_book_title = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-SemiBold.ttf"), size=21)
font_book_author = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-Regular.ttf"), size=17)
font_menu = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-Regular.ttf"), size=21)
font = ImageFont.truetype(os.path.join(FONT_DIR, "Figtree-Regular.ttf"), size=17)


W, H = 280, 480

epd = None
simulator = None


def init_display():
    global epd, simulator, W, H

    if USE_SIMULATOR:
        import simulator
        return

    from waveshare_epd import epd3in7

    epd = epd3in7.EPD()
    epd.init(0)
    epd.Clear(0, 0)

    W, H = epd.width, epd.height


# -- Clock --
def draw_header(draw):
    foreground = get_foreground()

    now = datetime.now()
    date_text = now.strftime("%a, %b %d").replace(" 0", " ")
    time_text = now.strftime("%I:%M %p").lstrip("0")


    # Date - left side
    draw.text(
        (10, 10),
        date_text,
        font=font_date,
        fill=foreground
    )

    # Time - right side
    time_bbox = draw.textbbox(
        (0, 0),
        time_text,
        font=font_time
    )

    time_width = time_bbox[2] - time_bbox[0]

    draw.text(
        (W - time_width - 10, 9),
        time_text,
        font=font_time,
        fill=foreground
    )

    # Divider
    draw.line(
        (10, 38, W - 10, 38),
        fill=foreground,
        width=1
    )


# --- Render function ---
def get_background():
    current_settings = settings.load_settings()

    if current_settings["dark_mode"]:
        return 0

    return 255


def get_foreground():
    current_settings = settings.load_settings()

    if current_settings["dark_mode"]:
        return 255

    return 0


def render(draw_fn):
    background = get_background()

    image = Image.new(
        'L',
        (W, H),
        background
    )

    draw = ImageDraw.Draw(image)

    draw_fn(draw, font)

    if USE_SIMULATOR:
        simulator.show_image(image)
    else:
        epd.display_4Gray(
            epd.getbuffer_4Gray(image)
        )


# Clock Refresh
_clock_callback = None
_clock_running = False

def start_clock(update_callback):
    global _clock_callback
    global _clock_running

    _clock_callback = update_callback

    if _clock_running:
        return

    _clock_running = True

    thread = threading.Thread(
        target=_clock_loop,
        daemon=True
    )

    thread.start()


def _clock_loop():
    global _clock_running

    while _clock_running:

        # Wait until the next minute
        time.sleep(60)

        if _clock_callback is not None:
            _clock_callback()