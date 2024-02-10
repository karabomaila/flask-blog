import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from blog.db import get_db

blueprint = Blueprint('auth', __name__, url_prefix="/auth")

@blueprint.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."

        if error is None:
            db = get_db()
            try:
                db.execute("INSERT INTO user (username, password) VALUES(?, ?)",
                           (username, generate_password_hash(password)),)
                db.commit()
            except db.IntegrityError:
                error = f"Error saving your details! User {username} is already registered."
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@blueprint.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        if not username:
            error = "Username is required"
        elif not password:
            error = "Username is required"

        db = get_db()
        user = db.execute("SELECT * FROM user WHERE username=?", (username,)).fetchone()

        if user is None:
            error = f"The username {username} is not found."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('index'))

        flash(error)
    return render_template('auth/login.html')

@blueprint.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

"""
@blueprint.errorhandler(404)
def error(error):
    return render_template('auth/error.html'), 404"""

# adds the function that runs before each view function.
@blueprint.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()

# authenticate the other views and requre login of some endpoints. 
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)
    
    return wrapped_view