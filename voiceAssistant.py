import os
import sys
import time
import subprocess
import json
import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import signal
import threading
from PyQt5.QtCore import pyqtSignal

GESTURE_CONTROL_SCRIPT = "main.py" 

MODEL_PATH = "/Users/subhasadhikari/Desktop/phol/vosk-model-small-en-us-0.15"
if not os.path.exists(MODEL_PATH):
    print("Downloading Vosk model...")
    os.system(f"wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip")
    os.system("unzip vosk-model-small-en-us-0.15.zip")
    
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, 16000)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))


def listen_for_command(start_signal,exit_signal):   
    camera_started = False

    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("Listening for 'open' command...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").lower()
                print(f"Recognized: {text}")

                if "open" in text and not camera_started:
                    print("Starting Camera...")
                    start_signal.emit()  #Todo:start of the camera
                    camera_started = True 

                elif "stop" in text:
                    print("Exiting program...")
                    exit_signal.emit()
                    break  

def start_video_thread():
    """ Start the newui.py script with video thread """
    global process
    if process is None or process.poll() is not None:
        process = subprocess.Popen(["python3", GESTURE_CONTROL_SCRIPT]) 
        print("Gesture control and video thread started.")
        time.sleep(2) 

if __name__ == "__main__":
    listen_for_command()
