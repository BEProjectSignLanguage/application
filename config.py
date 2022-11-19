config = {
    # Camera parameters
    "WIDTH" : 1920,
    "HEIGHT" : 1080,
    "FPS" : 20,
    # Mediapipe thresholds
    "min_detection_confidence" : 0.5,
    "min_tracking_confidence" : 0.5,
    # Actions detected by inferencing model
    "actions" : [
        'allergy', 
        'emergency', 
        'hospital'
    ],
    "frame_buffer" : 30,
}
