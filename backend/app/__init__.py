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

    CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes import habit_bp
    app.register_blueprint(habit_bp)

    return app