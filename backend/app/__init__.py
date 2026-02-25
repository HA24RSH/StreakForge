import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow all origins in production (safe for this project)
    CORS(app, supports_credentials=True)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import habit_bp
    app.register_blueprint(habit_bp)

    return app