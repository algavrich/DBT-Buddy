"""Flask server for diary card app."""

from flask import Flask, session, request, flash, render_template, redirect
from model import DiaryEntry, connect_to_db, db
import crud
from jinja2 import StrictUndefined
import os
from datetime import datetime, date

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
    entry_reminders = convert_radio_to_bool(
        request.form.get("entry-reminders")
    )
    med_tracking = convert_radio_to_bool(
        request.form.get("med-tracking")
    )
    med_reminders = convert_radio_to_bool(
        request.form.get("med-reminders")
    )
    urge_1 = request.form.get("urge-1")
    urge_2 = request.form.get("urge-2")
    urge_3 = request.form.get("urge-3")
    action_1 = request.form.get("action-1")
    action_2 = request.form.get("action-2")

    
    if not crud.get_user_by_email(email):
        if password == password2:
            # TODO move this somewhere else (crud.py? helper func here?)
            new_user = crud.create_user(fname, email, password, phone_number,
                                        entry_reminders, med_tracking, 
                                        med_reminders)
            db.session.add(new_user)
            db.session.commit()
            new_user = crud.get_user_by_email(email)
            new_urges = []
            new_actions = []
            for urge in [urge_1, urge_2, urge_3]:
                new_urges.append(crud.create_urge(new_user.user_id, urge))
            for action in [action_1, action_2]:
                new_urges.append(crud.create_action(new_user.user_id, action))
            db.session.add_all(new_urges)
            db.session.add_all(new_actions)
            db.session.commit()

            flash("Successfully created account")
            return redirect("/dashboard")

        flash("Passwords do not match")
        return redirect("/create-account")

    flash("That email is already associated with an account")
    return redirect("/create-account")


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


@app.route("/new-diary-entry")
def new_diary_entry():
    """Render the new diary entry form."""
    
    user_urges = crud.get_urges_by_user_id(session.get("user_id"))
    user_actions = crud.get_actions_by_user_id(session.get("user_id"))
    user_urges_descs = get_descs_from_object_list(user_urges)
    user_actions_descs = get_descs_from_object_list(user_actions)

    return render_template("diary-entry.html", 
                           user_actions=user_actions_descs,
                           user_urges=user_urges_descs)


@app.route("/new-diary-entry", methods=["POST"])
def create_new_diary_entry():
    """Creates new DiaryEntry and pushes to DB given user input."""

    current_user_id = session.get("user_id")

    sad_score = int(request.form.get("sad"))
    angry_score = int(request.form.get("angry"))
    fear_score = int(request.form.get("fear"))
    happy_score = int(request.form.get("happy"))
    shame_score = int(request.form.get("shame"))
    urge_1_score = int(request.form.get("urge-1"))
    urge_2_score = int(request.form.get("urge-2"))
    urge_3_score = int(request.form.get("urge-3"))
    action_1 = convert_radio_to_bool(request.form.get("action-1"))
    action_2 = convert_radio_to_bool(request.form.get("action-2"))
    used_skills = int(request.form.get("used-skills"))

    # TODO make this into a helper function
    # FROM HERE
    new_d_entry = crud.create_diary_entry(
        current_user_id,
        datetime.now(),
        sad_score,
        angry_score,
        fear_score,
        happy_score,
        shame_score,
        used_skills
    )
    db.session.add(new_d_entry)
    db.session.commit()

    new_d_entry = crud.get_diary_entry_by_user_date(
        current_user_id, 
        date.today()
    )
    user_urges = crud.get_urges_by_user_id(current_user_id)
    urge_scores = [urge_1_score, urge_2_score, urge_3_score]
    new_entries = []
    for i in range(3):
        new_entries.append(crud.create_urge_entry(
            user_urges[i].urge_id, 
            new_d_entry.entry_id, 
            current_user_id,
            datetime.now(),
            urge_scores[i]
        ))
    user_actions = crud.get_actions_by_user_id(current_user_id)
    action_scores = [action_1, action_2]
    for i in range(2):
        new_entries.append(crud.create_action_entry(
            user_actions[i].action_id,
            new_d_entry.entry_id,
            current_user_id,
            datetime.now(),
            action_scores[i]
        ))
    db.session.add_all(new_entries)
    db.session.commit()
    # TO HERE
    flash("Entry successfully added")

    return redirect("/dashboard")



@app.route("/logout")
def logout():
    """Log user out."""

    session.pop("user_id")
    session.pop("fname")

    return redirect("/")


def convert_radio_to_bool(var):
    """Convert a radio value to boolean."""
    
    return var == "yes"


def get_descs_from_object_list(objects):
    """Get descriptions from list of user's custom Urge or Action object."""
    
    descriptions = []

    for object in objects:
        descriptions.append(object.description)

    return descriptions


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///test-db")
    app.run(host="0.0.0.0", debug=True)
