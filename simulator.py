import tkinter as tk
from PIL import ImageTk

root = tk.Tk()

# Window properties
root.title("E-reader")
root.geometry("280x480")
root.resizable(False, False)

# Widget that will hold the screen image
screen = tk.Label(root, width=280, height=480)
screen.pack()

# Keep a reference to prevent garbage collection
current_image = None


def show_image(image):
    """
    Displays a Pillow image in the simulator window.
    """

    global current_image

    current_image = ImageTk.PhotoImage(image)

    screen.config(image=current_image)

    # Update window immediately
    root.update_idletasks()
    root.update()


def start():
    """
    Starts the simulator event loop.
    """
    root.mainloop()