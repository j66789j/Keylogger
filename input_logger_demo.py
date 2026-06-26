import time
from pynput import keyboard, mouse

mouse_listener = None
keyboard_listener = None

def current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def show_event(category, event_type, description=""):
    output = f"[{current_time()}] {category:<8} {event_type:<11}"
    if description:
        output += f" | {description}"
    print(output)


def stop_program():
    global mouse_listener, keyboard_listener
    if mouse_listener is not None:
        mouse_listener.stop()
    if keyboard_listener is not None:
        keyboard_listener.stop()


def on_press(key):
    if key == keyboard.Key.esc:
        show_event("CONTROL", "Exit", "Escape pressed")
        stop_program()
        return False
    
    try:
        value = key.char
        description = "Typed character"
    except AttributeError:
        value = str(key).replace("Key.", "")
        description = "Special key"

    show_event("KEY", value, description)


def on_click(x, y, button, pressed):
    if pressed:
        show_event("INPUT", "Mouse click", f"{button} at ({x}, {y})")


print("Input analyzer started. Press Esc to stop.")
print("Listening for keyboard and mouse events...")
print("=" * 60 , "\n")

with keyboard.Listener(on_press=on_press) as keyboard_listener:
    with mouse.Listener(on_click=on_click) as active_mouse_listener:
        mouse_listener = active_mouse_listener
        keyboard_listener.join()

print("\nInput analyzer stopped.")
print("=" * 60)