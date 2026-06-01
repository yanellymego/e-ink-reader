import os
from PIL import Image, ImageDraw, ImageFont

# Toggle this depending on where you're running
USE_SIMULATOR = os.getenv("EREADER_SIM", "0") == "1"

font = ImageFont.load_default()

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


# --- Render function ---
def render(draw_fn):
    image = Image.new('L', (W, H), 255)
    draw = ImageDraw.Draw(image)

    draw_fn(draw, font)

    if USE_SIMULATOR:
        simulator.show_image(image)
    else:
        epd.display_4Gray(epd.getbuffer_4Gray(image))