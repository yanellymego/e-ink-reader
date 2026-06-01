import parser
import textwrap

class ReaderScene:
    def __init__(self, book_path, renderer):
        self.renderer = renderer
        self.book_title = book_path
        self.full_text = parser.extract_text(f"books/{book_path}")
        
        # History of start_indexes for each page
        self.page_bookmarks = [0] 
        self.current_page_idx = 0
        self.current_img = None

    def render(self):
        start_idx = self.page_bookmarks[self.current_page_idx]
        img, next_idx = self.renderer.draw_page(self.full_text, start_idx, self.book_title)
        
        # If we haven't recorded the next page's start yet, do it now
        if next_idx != -1 and len(self.page_bookmarks) <= self.current_page_idx + 1:
            self.page_bookmarks.append(next_idx)
            
        return img

    def handle_input(self, action):
        if action == "NEXT":
            if self.current_page_idx < len(self.page_bookmarks) - 1:
                self.current_page_idx += 1
        elif action == "PREV":
            self.current_page_idx = max(0, self.current_page_idx - 1)