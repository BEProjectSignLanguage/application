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
        'not signing',
        'blood',
        'medicine',
        'allergy', 
        'emergency', 
        'hospital'
    ],
    # Specifics for detection model
    "detection_model_path" : "./models/detections.h5",
    # Specifics for interpretation model
    "frame_buffer" : 30,
    "interpretation_model_path" : "./models/interpretation.h5",
}
