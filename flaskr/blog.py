from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('blog', __name__)


@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', posts=posts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')


@bp.route('/<int:id>/createComment', methods=('GET', 'POST'))
@login_required
def createComment(id):
    post = get_post(id)

    if request.method == 'POST':
        comment = request.form['comment']
        error = None

        if not comment:
            error = 'Comment is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (comment, post_id, author_id)'
                ' VALUES (?, ?, ?)',
                (comment, post['id'], g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/createComment.html', post=post)


def get_post(id):
    post = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, f"Post id {id} doesn't exist.")

    return post

def get_comment(id):
    comment = get_db().execute(
        'SELECT c.id, comment, post_id, created, author_id, username'
        ' FROM comment c JOIN user u ON c.author_id = u.id'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE c.id = ?',
        (id,)
    ).fetchone()

    if comment is None:
        abort(404, f"Comment id {id} doesn't exist.")

    return comment

def get_comments(id):
    db = get_db()
    comments = db.execute(
        'SELECT c.id, comment, c.post_id, c.created, c.author_id, username'
        ' FROM comment c JOIN user u on c.author_id = u.id'
        ' WHERE c.post_id = ?'
        ' ORDER BY c.created DESC',
        (id,)
    ).fetchall()

    return comments


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)


@bp.route('/<int:id>/viewPost')
def viewPost(id):
    post = get_post(id)
    comments = get_comments(id)
    return render_template('blog/viewPost.html', post=post, comments=comments)



@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))
