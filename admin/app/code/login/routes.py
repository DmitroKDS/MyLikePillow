from flask import render_template, request, redirect, session
from . import bp
import config


@bp.route('/', methods=['GET', 'POST'])
async def index():
    if session.get("user", None) in config.USERS_NAMES:
        return redirect("/main")

    if request.method == 'POST':
        username, password = request.form.get('username'), request.form.get('password')
        user = config.USERS.get((username, password), None)

        if user == None:
            return render_template('login/index.html', error=1)

        session["user"] = user

        return redirect("/")
    
    return render_template('login/index.html', error=0)