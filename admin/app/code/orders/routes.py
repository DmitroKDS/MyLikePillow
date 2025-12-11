from flask import render_template, redirect, request, session
from . import bp
from .features import orders, orders_info
import config

@bp.route('/', methods=['GET'])
async def index():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")

    got_orders = await orders.get()

    return render_template('orders/index.html', orders=got_orders)


@bp.route('/status_edit/<int:id>/<int:status>', methods=['POST'])
async def edit_status(id: int, status: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await orders.edit_status(id, status, config.USERS_NAMES[session["user"]])

    return redirect("/orders/")


@bp.route('/info/<int:id>/', methods=['GET'])
async def info(id: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    got_info = await orders_info.get(id)

    return render_template('orders/info.html', info=got_info)


@bp.route('/info/<int:id>/status_edit/<int:status>', methods=['POST'])
async def info_edit_status(id: int, status: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await orders.edit_status(id, status, config.USERS_NAMES[session["user"]])

    return redirect(f"/orders/info/{id}")


@bp.route('/info/<int:id>/add_comment', methods=['POST'])
async def add_comment(id: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await orders_info.add_comment(id, request.form.get('comment'), config.USERS_NAMES[session["user"]])

    return redirect(f"/orders/info/{id}/")


@bp.route('/info/<int:id>/delete_comment/<int:index>', methods=['POST'])
async def delete_comment(id: int, index: int):
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await orders_info.delete_comment(id, index, config.USERS_NAMES[session["user"]])

    return redirect(f"/orders/info/{id}/")