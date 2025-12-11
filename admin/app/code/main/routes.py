from flask import render_template, redirect, session
from . import bp
import config

@bp.route('/')
def index():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    return render_template("main.html", role = config.USERS_ROLES[session["user"]])