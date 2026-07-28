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


@blueprint.get("/prototypes/calm-break")
def calm_break():
    if not current_app.config.get("ENABLE_PROTOTYPES", False):
        abort(404)
    response = make_response(render_template("prototype/calm_break.html"))
    response.headers["Cache-Control"] = "no-store"
    return response


@blueprint.get("/prototypes/school-support-share")
def school_support_share():
    if not current_app.config.get("ENABLE_PROTOTYPES", False):
        abort(404)
    response = make_response(render_template("prototype/school_support_share.html"))
    response.headers["Cache-Control"] = "no-store"
    return response
