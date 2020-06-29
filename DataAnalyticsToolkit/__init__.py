from flask import Flask, g, redirect, url_for, make_response, render_template
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient

from DataAnalyticsToolkit.models.users import User

from DataAnalyticsToolkit.views.authentication import authentication
from DataAnalyticsToolkit.views.dashboard import dashboard


def create_app():
    """App Factory: Instance the Flask application, login, blueprints, etc

    :return: Flask App Instance
    """

    app = Flask(__name__, template_folder='templates')
    app.config.from_object('DataAnalyticsToolkit.config')
    app.secret_key = app.config["APP_SECRET_KEY"]
    configure_error_handlers(app)

    initialize_login(app)

    register_blueprints(app)

    from DataAnalyticsToolkit.tools.AB_Testing_Tool import ab_testing_tool
    app.register_blueprint(ab_testing_tool)

    from DataAnalyticsToolkit.tools.Query_Automation_Tool import query_automation_tool
    app.register_blueprint(query_automation_tool)

    return app


def register_blueprints(app):
    """Register main app blueprints

    :param app: Flask application instance
    :return: Void
    """
    app.register_blueprint(dashboard)
    app.register_blueprint(authentication)


def initialize_login(app):
    """Login Manager initialization: This method creates the Login Manager Instance and set the login handlers

    :param app: Flask application instance
    :return: Void
    """

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get(user_id)

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        return redirect(url_for("dashboard.home"))

    client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])

    @app.before_request
    def before_request():
        g.client = client


def configure_error_handlers(app):
    """Defines the error routes and responses

    :param app: Flask application instance
    :return: Void
    """

    @app.errorhandler(400)
    def bad_request(error):
        """Bad request."""
        return make_response(render_template("http_error.html", error=error), error.code)

    @app.errorhandler(404)
    def not_found(error):
        """Page not found."""
        return make_response(render_template("http_error.html", error=error), error.code)

    @app.errorhandler(500)
    def server_error(error):
        """Internal server error."""
        return make_response(render_template("http_error.html", error=error), error.code)


if __name__ == '__main__':
    app_instance = create_app()
    app_instance.run()
