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
    
    if session.get('user_id'):
        return redirect("/dashboard")
    
    return render_template("create-account.html")


@app.route("/create-account", methods=["POST"])
def create_account():
    """Create new account."""

    # TODO add email validation

    email = request.form.get("email")
    password = request.form.get("password")
    phone_number = request.form.get("phone-number")
    entry_reminders = request.form.get("entry-reminders")
    med_tracking = request.form.get("med-tracking")
    med_reminders = request.form.get("med-reminders")

    entry_reminders = convert_radio_to_bool(entry_reminders)
    med_tracking = convert_radio_to_bool(med_tracking)
    med_reminders = convert_radio_to_bool(med_reminders)

    if not crud.get_user_by_email(email):
        new_user = crud.create_user(email, password, phone_number, entry_reminders,
                         med_tracking, med_reminders)
        db.session.add(new_user)
        db.session.commit()
        flash("Successfully created account")
        return redirect("/dashboard")

    flash("That email is already associated with an account")
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    """Render the dashboard page."""

    if not session.get("user_id"):
        return redirect("/")

    return render_template("dashboard.html")


def convert_radio_to_bool(var):
    """Convert a radio value to boolean."""

    if var == "yes":
        var = True
    else:
        var = False

    return var


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///test-db")
    app.run(host="0.0.0.0", debug=True)
