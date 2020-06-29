from flask import render_template, request, make_response
from flask_login import login_required

from ...AB_Testing_Tool import ab_testing_tool
from ..models.ab_test_configs import ABTestConfig


@ab_testing_tool.route('/edit')
def edit_view():
    return render_template('ab_testing_tool/tool_home.html', view="edit")


@ab_testing_tool.route("/finish_ab_test", methods=['POST'])
@login_required
def finish_ab_test():
    """Marks a AB test as finished, updating the to_date, the result and explanation

    :return: Json object with the saving result
    """
    data = request.get_json()
    ab_test = ABTestConfig.get(data["ab_test_name"])

    result = ab_test.finish_test(
        data["ab_test_to_date"],
        data["ab_test_result"],
        data["ab_test_explanation"]
    )

    if result["error"]:
        return make_response({"error": result["message"]}, 400)
    else:
        return make_response({"error": False}, 200)
