import cv2
import pyvirtualcam
import numpy as np
from datetime import datetime

# Internal Imports
from config import config
from gesture_detection import GestureDetection
from gesture_interpretation import GestureInterpretation
from landmark_detection import PredictLandmarks

# Defining format for virtual camera input
fmt = pyvirtualcam.PixelFormat.BGR

# Defining configuration for camera
handler = None

def run_feed():
    """
        Input   :   None
        Utility :   Capture video feed from camera
        Output  :   None
    """
    global handler
    # Defining constants
    frame_buffer = config["frame_buffer"]
    WIDTH = config["WIDTH"]
    HEIGHT = config["HEIGHT"]
    FPS = config["FPS"]
    actions = np.array(
        config["actions"]
    )
    interpretation_threshold = config["interpretation_threshold"]
    previous = None
    now = None

    # Initialize Inferencing components
    landmarkDetection = PredictLandmarks()
    gestureDetection = GestureDetection()
    gestureInterpretation = GestureInterpretation(
        output_units=actions.shape[0]
    )
    mp_holistic = landmarkDetection.get_holistic()

    # Defining camera handler
    # handler = cv2.VideoCapture(0)
    handler = cv2.VideoCapture(0)    
    handler.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    handler.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT) 
    
    sequence = []

    # Open mediapipe holistic
    with mp_holistic.Holistic(
        min_detection_confidence=config["min_detection_confidence"],
        min_tracking_confidence=config["min_tracking_confidence"]
    ) as holistic:
        # Open link to virtual camera
        with pyvirtualcam.Camera(
            width=WIDTH, 
            height=HEIGHT, 
            fps=FPS, 
            fmt=fmt
        ) as cam: 
            # Run feed
            while True:
                now = datetime.now()
                gesture = ""
                ret, frame = handler.read()                
                key = cv2.waitKey(1)
                if ret:            
                    frame = cv2.resize(
                        frame, 
                        (WIDTH, HEIGHT), 
                        interpolation=cv2.INTER_CUBIC
                    )
                    landmarks = landmarkDetection.mediapipe_detection(
                        image=frame,
                        model=holistic
                    )
                    keypoints = landmarkDetection.extract_keypoints(
                        landmarks
                    )
                
                    sequence.append(keypoints)
                    sequence = sequence[
                        -1 * frame_buffer:
                    ]

                    # TODO : Replace "None" by landmarks
                    is_signing = gestureDetection.predict(keypoints)                      
                    if is_signing and len(sequence) == frame_buffer:
                        # Run classification
                        result, max_index = gestureInterpretation.predict(
                            sequence=sequence
                        )       
                        # Apply threshold on classification
                        if result[max_index] > interpretation_threshold:   
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
                    # if previous is not None:
                    #     delta = now - previous
                    #     seconds = delta.seconds + delta.microseconds * (10 ** -6)
                    #     cv2.putText(
                    #         frame, 
                    #         f"FPS : {1/seconds}", 
                    #         (50, 300), 
                    #         cv2.FONT_HERSHEY_COMPLEX, 
                    #         2, 
                    #         (0, 0, 0), 
                    #         2, 
                    #         cv2.LINE_AA
                    #     )                      
                    cam.send(frame)                
                    cam.sleep_until_next_frame() 
                    # cv2.imshow("Feed", frame)
                else:
                    print("Camera load failed")
                    break
                if key == ord('q'):
                    break
                # previous = now
                
def stop_feed():
    """
        Input   :   None
        Utility :   Stop camera feed access
        Output  :   None
    """
    # Release camera handler
    handler.release()
    # Destroy all created windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    run_feed()
            