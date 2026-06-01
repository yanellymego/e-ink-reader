from pynput import keyboard

# This variable will hold the 'input_handler' function from main.py
callback = None

def on_press(key):
    global callback
    if not callback:
        return

    try:
        # Mapping keyboard keys to your 4-button actions
        if key == keyboard.Key.right:
            callback("NEXT")
        elif key == keyboard.Key.left:
            callback("PREV")
        elif key == keyboard.Key.up:
            callback("SELECT")
        elif key == keyboard.Key.down:
            callback("BACK")
    except AttributeError:
        pass

def start_listening(main_app_callback):
    """
    This starts a background 'listener' that waits for key presses
    without stopping the rest of your program.
    """
    global callback
    callback = main_app_callback
    
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    print("Button Simulator Active: Use ARROW KEYS to navigate.")