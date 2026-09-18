import cv2
import numpy as np

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


def detect_image(image_path, model):
    """Detect and classify faces in an image with confidence score."""
    try:
        image = cv2.imread(image_path)
        if image is None:
            return "Invalid or Unreadable Image"

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
            
            # Add confidence score to the result
            confidence = prediction if label == "Fake" else 1 - prediction
            results.append(f"{label} (Confidence: {confidence:.2f})")

        return results

    except Exception as e:
        return f"Error processing image: {str(e)}"
