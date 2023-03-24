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

class WebcamFeed:

    def __init__(self, app_reference):
        # Defining configuration for camera
        self.handler = None
         # Initialize empty occurence counter for voting
        self.occurence_counter = []
        self.keywords = []
        self.reset_occurence_counter()
        self.allow_inference = False
        self.gui_reference = app_reference
        self.signing_status = "Not Signing"
        self.sentence_display_start = None
        self.sentence_display_end = None        

    def update_signing_status(self, sentence):
        self.signing_status = sentence
        self.sentence_display_start = datetime.now()

    def set_inference_status(self, allowed):
        if allowed:
            self.signing_status = "Signing"
        else:
            self.signing_status = "Not Signing"
        self.allow_inference = allowed

    def reset_keywords(self):
        self.keywords = []

    def reset_occurence_counter(self):
        """
            Input   :   None
            Utility :   Get empty array for recording occurence
            Output  :   None
        """
        self.occurence_counter = [
            0 for i in range(len(config["actions"]))
        ]
        
    def run_feed(self):
        """
            Input   :   None
            Utility :   Capture video feed from camera
            Output  :   None
        """        
        # Defining constants
        frame_buffer = config["frame_buffer"]
        WIDTH = config["WIDTH"]
        HEIGHT = config["HEIGHT"]
        FPS = config["FPS"]
        actions = np.array(
            config["actions"]
        )
        interpretation_threshold = config["interpretation_threshold"]
        not_signing_interrupt_interval = config["not_signing_interrupt_interval"]

        # Initialize variable to record start point and end point of not signing
        start_not_signing = None
        end_not_signing = None

        # Initialize Inferencing components
        landmarkDetection = PredictLandmarks()
        gestureDetection = GestureDetection()
        gestureInterpretation = GestureInterpretation(
            output_units=actions.shape[0]
        )
        mp_holistic = landmarkDetection.get_holistic()

        # Defining camera self.handler    
        self.handler = cv2.VideoCapture(0)    
        self.handler.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.handler.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT) 
        
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
                    ret, frame = self.handler.read()                
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

                        # TODO : Uncomment further 2 lines to start gesture detection
                        # is_signing = gestureDetection.predict(keypoints)                      
                        # if is_signing and len(sequence) == frame_buffer:
                        # Run classification
                        if self.allow_inference and len(sequence) == frame_buffer:
                            result, max_index = gestureInterpretation.predict(
                                sequence=sequence
                            )       
                            # TODO : Uncomment and indent to Apply threshold on classification                        
                            # if result[max_index] > interpretation_threshold:                                                                          
                            # gesture = actions[max_index]
                            if max_index == 0:
                                if start_not_signing is None:
                                    start_not_signing = datetime.now()
                                    end_not_signing = datetime.now()
                                else:
                                    end_not_signing = datetime.now()
                                    # TODO  :   Implement thresholding logic
                                    delta = end_not_signing - start_not_signing
                                    if (delta.seconds + delta.microseconds * (10 ** -6)) >= not_signing_interrupt_interval:
                                        # print("Not signing threshold exceeded ", delta.seconds)
                                        maximum_occuring = np.argmax(self.occurence_counter)
                                        self.gui_reference.update_detection_label(actions[maximum_occuring])
                                        # print("Occurence counter : ", maximum_occuring)
                                        # Check most occurring
                                        if np.argmax(self.occurence_counter) != 0:   
                                            #   If sign is not detected already
                                            if actions[maximum_occuring] not in self.keywords:                                                                             
                                                self.keywords.append(actions[maximum_occuring])                                                
                                                start_not_signing = None
                                                end_not_signing = None                 
                                                # Refresh occurence counter
                                                self.reset_occurence_counter()                                                
                                                self.gui_reference.update_keywords_placeholder(self.keywords)
                            else:
                                # Update frequency
                                self.occurence_counter[max_index] += 1
                                maximum_occuring = np.argmax(self.occurence_counter)
                                self.gui_reference.update_detection_label(actions[maximum_occuring])
                            # frame = landmarkDetection.prob_viz(
                            #     res=result,
                            #     input_frame=frame,                    
                            # )                                
                        cv2.rectangle(
                            frame, 
                            (30, HEIGHT - 30),
                            (WIDTH - 30, HEIGHT - 120),
                            (252, 173, 3),
                            -1,                            
                        )    
                        cv2.putText(
                            frame, 
                            self.signing_status, 
                            (50, HEIGHT - 50), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            2, 
                            (255, 255, 255), 
                            2, 
                            cv2.LINE_AA
                        )         
                        if self.sentence_display_start:
                            self.sentence_display_end = datetime.now()
                            time_delta = self.sentence_display_end - self.sentence_display_start
                            #   IF sentence has been displayed for fixed time, replace status value
                            if(time_delta.seconds >= config["sentence_display_persistence"]):
                                self.signing_status = "Signing"          
                                self.sentence_display_start = None
                                self.sentence_display_end = None 
                        cam.send(frame)                
                        # cam.sleep_until_next_frame() 
                        # cv2.imshow("Feed", frame)
                    else:
                        print("Camera load failed")
                        break
                    if key == ord('q'):                        
                        break                    
                    # previous = now
                    
    def stop_feed(self):
        """
            Input   :   None
            Utility :   Stop camera feed access
            Output  :   None
        """
        # Release camera self.handler
        self.handler.release()
        # Destroy all created windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    webcam = WebcamFeed()

    webcam.run_feed()
            