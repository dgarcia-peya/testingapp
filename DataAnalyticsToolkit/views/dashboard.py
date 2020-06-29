from flask import Blueprint, redirect, request, url_for, render_template
from flask.views import View
from flask_login import current_user, login_required
from markupsafe import Markup

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/')
def home():
    """Tool Home Page: Shows a welcome message and login access

    :return: Redirect object or Rendered Template
    """
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.dashboard_panel"))
    else:
        return render_template("home.html", request_path=request.path)


@dashboard.route('/dashboard')
@login_required
def dashboard_panel():
    """User Dashboard: Get access to the user tools and last activity

    :return: Rendered template
    """
    return render_template('dashboard.html', user=current_user)


class DetailView(View):
    decorators = [login_required]

    id = ""

    @property
    def template_name(self):
        return 'detail.html'

    @property
    def object(self):
        return {}

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def dispatch_request(self, id):
        self.id = id
        context = {'object': self.object}
        return self.render_template(context)


class ListView(View):
    decorators = [login_required]

    @property
    def template_name(self):
        return 'list.html'

    @property
    def actions(self):
        return []

    @property
    def objects(self):
        return []

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def dispatch_request(self):
        context = {'objects': self.objects, 'actions': self.actions}
        return self.render_template(context)


class CreateView(View):
    decorators = [login_required]

    @property
    def template_name(self):
        return 'create.html'

    @property
    def form(self):
        return {}

    def render_template(self, context):
        return render_template(self.template_name, **context)

    def dispatch_request(self):
        context = {'form': self.form}
        return self.render_template(context)


@dashboard.app_template_filter()
def form_field(field):

    required = ""
    if "required" in field and field['required']:
        required = "required"

    read_only = ""
    if "read_only" in field and field['read_only']:
        read_only = "readonly"

    if field["type"] == "select":
        field_html = select_field(field, required)
    elif field["type"] == "multiple":
        field_html = multiple_field(field, required)
    elif field["type"] == "textarea":
        field_html = text_area_field(field, required, read_only)
    elif field["type"] == "checkbox":
        field_html = checkbox_field(field, required)
    elif field["type"] == "date":
        field_html = date_field(field, required)
    else:
        field_html = text_field(field, required, read_only)

    return Markup(field_html)


def text_field(field, required, read_only):
    return f"<input type='text' name='{ field['name'] }' id='{ field['name'] }' { required } { read_only } />"


def text_area_field(field, required, read_only):
    return f"<textarea name='{ field['name'] }' id='{ field['name'] }' { required } { read_only }></textarea>"


def checkbox_field(field, required):
    return f"<input type='checkbox' name='{ field['name'] }' id='{ field['name'] }' { required } />"


def date_field(field, required):
    return f"<input type='text' name='{ field['name'] }' id='{ field['name'] }'" \
           f"data-provide='datepicker' data-date-format='yyyy-mm-dd' data-date-autoclose='true' { required} />"


def select_field(field, required):
    field_html = f"<select name='{ field['name'] }' id='{ field['name'] }'"
    if "is_parent" in field and field["is_parent"]:
        field_html += f" onchange='getNestedOptions(\"{ field['child_options_endpoint']}\"," \
                      f"\"{ field['name'] }\", \"{ field['child'] }\")'"
    elif "on_change" in field:
        field_html += f" onchange='{ field['on_change'] }(\"{ field['name'] }\")'"
    field_html += f" { required } >"
    if "include_empty" in field and field["include_empty"]:
        field_html += f"<option value=''></option>"
    for option in field["options"]:
        field_html += f"<option value='{ option[0] }'>{ option[1] }</option>"
    field_html += "</select>"
    return field_html


def multiple_field(field, required):
    field_html = f"<select name='{ field['name'] }' id='{ field['name'] }' multiple {required} >"
    if "include_empty" in field and field["include_empty"]:
        field_html += f"<option value=''></option>"
    for option in field["options"]:
        field_html += f"<option value='{ option[0] }'>{ option[1] }</option>"
    field_html += "</select>"
    return field_html
