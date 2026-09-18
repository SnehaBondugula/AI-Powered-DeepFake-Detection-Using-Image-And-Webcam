from tensorflow.keras.models import load_model as keras_load_model
import os

def load_model():
    """Loads the trained model with error handling."""
    try:
        model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models', 'deepfake_model.h5')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        
        model = keras_load_model(model_path)
        print("Model loaded successfully.")
        return model

    except Exception as e:
        print(f"Error loading model: {str(e)}")
        return None
