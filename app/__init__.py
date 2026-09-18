import os
from flask import Flask
from flask_cors import CORS

# Determine the base directory (the project root)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define absolute paths for templates and static folders
template_path = os.path.join(base_dir, 'templates')
static_path = os.path.join(base_dir, 'static')

# Initialize Flask app
app = Flask(__name__, template_folder=template_path, static_folder=static_path)

# Apply configuration settings
app.config.from_object('config.Config')

# Enable CORS
CORS(app)

# Import and register the blueprint
from .routes import main_blueprint, limiter
limiter.init_app(app)
app.register_blueprint(main_blueprint)
