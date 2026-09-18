from app import app
import os

if __name__ == "__main__":
    # Use environment variable to control debug mode
    debug_mode = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    app.run(debug=debug_mode)
