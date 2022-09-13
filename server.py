"""Flask server for diary card app."""

from flask import Flask, session, request, flash, render_template, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Render homepage."""

    if session.get('user_id'):
        return redirect("/dashboard")

    return render_template("login.html")


@app.route('/login')
def login():
    """Log user in."""

    email = request.args.get("email")
    password = request.args.get("password")

    user = crud.get_user_by_email(email)
    print(user)
    print(email)

    if user and user.password == password:
        session["user_id"] = user.user_id
        flash("Successfully logged in")
        return redirect("/dashboard")

    else:
        flash("Incorrect email or password")
        return redirect("/")


@app.route("/create-account")
def create_account_form():
    """Render create account page."""
    
    return render_template("create-account.html")


@app.route("/create-account", methods=["POST"])
def create_account():
    """Create new account."""

    return "Info received"


@app.route("/dashboard")
def dashboard():
    """Render dashboard."""

    return "This is a dashboard"


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///test-db")
    app.run(host="0.0.0.0", debug=True)
