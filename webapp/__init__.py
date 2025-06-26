from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_talisman import Talisman
from dotenv import load_dotenv
import os

# Initialize core extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
csrf = CSRFProtect()
talisman = Talisman()

from webapp.models import User

# Define Content Security Policy (CSP)
csp = {
    "default-src": ["'self'"],
    "script-src": ["'self'", "https://cdn.jsdelivr.net"],
    "style-src": ["'self'", "https://cdn.jsdelivr.net", "https://fonts.googleapis.com"],
    "font-src": ["'self'", "https://fonts.gstatic.com"],
}

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object("config.Config")

    if test_config:
        app.config.update(test_config)

    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

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

    # Login manager setup
    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    from webapp import routes

    app.register_blueprint(routes.bp)

    # Error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errors/500.html"), 500

    # Create database tables and create admin user if not exist
    with app.app_context():
        db.create_all()

        admin_username = os.environ.get("ADMIN_USERNAME")
        admin_email = os.environ.get("ADMIN_EMAIL")
        admin_password = os.environ.get("ADMIN_PASSWORD")

        if admin_username and admin_email and admin_password:
            admin = User.query.filter_by(role="admin").first()
            if not admin:
                hashed_pw = bcrypt.generate_password_hash(admin_password).decode(
                    "utf-8"
                )
                admin_user = User(
                    username=admin_username,
                    email=admin_email,
                    password=hashed_pw,
                    role="admin",
                )
                db.session.add(admin_user)
                db.session.commit()
                print("Admin user created.")
            else:
                print("Admin user already exists.")

    return app
