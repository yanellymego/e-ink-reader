import buttons
import display
import library
import reader
import renderer
import time

class EReaderApp:
    def __init__(self):
        self.renderer = renderer.Renderer()
        self.lib_scene = library.LibraryScene(self.renderer)
        self.read_scene = None
        self.state = "LIBRARY"
        self.refresh()

    def handle_input(self, action):
        if self.state == "LIBRARY":
            selected_book = self.lib_scene.handle_input(action)
            if selected_book:
                self.read_scene = reader.ReaderScene(selected_book, self.renderer)
                self.state = "READING"
        
        elif self.state == "READING":
            if action == "BACK":
                self.state = "LIBRARY"
            else:
                self.read_scene.handle_input(action)
        
        self.refresh()

    def refresh(self):
        img = self.lib_scene.render() if self.state == "LIBRARY" else self.read_scene.render()
        display.screen.display_image(img)

if __name__ == "__main__":
    app = EReaderApp()
    buttons.start_listening(app.handle_input)
    display.screen.root.mainloop()