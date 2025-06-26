from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
import os

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


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    if test_config:
        app.config.update(test_config)

    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Enable CSRF protection
    csrf.init_app(app)

    # Initialize core app services
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Setup user login manager
    login_manager = LoginManager()
    login_manager.init_app(app)

    # Security Headers via Flask-Talisman
    if os.environ.get("FLASK_ENV") == "development":
        talisman.init_app(app, content_security_policy=csp, force_https=False)
    else:
        talisman.init_app(
            app,
            content_security_policy=csp,
            force_https=True,
            strict_transport_security=True,
            session_cookie_secure=True,
            frame_options="DENY",
        )

    # User session loader
    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from webapp import routes

    app.register_blueprint(routes.bp)

    # Custom error pages
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    return app
