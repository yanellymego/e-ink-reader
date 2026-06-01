import os
from PIL import Image, ImageDraw, ImageFont

class LibraryScene:
    def __init__(self, renderer):
        self.renderer = renderer
        if not os.path.exists("books"): os.makedirs("books")
        self.books = [f for f in os.listdir("books") if f.endswith(".epub")]
        self.selected_index = 0

    def render(self):
        img = Image.new('1', (600, 800), 255)
        draw = ImageDraw.Draw(img)
        
        # Title with more padding
        draw.text((self.renderer.margin, 50), "LIBRARY", font=self.renderer.font_bold, fill=0)
        draw.line((self.renderer.margin, 100, 550, 100), fill=0)

        # Increased line spacing from 60 to 100
        for i, book in enumerate(self.books):
            y = 150 + (i * 100) 
            if i == self.selected_index:
                # Bigger selection box
                draw.rectangle([40, y-10, 560, y+60], fill=0)
                draw.text((60, y), book[:30], font=self.renderer.font_main, fill=255)
            else:
                draw.text((60, y), book[:30], font=self.renderer.font_main, fill=0)
        return img

    def handle_input(self, action):
        if action == "NEXT":
            self.selected_index = (self.selected_index + 1) % len(self.books)
        elif action == "SELECT":
            return self.books[self.selected_index]
        return None