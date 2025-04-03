# run.py
from app import create_app

app = create_app()

app.config['UPLOAD_FOLDER'] = 'app/static/images/userimage'

if __name__ == "__main__":
    app.run(debug=True)