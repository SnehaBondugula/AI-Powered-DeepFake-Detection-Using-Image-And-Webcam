# Utility functions can be added here if needed.
import cv2
import numpy as np
import base64

def decode_base64_image(image_data):
    """Decode a base64 image string into an OpenCV image."""
    try:
        header, encoded = image_data.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        print(f"Error decoding image: {str(e)}")
        return None


def resize_image(image, size=(224, 224)):
    """Resize image to the target size."""
    return cv2.resize(image, size)
