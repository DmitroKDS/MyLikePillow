from flask import render_template, redirect, request, session
from . import bp
from .features import messages, messages_info
import config


@bp.route('/', methods=['GET'])
async def index():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    got_messages = await messages.get()

    return render_template('messages/index.html', messages=got_messages)


@bp.route('/status_edit/<int:id>/<int:status>', methods=['POST'])
async def edit_status(id: int, status: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await messages.edit_status(id, status, config.USERS_NAMES[session["user"]])

    return redirect("/messages/")


@bp.route('/info/<int:id>/', methods=['GET'])
async def info(id: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    got_info = await messages_info.get(id)

    return render_template('messages/info.html', info=got_info)


@bp.route('/info/<int:id>/status_edit/<int:status>', methods=['POST'])
async def info_edit_status(id: int, status: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await messages.edit_status(id, status, config.USERS_NAMES[session["user"]])

    return redirect(f"/messages/info/{id}")


@bp.route('/info/<int:id>/add_comment', methods=['POST'])
async def add_comment(id: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await messages_info.add_comment(id, request.form.get('comment'), config.USERS_NAMES[session["user"]])

    return redirect(f"/messages/info/{id}/")


@bp.route('/info/<int:id>/delete_comment/<int:index>', methods=['POST'])
async def delete_comment(id: int, index: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await messages_info.delete_comment(id, index, config.USERS_NAMES[session["user"]])

    return redirect(f"/messages/info/{id}/")