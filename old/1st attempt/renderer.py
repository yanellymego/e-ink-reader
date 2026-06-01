from PIL import Image, ImageDraw, ImageFont

class Renderer:
    def __init__(self, width=600, height=800):
        self.width = width
        self.height = height
        self.margin = 50
        
        # Load fonts - Adjust paths for Windows
        try:
            self.font_main = ImageFont.truetype("georgia.ttf", 28)
            self.font_bold = ImageFont.truetype("georgiab.ttf", 32)
            self.font_tiny = ImageFont.truetype("arial.ttf", 20)
        except:
            self.font_main = ImageFont.load_default()
            self.font_bold = ImageFont.load_default()
            self.font_tiny = ImageFont.load_default()

    def draw_status_bar(self, draw, current_idx, total_len):
        progress = int((current_idx / total_len) * 100) if total_len > 0 else 0
        y_bar = self.height - 40
        
        # Status line
        draw.line((self.margin, y_bar, self.width - self.margin, y_bar), fill=0)
        
        # Progress text
        draw.text((self.margin, y_bar + 10), f"Progress: {progress}%", font=self.font_tiny, fill=0)
        
        # Battery mock
        battery_text = "Battery: 100%"
        # Get width of battery text for right-alignment
        bbox = draw.textbbox((0, 0), battery_text, font=self.font_tiny)
        tw = bbox[2] - bbox[0]
        draw.text((self.width - self.margin - tw, y_bar + 10), battery_text, font=self.font_tiny, fill=0)

    def draw_page(self, text_content, start_index, title=""):
        img = Image.new('1', (self.width, self.height), 255)
        draw = ImageDraw.Draw(img)
        
        # Draw Header
        draw.text((self.margin, 20), title[:30].upper(), font=self.font_main, fill=0)
        draw.line((self.margin, 60, self.width - self.margin, 60), fill=0)

        # Pagination Logic
        words = text_content[start_index:].split()
        current_char_count = 0
        y_text = 100
        line_height = 45
        current_line = ""
        
        final_index = -1 # Default to end of book

        for i, word in enumerate(words):
            test_line = current_line + word + " "
            
            # Check if line is too wide
            if draw.textlength(test_line, font=self.font_main) < (self.width - (self.margin * 2)):
                current_line = test_line
            else:
                # Draw the line
                draw.text((self.margin, y_text), current_line, font=self.font_main, fill=0)
                y_text += line_height
                current_line = word + " "
                
                # Check if we hit the bottom (leave room for status bar)
                if y_text > (self.height - 100):
                    # We stop here. Calculate where the NEXT page starts.
                    # The next page starts at original start + characters consumed so far
                    # We find the word we are on in the original string to be precise
                    remaining_text = " ".join(words[i:])
                    final_index = len(text_content) - len(remaining_text)
                    break
        else:
            # This executes if the loop finishes naturally (end of text)
            draw.text((self.margin, y_text), current_line, font=self.font_main, fill=0)

        # Add the status bar
        self.draw_status_bar(draw, start_index, len(text_content))
        
        return img, final_index