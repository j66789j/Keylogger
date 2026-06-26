# Keylogger

## Overview

This project is a simple input monitor designed for educational purposes only. It demonstrates how to capture keyboard and mouse events in Python and display them in the console. The project is intended for learning, experiment, and development of event-driven input handling.

## How It Works

The script uses the `pynput` library to listen for input events from the keyboard and mouse.

- Keyboard events: The program logs each key pressed and classifies regular characters and special keys.
- Mouse events: The program logs each mouse click and includes the button used and the click location.
- Exit trigger: Press the `Esc` key to stop the listener and end the program.

## Usage

1. Install the required dependency:

```bash
pip install -r requirements.txt
```

2. Run the script:

```bash
python input_logger_demo.py
```

3. The program will start listening and print input events in the terminal.
4. Press `Esc` to safely stop the program.

## Important Note

This project is for educational purposes only. Do not use it to record or monitor input without explicit permission from the owner of the device or system. Respect privacy and legal boundaries.

## Questions

If you have any questions or need help understanding the code, feel free to ask.