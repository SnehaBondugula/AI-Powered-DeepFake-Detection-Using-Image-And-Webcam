import cv2
import numpy as np
import base64

def detect_faces(image):
    """Detect faces using OpenCV's Haar cascade classifier."""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    
    if len(faces) == 0:
        return []

    # Return all detected faces
    face_images = [image[y:y + h, x:x + w] for (x, y, w, h) in faces]
    return face_images


def detect_frame(image_data, model):
    """Detect and classify faces from real-time frames with confidence score."""
    try:
        header, encoded = image_data.split(",", 1)
        img_bytes = base64.b64decode(encoded)
        nparr = np.frombuffer(img_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return "Invalid Frame"

        faces = detect_faces(image)

        if len(faces) == 0:
            return "No Face Detected"

        results = []

        for face in faces:
            face = cv2.resize(face, (224, 224))
            face = face.astype("float") / 255.0
            face = np.expand_dims(face, axis=0)

            prediction = model.predict(face)[0][0]
            label = "Fake" if prediction > 0.5 else "Real"
            
            # Add confidence score
            confidence = prediction if label == "Fake" else 1 - prediction
            results.append(f"{label} (Confidence: {confidence:.2f})")

        return results

    except Exception as e:
        return f"Error processing frame: {str(e)}"
