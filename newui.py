import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QThread, pyqtSignal
import threading
from ma import GestureControl
from voiceAssistant import listen_for_command  
import os

class VideoThread(QThread):
    update_frame = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.gesture_control = GestureControl()
        self.running = True

    def run(self):
        while self.running:
            frame = self.gesture_control.process_frame()
            if frame is None:
                continue

            h, w, ch = frame.shape
            bytes_per_line = ch * w
            frame = np.ascontiguousarray(frame)
            qt_image = QImage(frame, w, h, bytes_per_line, QImage.Format_RGB888)
            self.update_frame.emit(qt_image)

        self.gesture_control.release_resources()

    def stop(self):
        self.running = False
        self.quit()
        self.wait()


class GestureControlApp(QMainWindow):
    start_signal = pyqtSignal()  
    exit_signal = pyqtSignal()  

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Gesture Control System")
        self.setGeometry(90, 40, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.label = QLabel("Waiting for 'open' command...")
        self.layout.addWidget(self.label)

        self.exit_button = QPushButton("Exit")
        self.exit_button.clicked.connect(self.exit_application) 
        self.layout.addWidget(self.exit_button)

        self.central_widget.setLayout(self.layout)

        self.thread = None

        self.start_signal.connect(self.start_camera)
        self.exit_signal.connect(self.exit_application)

       
        self.voice_thread = threading.Thread(target=self.run_voice_assistant)
        self.voice_thread.daemon = True  
        self.voice_thread.start()
        

    def run_voice_assistant(self):
        listen_for_command(self.start_signal,self.exit_signal) 
    def update_image(self, qt_image):
        self.label.setPixmap(QPixmap.fromImage(qt_image))

    def start_camera(self):
        self.label.setText("Starting Camera...")
        self.thread = VideoThread()
        self.thread.update_frame.connect(self.update_image)
        self.thread.start()

    def exit_application(self):
        print("Exiting the application...")
        if self.thread is not None:
            self.thread.stop() 
        QApplication.quit()  
    def closeEvent(self, event):
        if self.thread is not None:
         self.thread.stop() 
        event.accept() 
     

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestureControlApp()
    window.show()
    sys.exit(app.exec_())
