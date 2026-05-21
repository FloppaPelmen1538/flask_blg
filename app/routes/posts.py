from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user

from app import db
from app.models import Post
from app.forms import PostForm

posts_bp = Blueprint("posts", __name__)


@posts_bp.route("/")
def list_posts():
    page = request.args.get("page", 1, type=int)
    pagination = Post.query.order_by(Post.created_at.desc()).paginate(
        page=page, per_page=6, error_out=False
    )
    return render_template(
        "posts/list.html", posts=pagination.items, pagination=pagination
    )


@posts_bp.route("/<int:post_id>")
def detail(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    return render_template("posts/detail.html", post=post)


@posts_bp.route("/new", methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data.strip(),
            body=form.body.data.strip(),
            author=current_user,
        )
        db.session.add(post)
        db.session.commit()
        flash("Запись успешно создана!", "success")
        return redirect(url_for("posts.detail", post_id=post.id))
    return render_template("posts/edit.html", form=form, title="Новая запись")


@posts_bp.route("/<int:post_id>/edit", methods=["GET", "POST"])
@login_required
def edit(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    if post.author != current_user:
        abort(403)

    form = PostForm(obj=post)
    if form.validate_on_submit():
        post.title = form.title.data.strip()
        post.body = form.body.data.strip()
        db.session.commit()
        flash("Запись обновлена.", "success")
        return redirect(url_for("posts.detail", post_id=post.id))

    return render_template("posts/edit.html", form=form, title="Редактировать запись")


@posts_bp.route("/<int:post_id>/delete", methods=["POST"])
@login_required
def delete(post_id):
    post = db.session.get(Post, post_id)
    if post is None:
        abort(404)
    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Запись удалена.", "info")
    return redirect(url_for("auth.profile"))
