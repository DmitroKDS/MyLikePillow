from flask import render_template, redirect, session
from . import bp
from .features import contacts
import config


@bp.route('/', methods=['GET'])
async def index():
    if session.get("user", None) not in config.USERS_NAMES:
        return redirect("/")
    
    got_contacts = await contacts.get()

    return render_template('contacts/index.html', contacts=got_contacts)