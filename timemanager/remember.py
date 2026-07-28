from __future__ import annotations

import sqlalchemy as sa
from flask import Blueprint, abort, flash, g, redirect, request, url_for

from .auth import login_required
from .db import get_db, local_installation_id, new_public_id
from .models import remember_items


blueprint = Blueprint("remember", __name__)

REMEMBER_ITEM_LIMIT = 3
REMEMBER_TITLE_LIMIT = 100


@blueprint.post("/remember")
@login_required
def create_item():
    title = " ".join(request.form.get("title", "").split())
    if not title:
        flash("Add a few words for the reminder.", "error")
        return redirect(url_for("tasks.today", _anchor="remember"))
    if len(title) > REMEMBER_TITLE_LIMIT:
        flash(
            f"Keep Remember items under {REMEMBER_TITLE_LIMIT} characters.",
            "error",
        )
        return redirect(url_for("tasks.today", _anchor="remember"))

    database = get_db()
    item_count = database.execute(
        sa.select(sa.func.count())
        .select_from(remember_items)
        .where(remember_items.c.user_id == g.user["id"])
    ).scalar_one()
    if item_count >= REMEMBER_ITEM_LIMIT:
        flash(
            "Remember can hold three items. Check one off before adding another.",
            "error",
        )
        return redirect(url_for("tasks.today", _anchor="remember"))

    database.execute(
        sa.insert(remember_items).values(
            public_id=new_public_id(),
            origin_installation_id=local_installation_id(database),
            user_id=g.user["id"],
            title=title,
        )
    )
    database.commit()
    return redirect(url_for("tasks.today", _anchor="remember"))


@blueprint.post("/remember/<int:item_id>/complete")
@login_required
def complete_item(item_id: int):
    database = get_db()
    deleted_id = database.execute(
        sa.delete(remember_items)
        .where(
            remember_items.c.id == item_id,
            remember_items.c.user_id == g.user["id"],
        )
        .returning(remember_items.c.id)
    ).scalar_one_or_none()
    if deleted_id is None:
        database.rollback()
        abort(404)
    database.commit()
    return redirect(url_for("tasks.today", _anchor="remember"))
