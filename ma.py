import cv2
import mediapipe as mp
import pyautogui
import random
import time
import os
import sys
import util
import numpy as np
from pynput.mouse import Button, Controller

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7,
    max_num_hands=1,
)

class GestureControl:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.draw = mp.solutions.drawing_utils
        self.mouse_movement_enabled = False

    def process_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None

        frame = cv2.flip(frame, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        processed = hands.process(frame)
        landmark_list = []

        if processed.multi_hand_landmarks:
            hand_landmarks = processed.multi_hand_landmarks[0]
            self.draw.draw_landmarks(frame, hand_landmarks, mpHands.HAND_CONNECTIONS)

            for lm in hand_landmarks.landmark:
                landmark_list.append((lm.x, lm.y))

            self.detect_gesture(landmark_list, processed, frame)

        frame = cv2.resize(frame, (640, 480), interpolation=cv2.INTER_LINEAR)
        return frame

    def detect_gesture(self, landmark_list, processed, frame):
        if len(landmark_list) < 21:
            return

        index_finger_tip = self.find_finger_tip(processed)
        thumb_index_dist = util.get_distance([landmark_list[4], landmark_list[5]])

        if self.all_fingers_up(landmark_list) and util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90:
            self.move_mouse(index_finger_tip)

        elif self.left_click(landmark_list, thumb_index_dist):
            mouse.press(Button.left)
            time.sleep(0.2)
            mouse.release(Button.left)
        elif self.right_click(landmark_list, thumb_index_dist):
            mouse.press(Button.right)
            mouse.release(Button.right)
            time.sleep(0.2)
        elif self.double_click(landmark_list, thumb_index_dist):
            pyautogui.doubleClick()
        elif self.screenshot(landmark_list, thumb_index_dist):
            # Get the path for the Pictures folder
            pictures_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Picture')

    # Ensure the Pictures folder exists
            if not os.path.exists(pictures_path):
               os.makedirs(pictures_path)
            im1 = pyautogui.screenshot()
            label = random.randint(1, 1000)
            screenshot_filename= f"my_screenshot_{label}.png"
            im1.save(os.path.join(pictures_path, screenshot_filename))
            print(f"Screenshot saved to {os.path.join(pictures_path, screenshot_filename)}")
        elif self.scroll_down(landmark_list, thumb_index_dist):    
            if thumb_index_dist < 130:
                frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                cv2.putText(frame_bgr, "Scrolling Up", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                pyautogui.scroll(-1)

        elif self.scroll_up(landmark_list):
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            cv2.putText(frame_bgr, "Scrolling Down", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            pyautogui.scroll(1)

    def find_finger_tip(self, processed):
        if processed.multi_hand_landmarks:
            hand_landmarks = processed.multi_hand_landmarks[0]
            return hand_landmarks.landmark[mpHands.HandLandmark.INDEX_FINGER_TIP]
        return None

    def move_mouse(self, index_finger_tip):
        if index_finger_tip is not None:
            x = int(index_finger_tip.x * screen_width)
            y = int(index_finger_tip.y * screen_height)
            pyautogui.moveTo(x, y)

    def left_click(self, landmark_list, thumb_index_dist):
        return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 90 and
            thumb_index_dist > 50
        )

    def right_click(self, landmark_list, thumb_index_dist):
        return (
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 90 and
            thumb_index_dist > 50
        )

    def double_click(self, landmark_list, thumb_index_dist):
        return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 70 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 70 and
            thumb_index_dist > 50
        )

    def screenshot(self, landmark_list, thumb_index_dist):
        return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) < 50 and
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) < 50 and
            thumb_index_dist < 50
        )

    def scroll_down(self, landmark_list, thumb_index_dist):      
        angle_ring_finger = (
            util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) < 50 and
            util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 90
        )
        return angle_ring_finger and thumb_index_dist > 100

    def scroll_up(self, landmark_list):
        thumb_up = landmark_list[4][1] < landmark_list[3][1] 
        pinky_up = landmark_list[20][1] < landmark_list[19][1]  

        index_down = landmark_list[8][1] > landmark_list[7][1]  
        middle_down = landmark_list[12][1] > landmark_list[11][1]  
        ring_down = landmark_list[16][1] > landmark_list[15][1] 

        return thumb_up and pinky_up and index_down and middle_down and ring_down 

    def all_fingers_up(self, landmark_list):
        return (
            util.get_angle(landmark_list[5], landmark_list[6], landmark_list[8]) > 60 and 
            util.get_angle(landmark_list[9], landmark_list[10], landmark_list[12]) > 60 and  
            util.get_angle(landmark_list[13], landmark_list[14], landmark_list[16]) > 60 and  
            util.get_angle(landmark_list[17], landmark_list[18], landmark_list[20]) > 60  and
            util.get_distance([landmark_list[4], landmark_list[5]]) < 50 
        )

    def release_resources(self):
        self.cap.release()