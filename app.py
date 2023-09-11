"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Posts, Tag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
DEBUG_TB_INTERCEPT_REDIRECTS = False

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

@app.route("/users", methods = ["GET", "POST"])
def users():
    # Show list of users in database
    users = User.query.all()
    return render_template('list.html', users = users)

@app.route("/<int:user_id>")
def show_user(user_id):
    user = User.query.get(user_id)
    posts = Posts.query.filter_by(user_id=user_id).all()
    return render_template("details.html", user=user, posts=posts)



@app.route("/create_form", methods=["GET"])
def create_form():
    return render_template("create_user.html")


@app.route("/create_user", methods=["POST"])
def create_user():
    first_name = request.form.get("enter_first")
    last_name = request.form.get("enter_last")
    image_url = request.form.get("img_url")

    if not first_name or not last_name:
        return "Error: First name or Last name missing", 400

    new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users") 

@app.route("/<int:user_id>/edit/", methods = ["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        user = User.query.get_or_404(user_id)
        first_name = request.form.get("enter_first")
        last_name = request.form.get("enter_last")
        image_url = request.form.get("img_url")

        if not first_name or not last_name:
            return "Error: First name or Last name missing", 400

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/users")
    else:
        user = User.query.get_or_404(user_id)
        return render_template("edit_user.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_delete(user_id):

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/new', methods = ["GET"])
def post(user_id):
    tags = Tag.query.all()
    print (tags)
    return render_template("user_post.html", tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods = ["POST"])
def post_print(user_id):
    title = request.form.get("enter_post")
    content = request.form.get("enter_content")
    tag_id = request.form.get("tag")
    print_post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(print_post)
    if tag_id:
        tag = Tag.query.get(tag_id)
        if tag:
            print_post.tags.append(tag)
    
    db.session.commit()

    return redirect("/users")

@app.route('/users/<int:user_id>/posts/<int:post_id>', methods = ["GET"])
def created_posts(user_id, post_id):
    user = User.query.get_or_404(user_id)
    posts = Posts.query.get_or_404(post_id)
    tags = posts.tags
    return render_template('created_posts.html', posts=posts, user=user, tags=tags)

@app.route ('/users/<int:user_id>/posts/<int:post_id>/edit', methods = ["GET"])
def edit_post(user_id, post_id):
    
    return render_template('edit_post.html')

@app.route ('/users/<int:user_id>/posts/<int:post_id>/edit', methods = ["POST"])
def post_edit(user_id, post_id):

    user = User.query.get_or_404(user_id)
    posts = Posts.query.get_or_404(post_id)
    posts.title = request.form.get( "edit_title")
    posts.content = request.form.get("edit_content")
    db.session.commit()
    return render_template('created_posts.html',  posts=posts, user=user)

@app.route('/users/<int:user_id>/<int:post_id>/delete', methods=["POST"])
def posts_delete(user_id, post_id):

    user = User.query.get_or_404(user_id)
    post = Posts.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")

@app.route('/tags/new', methods = ["GET"])
def tag_tag():

    return render_template("user_tag.html")

@app.route('/tags/new', methods = ["POST"])
def tags_print():
    tag_test = request.form.get("enter_tag")
    tag = Tag(tags=tag_test)

    db.session.add(tag)
    db.session.commit()

    return redirect("/users")

@app.route ('/tag/<int:tag_id>/edit', methods = ["GET"])
def edit_tag(tag_id):
    
    tags = Tag.query.all()
    return render_template('edit_tag.html', tags=tags)

@app.route ('/tag/<int:tag_id>/edit', methods = ["POST"])
def post_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.tags = request.form.get("edit_tag")
    db.session.commit()
    return render_template('edit_tag.html',  tag=tag)

# @app.route ('/tags/<int:tag_id>', methods = "GET")
# def show_tags(tag_id):

#     return render_template('tags.html')

@app.route("/tags")
def show_tag():

    tags = Tag.query.all()
    return render_template("tag_details.html", tags=tags)

@app.route("/tags/<int:tag_id>")
def show_tag_posts(tag_id):
    tag = Tag.query.get_or_404(tag_id)  # Changed to 'tag'
    print(f"Tag: {tag}")  # Debug print statement
    posts = tag.posts
    users = {post.id: User.query.get(post.user_id) for post in posts}
    print(f"Posts: {posts}")  # Debug print statement
    return render_template('lol.html', tag=tag, posts=posts, users=users)  # Changed to 'tag'



