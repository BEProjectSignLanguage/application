import mediapipe as mp
import cv2
import numpy as np

# Internal imports
from config import config

class PredictLandmarks:

    def __init__(self):
        self.mp_holistic = mp.solutions.holistic # Holistic model
        self.mp_drawing = mp.solutions.drawing_utils # Drawing utilities
        self.colors = [(245,117,16) for i in range(len(config["actions"]))]

    def get_holistic(self):
        return self.mp_holistic

    def mediapipe_detection(self, image, model):
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # COLOR CONVERSION BGR 2 RGB
        image.flags.writeable = False                  # Image is no longer writeable
        results = model.process(image)                 # Make prediction
        image.flags.writeable = True                   # Image is now writeable 
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR) # COLOR COVERSION RGB 2 BGR
        return results

    def draw_landmarks(self, image, results):
        self.mp_drawing.draw_landmarks(image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION) # Draw face connections
        self.mp_drawing.draw_landmarks(image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS) # Draw pose connections
        self.mp_drawing.draw_landmarks(image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS) # Draw left hand connections
        self.mp_drawing.draw_landmarks(image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS) # Draw right hand connections

    def draw_styled_landmarks(self, image, results):
        # Draw face connections
        # self.mp_drawing.draw_landmarks(
        #     image, results.face_landmarks, self.mp_holistic.FACEMESH_TESSELATION, 
        #     self.mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1), 
        #     self.mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
        # ) 
        # Draw pose connections
        self.mp_drawing.draw_landmarks(
            image, results.pose_landmarks, self.mp_holistic.POSE_CONNECTIONS,
            self.mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4), 
            self.mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
        ) 
        # Draw left hand connections
        self.mp_drawing.draw_landmarks(
            image, results.left_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
            self.mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4), 
            self.mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
        ) 
        # Draw right hand connections  
        self.mp_drawing.draw_landmarks(
            image, results.right_hand_landmarks, self.mp_holistic.HAND_CONNECTIONS, 
            self.mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4), 
            self.mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
        ) 

    def extract_keypoints(self, results):
        pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
        # face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
        lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
        rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
        return np.concatenate([pose, lh, rh])    

    def prob_viz(self, res, input_frame):
        output_frame = input_frame.copy()
        for num, prob in enumerate(res):
            cv2.rectangle(
                output_frame, 
                (0,60+num*40), 
                (
                    int(prob*100), 
                    90+num*40
                ), 
                self.colors[num], 
                -1
            )
            cv2.putText(
                output_frame, 
                config["actions"][num], 
                (0, 85+num*40), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (255,255,255), 
                2, 
                cv2.LINE_AA
            )            
        return output_frame