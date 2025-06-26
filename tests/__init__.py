from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_talisman import Talisman

# Initialize extensions without app
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
talisman = Talisman()
login_manager = LoginManager()

# Define your Content Security Policy here if needed
csp = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "https://cdn.jsdelivr.net"],
    "style-src": ["'self'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
}


def create_test_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Override config with test_config if provided
    if test_config:
        app.config.update(test_config)

    # Initialize extensions with app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    talisman.init_app(app, content_security_policy=csp, force_https=False)

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message_category = "info"

    # Import models here to avoid circular import issues
    from webapp.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints here
    from webapp.routes import bp

    app.register_blueprint(bp)

    return app
