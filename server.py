"""Flask server for diary card app."""

from flask import Flask, session, request, flash, render_template, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
from datetime import datetime

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
        session["fname"] = user.fname
        flash(f"Successfully logged in as {user.fname}")
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

    # TODO add input validation

    fname = request.form.get("fname")
    email = request.form.get("email")
    password = request.form.get("password")
    password2 = request.form.get("password-2")
    phone_number = request.form.get("phone-number")
    entry_reminders = request.form.get("entry-reminders")
    med_tracking = request.form.get("med-tracking")
    med_reminders = request.form.get("med-reminders")

    entry_reminders = convert_radio_to_bool(entry_reminders)
    med_tracking = convert_radio_to_bool(med_tracking)
    med_reminders = convert_radio_to_bool(med_reminders)

    if not crud.get_user_by_email(email):
        if password == password2:
            new_user = crud.create_user(fname, email, password, phone_number, entry_reminders,
                            med_tracking, med_reminders)
            db.session.add(new_user)
            db.session.commit()

            flash("Successfully created account")
            return redirect("/dashboard")

        flash("Passwords do not match")
        return redirect("/")

    flash("That email is already associated with an account")
    return redirect("/")


@app.route("/dashboard")
def dashboard():
    """Render the dashboard page."""

    if not session.get("user_id"):
        return redirect("/")

    this_week = crud.get_this_week_for_user(session.get("user_id"))
    entries = []
    for entry in this_week:
        if entry is not None:
            entry_contents = {
                "date": datetime.strftime(entry.dt, "%A %d"),
                "sad score": entry.sad_score,
                "angry score": entry.angry_score,
                "fear score": entry.fear_score,
                "shame score": entry.shame_score,
                "skills used": entry.skills_used
            }
        else:
            entry_contents = None
        entries.append(entry_contents)

    return render_template("dashboard.html", entries=entries)


@app.route("/logout")
def logout():
    """Log user out."""

    session.pop("user_id")
    session.pop("fname")

    return redirect("/")


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
