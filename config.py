import os

class Config:
    # Use environment variables for security
    SECRET_KEY = os.getenv('SECRET_KEY', 'fallback_key')
    
    # Dynamic path for upload folder
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
