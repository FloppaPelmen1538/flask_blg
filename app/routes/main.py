from flask import Blueprint, render_template
from app.models import Post

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    posts = Post.query.order_by(Post.created_at.desc()).limit(10).all()
    return render_template("index.html", posts=posts)


@main_bp.route("/about")
def about():
    return render_template("about.html")
