import cv2
import pyvirtualcam

# Internal imports
from pose_estimation import PoseEstimation 
import numpy as np

# Parameters for camera inputs
WIDTH = 1920
HEIGHT = 1080
FPS = 60.0
fmt = pyvirtualcam.PixelFormat.BGR

# Parameters for camera inputs
WIDTH = 1920
HEIGHT = 1080
FPS = 1.0
text = ["Not Signing", "Signing"]

def main():
    """
        Input   :   None
        Utility :   Capture video feed from camera
        Output  :   None
    """
    # Initialize Pose Estimation model
    poseEstimation = PoseEstimation(FPS)

    # Defining camera handler
    handler = cv2.VideoCapture(0)
    
    # Defining configuration for camera
    handler = cv2.VideoCapture(0)    
    handler.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    handler.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT) 

    with pyvirtualcam.Camera(width=WIDTH, height=HEIGHT, fps=20, fmt=fmt) as cam: 
        # Run feed
        while True:
            ret, frame = handler.read()
            is_signing = np.argmax(poseEstimation.predict(frame))
            key = cv2.waitKey(1)
            if ret:            
                frame = cv2.resize(frame, (WIDTH, HEIGHT), interpolation=cv2.INTER_CUBIC)
                cv2.rectangle(
                    frame, 
                    (0, 960), 
                    (1920, 1080), 
                    (255, 255, 255), 
                    -1
                )           
                cv2.putText(
                    frame, 
                    text[is_signing], 
                    (50, 50), 
                    cv2.FONT_HERSHEY_COMPLEX, 
                    2, 
                    (0, 0, 0), 
                    2, 
                    cv2.LINE_AA
                )   
                cam.send(frame)                
                cam.sleep_until_next_frame() 
            else:
                print("Camera load failed")
                break
            if key == ord('q'):
                break
    handler.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
            