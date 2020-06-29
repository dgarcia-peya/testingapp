import json
import requests
from flask import Blueprint, request, redirect, url_for, current_app, g
from flask_login import login_user, logout_user, login_required
from werkzeug.exceptions import Unauthorized

from DataAnalyticsToolkit.models.users import User

authentication = Blueprint('authentication', __name__)


@authentication.route("/login")
def login():
    """Prepare the Google OAuth request and redirect to it

    :return: Redirect object to Google OAuth
    """
    google_provider_cfg = requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    request_uri = g.client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@authentication.route("/login/callback")
def callback():
    """Receive the Google OAuth response and try to login user.

    :return: Rendered template
    """
    code = request.args.get("code")
    google_provider_cfg = requests.get(current_app.config["GOOGLE_DISCOVERY_URL"]).json()
    token_endpoint = google_provider_cfg["token_endpoint"]
    token_url, headers, body = g.client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config["GOOGLE_CLIENT_ID"], current_app.config["GOOGLE_CLIENT_SECRET"]),
    )
    g.client.parse_request_body_response(json.dumps(token_response.json()))
    user_info_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = g.client.add_token(user_info_endpoint)
    user_info_response = requests.get(uri, headers=headers, data=body)
    if user_info_response.json().get("email_verified") \
            and "hd" in user_info_response.json() \
            and user_info_response.json()["hd"] in current_app.config["SUPPORTED_LOGIN_DOMAINS"]:
        user_email = user_info_response.json()["email"]
    else:
        raise Unauthorized("User email not available or not verified.")

    user = User.query.get(user_email)

    login_user(user)

    return redirect(url_for('dashboard.home'))


@authentication.route("/logout")
@login_required
def logout():
    """Logout the user and redirect to Home Page

    :return: Redirection object to the Home Page
    """
    logout_user()
    return redirect(url_for("dashboard.home"))
