# app/__init__.py
from flask import Flask
from flask_mysqldb import MySQL
from flask_mail import Mail
import secrets

# Initialize MySQL
mysql = MySQL()
mail = Mail()

def create_app():
    app = Flask(__name__)

    # Set the secret key
    app.config['SECRET_KEY'] = secrets.token_hex(16)

    # App configuration for MySQL (defaults, not used for dynamic switching)
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = ''
    app.config['MYSQL_DB'] = ''  # Leave empty; it will be set dynamically

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USERNAME'] = 'probaho.app@gmail.com'
    app.config['MAIL_PASSWORD'] = 'asrl enty bjks pxmm'
    app.config['MAIL_DEFAULT_SENDER'] = 'probaho.app@gmail.com'

    # Initialize MySQL and Mail with the app
    mysql.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.routes.auth import auth
    from app.routes.main import main
    from app.routes.dashboard import dashboard 
    from app.routes.category import category  # Register category blueprint
    from app.routes.products import products  # Register product blueprint
    from app.routes.pos import pos  # Import and register POS blueprint
    from app.routes.staff import staff


    app.register_blueprint(auth, url_prefix='/auth')  # Prefix for authentication routes
    app.register_blueprint(main)  # Register main blueprint without any prefix
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(category, url_prefix='/category')  # Register category blueprint
    app.register_blueprint(products, url_prefix='/products')  # Register product blueprint
    app.register_blueprint(pos, url_prefix='/pos')  # Register product blueprint
    app.register_blueprint(staff, url_prefix='/staff')

    return app
