# Gesture Control System

## Overview

This project, developed by **Subhas Adhikari and his teammates**, implements a gesture control system using **PyQt5**, **OpenCV**, **MediaPipe**, and **PyInstaller**. It allows users to control mouse actions, scroll, take screenshots, and even shut down their system using hand gestures detected via a webcam.

## Features

- Mouse Movement: Move the cursor using your index finger.
- Left Click: Perform a left-click gesture.
- Right Click: Perform a right-click gesture.
- Double Click: Perform a double-click gesture.
- Scrolling: Scroll up and down using gestures.
- Drag & Drop: Drag objects by holding a specific hand position.
- Shutdown Gesture: Trigger system shutdown using a predefined gesture.
- Voice Activation: Start the application using voice commands.
- Screenshot Capture: Take a screenshot using a gesture.

## Installation

 # Prerequisites

Ensure you have Python 3 installed and set up in a virtual environment (recommended).

## Required Libraries

Install dependencies using pip:

pip install opencv-python mediapipe pyautogui numpy PyQt5 pynput sounddevice vosk


## Setting Up the Vosk Model for Voice Control

Download and extract the Vosk model if not already installed:


wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip


Update the `MODEL_PATH` in `voiceAssistant.py` accordingly.

Usage

# Running the Application

To start the gesture control system, run:
python newui.py

The application will wait for the voice command **'open'** to start the camera.

Gesture Controls

| Gesture                     | Action                          |
| --------------------------- | ------------------------------- |
| Open Hand                   | Move the mouse                  |
| Thumb + Index Finger Close  | Left Click                      |
| Thumb + Middle Finger Close | Right Click                     |
| All Fingers Close           | Shutdown System (Cmd+Space+F12) |
| Index Finger Up             | Scroll Up                       |
| Pinky Finger Up             | Scroll Down                     |
| Two-Finger Tap              | Double Click                    |             |

### Voice Commands

| Command | Action               |
| ------- | -------------------- |
| open    | Start the camera     |
| stop    | Exit the application |

## File Structure

project_directory/
│── main.py               # Gesture control logic
│── newui.py              # PyQt5 GUI for camera feed
│── util.py               # Helper functions for calculations
│── voiceAssistant.py     # Voice activation module
│── requirements.txt      # List of dependencies

## Creating an Executable

To package the application into an executable file using PyInstaller, run:

pyinstaller --onefile --windowed newui.py

This will generate an executable file inside the `dist` folder.

## Troubleshooting

- Ensure your webcam is accessible and functioning properly.
- If voice commands don't work, check your microphone permissions and ensure the correct audio device is selected.
- If gestures are not detected, adjust the **min\_detection\_confidence** parameter in `ma.py`.
- If screenshots are not saving, check the file path and ensure the `screenshots/` folder exists.

## Future Enhancements

- Adding more gesture-based controls.
- Improving voice recognition for better accuracy.
- Enhancing UI for better user interaction.

## License

This project is licensed under Subhas Adhikari and his teammate . It is not open-source and cannot be modified or distributed without permission.


