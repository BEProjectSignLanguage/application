import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Internal imports 
from config import config

class GestureInterpretation:

    def __init__(self, output_units):
        # Model architecture
        self.model = Sequential(
            [
                LSTM(
                    128, 
                    return_sequences=True, 
                    activation='relu', 
                    input_shape=(30,258)
                ),
                LSTM(
                    128, 
                    return_sequences=True, 
                    activation='relu'
                ),
                LSTM(
                    128, 
                    return_sequences=False, 
                    activation='relu'
                ),
                Dense(
                    128, 
                    activation='relu'
                ),
                Dense(
                    64, 
                    activation='relu'
                ),
                Dense(
                    output_units,
                    activation='softmax'
                )
            ]
        )
        # Model weights
        self.model.load_weights(
            config["interpretation_model_path"]
        )
    
    def predict(self, sequence):
        """
            Input   :   Sequence (frame buffer)
            Utility :   Predict gesture on last frame
            Output  :   Gesture (String)
        """
        result = self.model.predict(
            np.expand_dims(sequence, axis=0),
            verbose=0
        )[0]
        return result, np.argmax(result)