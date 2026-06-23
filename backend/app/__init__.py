from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

mongo = PyMongo()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__,
                template_folder='../../frontend/templates',
                static_folder='../../frontend/static')
    
    from config import config
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    mongo.init_app(app)
    jwt.init_app(app)
    CORS(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.admin import admin_bp
    from app.routes.faculty import faculty_bp
    from app.routes.student import student_bp
    from app.routes.parent import parent_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(faculty_bp, url_prefix='/api/faculty')
    app.register_blueprint(student_bp, url_prefix='/api/student')
    app.register_blueprint(parent_bp, url_prefix='/api/parent')
    
    # Serve frontend
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('login.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        from flask import send_from_directory
        return send_from_directory('../../frontend/templates', path)
    
    return app
