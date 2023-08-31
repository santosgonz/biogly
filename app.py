"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

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
    return render_template("details.html", user=user)

# def add_users():
#     name = request

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

@app.route("/<int:user_id>/edit/", methods = ["GET", "POST]"])
def edit_user(user_id):
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

@app.route("/<int:user_id>/edit/")
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)
