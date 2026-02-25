from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from .config import Config
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow local + production frontend
    allowed_origins = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        os.getenv("FRONTEND_URL")  # production URL
    ]

    CORS(app, origins=[origin for origin in allowed_origins if origin])

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import habit_bp
    app.register_blueprint(habit_bp)

    return app