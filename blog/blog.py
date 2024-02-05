import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from blog.db import get_db
from blog.auth import login_required


blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC').fetchall()

    return render_template('blog/index.html', posts=posts)



