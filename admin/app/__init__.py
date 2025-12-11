import logging.handlers
from flask import Flask
import logging

def create_app() -> Flask:
    """
    This function create app and register all blueprints
    And return fully configured app
    """

    # Create Flask app instance

    app = Flask(__name__)
    app.secret_key = 'secret_key'

    # Logger

    log_formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    file_handler = logging.handlers.RotatingFileHandler(
        "app.log", maxBytes=1024 * 1024 * 5, backupCount=3
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_formatter)

    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)


    # Register blueprints

    from .code.login import bp as login_bp
    app.register_blueprint(login_bp, url_prefix = "/")

    from .code.main import bp as main_bp
    app.register_blueprint(main_bp, url_prefix = "/main")

    from .code.channels import bp as channels_bp
    app.register_blueprint(channels_bp, url_prefix = "/channels")

    from .code.contacts import bp as contacts_bp
    app.register_blueprint(contacts_bp, url_prefix = "/contacts")

    from .code.messages import bp as messages_bp
    app.register_blueprint(messages_bp, url_prefix = "/messages")


    from .code.orders import bp as orders_bp
    app.register_blueprint(orders_bp, url_prefix = "/orders")

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application</h1>'

    return app