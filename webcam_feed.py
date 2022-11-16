import cv2
import pyvirtualcam
import numpy as np

# Internal Imports
from gesture_detection import GestureDetection
from gesture_interpretation import GestureInterpretation
from landmark_detection import PredictLandmarks

# Parameters for camera inputs
WIDTH = 1920
HEIGHT = 1080
FPS = 60.0
fmt = pyvirtualcam.PixelFormat.BGR

def run_feed():
    """
        Input   :   None
        Utility :   Capture video feed from camera
        Output  :   None
    """
    # Defining constants
    frame_buffer = 30
    actions = np.array(
        [
            'allergy', 
            'emergency', 
            'hospital'
        ]
    )

    # Initialize Inferencing components
    landmarkDetection = PredictLandmarks()
    gestureDetection = GestureDetection()
    gestureInterpretation = GestureInterpretation(
        output_units=actions.shape[0]
    )
    mp_holistic = landmarkDetection.get_holistic()

    # Defining camera handler
    handler = cv2.VideoCapture(0)
    
    # Defining configuration for camera
    handler = cv2.VideoCapture(0)    
    handler.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    handler.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT) 
    sequence = []

    # Open mediapipe holistic
    with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
        # Open link to virtual camera
        with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=20, fmt=fmt) as cam: 
            # Run feed
            while True:
                gesture = ""
                ret, frame = handler.read()                
                key = cv2.waitKey(1)
                if ret:            
                    frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
                    landmarks = landmarkDetection.mediapipe_detection(
                        image=frame,
                        model=holistic
                    )
                    keypoints = landmarkDetection.extract_keypoints(
                        landmarks
                    )
                    
                    sequence.append(keypoints)
                    sequence = sequence[-30:]

                    # TODO : Replace "None" by landmarks
                    is_signing = gestureDetection.predict(keypoints)  
                    if is_signing and len(sequence) == frame_buffer:                        
                        # Run inferencing
                        result, max_index = gestureInterpretation.predict(
                            sequence=sequence
                        )            
                        gesture = actions[max_index]
                        frame = landmarkDetection.prob_viz(
                            res=result,
                            input_frame=frame,                    
                        )        
                    cv2.putText(
                        frame, 
                        gesture, 
                        (50, 50), 
                        cv2.FONT_HERSHEY_COMPLEX, 
                        2, 
                        (0, 0, 0), 
                        2, 
                        cv2.LINE_AA
                    )   
                    cam.send(frame)                
                    cam.sleep_until_next_frame() 
                    # cv2.imshow("Feed", frame)
                else:
                    print("Camera load failed")
                    break
                if key == ord('q'):
                    break
        handler.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    run_feed()
            