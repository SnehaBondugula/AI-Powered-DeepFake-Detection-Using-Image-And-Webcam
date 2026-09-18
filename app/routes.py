from flask import Blueprint, request, render_template, jsonify, url_for
from .model_loader import load_model
from .detect import detect_image
from .realtime_detection import detect_frame
import os
from werkzeug.utils import secure_filename
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Create the blueprint
main_blueprint = Blueprint('main', __name__)

# Lazy load the model to reduce startup time
model = None

def get_model():
    global model
    if model is None:
        model = load_model()
    return model

# Set the upload folder path (absolute path)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_FOLDER = os.path.join(base_dir, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Rate limiter to prevent abuse
limiter = Limiter(get_remote_address, default_limits=["10 per second"])

@main_blueprint.route('/')
@limiter.limit("5 per second")
def index():
    return render_template('index.html')

@main_blueprint.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template('index.html', error='No file uploaded.')

    file = request.files['file']
    
    if file.filename == '':
        return render_template('index.html', error='No file selected.')

    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        try:
            result = detect_image(filepath, get_model())
            if not result:
                return render_template('result.html', error='No face detected.')
            
            # Provide relative image URL for rendering
            image_url = url_for('static', filename=f'uploads/{filename}')
            
            return render_template('result.html', result=result, image_url=image_url)
        
        except Exception as e:
            return render_template('index.html', error=f'Error: {str(e)}')

@main_blueprint.route('/webcam', methods=['POST'])
@limiter.limit("10/second")  # Rate limit
def webcam():
    data = request.json
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400

    try:
        image_data = data['image']
        result = detect_frame(image_data, get_model())
        return jsonify({'result': result})

    except Exception as e:
        return jsonify({'error': f'Error processing frame: {str(e)}'}), 500
