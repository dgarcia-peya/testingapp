from flask import Blueprint

ab_testing_tool = Blueprint('ab_testing_tool', __name__, template_folder='templates', url_prefix='/ab_testing',
                            static_folder='static')

from .views.list import *
from .views.detail import *
from .views.create import *
from .views.edit import *


@ab_testing_tool.route('/')
@login_required
def home_view():
    return render_template("ab_testing_tool/tool_home.html", view="home")
