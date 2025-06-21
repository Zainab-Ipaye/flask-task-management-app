from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
from flask import Flask

# Initialize core extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
talisman = Talisman()

# Define a secure Content Security Policy
csp = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "https://cdn.jsdelivr.net"],
    "style-src": ["'self'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
}


def create_test_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    # Use test config if provided (for unit tests)
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object("config.Config")

    # Initialize core app services
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Setup user login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    login_manager.login_view = "login.html"
    login_manager.login_message_category = "info"

    talisman.init_app(app, content_security_policy=csp, force_https=False)

    # User session loader
    from webapp.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from webapp import routes

    app.register_blueprint(routes.bp)

    return app
