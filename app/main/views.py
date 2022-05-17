from flask import render_template, request, redirect, url_for, abort, flash
from . import main
from flask_login import login_required, current_user
from ..models import User, Post, Comment
from .forms import UpdateProfile, PostForm, CommentForm
from .. import db, photos
from ..request import get_quotes


@main.route('/')
def index():
    quote = get_quotes()
    return render_template('index.html', quote = quote)


@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)


@main.route('/user/<uname>/update/pic', methods=['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username=uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/post/new', methods=['GET', 'POST'])
@login_required
def post():
    """
    View Post function that returns the Post page and data
    """
    post_form = PostForm()

    if post_form.validate_on_submit():
        post_title = post_form.post_title.data
        description = post_form.description.data
        # user = current_user

        new_post = Post(post_title=post_title, description=description, author=current_user)
        db.session.add(new_post)
        db.session.commit()

        return redirect(url_for('main.all'))

    title = 'New Post | One Minute Pitch'
    return render_template('post.html', title=title, post_form=post_form)


@main.route('/Post/all', methods=['GET', 'POST'])
@login_required
def all():
    posts = Post.query.all()
    quote = get_quotes()
    return render_template('allpost.html', posts=posts, quote=quote)


@main.route('/view/<int:id>', methods=['GET', 'POST'])
@login_required
def view(id):
    post = Post.query.get_or_404(id)
    post_comments = Comment.query.filter_by(post_id=id).all()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment_form.comment.data, author=current_user)
        new_comment.save_comment()

    return render_template('view.html', post=post, post_comments=post_comments, comment_form=comment_form)


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    # flash('Your post has been deleted', 'successfully')
    return redirect(url_for('main.all'))


@main.route('/Update/<int:id>', methods=['GET', 'POST'])
@login_required
def update_post(id):
    post = Post.query.get_or_404(id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.post_title = form.post_title.data
        post.description = form.description.data
        db.session.commit()
        flash('Your post has been Updated', 'successfully')
        return redirect(url_for('main.all'))
    elif request.method == 'GET':
        form.post_title.data = post.post_title
        form.description.data = post.description
    return render_template('update_post.html', form=form)


@main.route('/comment/<int:id>', methods=['GET', 'POST'])
@login_required
def comment(id):
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        new_comment = Comment(post_id=id, comment=comment.form.data, author=current_user)
        new_comment.save_comment()

    return render_template('view.html', comment_form=comment_form)
