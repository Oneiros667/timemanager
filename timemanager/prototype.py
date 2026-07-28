from __future__ import annotations

from flask import Blueprint, abort, current_app, make_response, render_template


blueprint = Blueprint("prototype", __name__)


@blueprint.get("/prototypes/complex-work")
def complex_work():
    if not current_app.config.get("ENABLE_PROTOTYPES", False):
        abort(404)
    response = make_response(render_template("prototype/complex_work.html"))
    response.headers["Cache-Control"] = "no-store"
    return response
