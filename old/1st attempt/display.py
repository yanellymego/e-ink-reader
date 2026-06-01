import tkinter as tk
from PIL import ImageTk

class MockScreen:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DIY E-Reader Mockup")
        self.label = tk.Label(self.root)
        self.label.pack()

    def display_image(self, pil_image):
        tk_img = ImageTk.PhotoImage(pil_image)
        self.label.config(image=tk_img)
        self.label.image = tk_img 
        self.root.update()

screen = MockScreen()