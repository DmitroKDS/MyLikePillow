from flask import render_template, redirect, request, session
from . import bp
from .features import channels
import config


@bp.route('/', methods=['GET'])
async def index():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    got_channels = await channels.get()

    return render_template('channels/index.html', channels=got_channels)

@bp.route('/add', methods=['POST'])
async def add():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    await channels.add(request.form['name'])

    return redirect('/channels')