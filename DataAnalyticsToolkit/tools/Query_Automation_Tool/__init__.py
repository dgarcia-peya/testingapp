from flask import Blueprint, render_template

query_automation_tool = Blueprint('query_automation_tool',
                                  __name__,
                                  template_folder='templates',
                                  url_prefix='/query_automation',
                                  static_folder='static')

from .views.list import *
from .views.detail import *
from .views.create import *


@query_automation_tool.route('/')
@login_required
def home_view():
    return render_template("query_automation_tool/tool_home.html", view="home")
