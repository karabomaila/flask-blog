import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import abort
from blog.db import get_db
from blog.auth import login_required


blog_blueprint = Blueprint('blog', __name__)

@blog_blueprint.route('/')
def index():
    db = get_db()
    posts = db.execute('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id ORDER BY created DESC').fetchall()

    return render_template('blog/index.html', posts=posts)

@blog_blueprint.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Please add the blog title!"
        elif not body:
            error = "Please add the blog body!"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('INSERT INTO post (title, body, author_id) VALUES(?, ?, ?)', (title, body, g.user['id']))
            db.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post_by_id(id, check_author=True):
    db = get_db()
    post = db.execute('SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?', (id,)).fetchone()
    
    if post is None:
        abort(404, f"Post id {id} doesn't exist.")
    elif check_author and post['author_id'] != g.user['id']:
        abort(403, "You are not allowed to update the post.")

    return post

@blog_blueprint.route('/update/<int:id>', methods=('GET', 'POST'))
def update(id):
    post = get_post_by_id(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = "Please add the blog title!"
        elif not body:
            error = "Please add the blog body!"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute('UPDATE post SET title= ?, body= ? WHERE author_id= ?', (title, body, g.user['id']))
            db.commit()

            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@blog_blueprint.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    print(id)
    get_post_by_id(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id= ?', (id,))
    db.commit()

    return redirect(url_for('blog.index'))
