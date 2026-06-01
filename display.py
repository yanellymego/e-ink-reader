from PIL import Image, ImageDraw, ImageFont

# Toggle this depending on where you're running
USE_SIMULATOR = True

# Define screen size
W, H = 280, 480 


font = ImageFont.load_default()

# --- Simulator import (only used if enabled) ---
if USE_SIMULATOR:
    import simulator
else:
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