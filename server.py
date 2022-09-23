"""Flask server for diary card app."""

# IMPORTS

from flask import (Flask, session, request, flash,
                   render_template, redirect, jsonify)
from model import connect_to_db
import crud
from jinja2 import StrictUndefined
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
app.jinja_env.undefined = StrictUndefined

# ROUTES

@app.route("/")
def index():
    """Render homepage."""

    if session.get('user_id'):
        return redirect("/dashboard")

    return render_template("login.html")


@app.route("/login")
def login():
    """Log user in."""

    if session.get('user_id'):
        return redirect("/dashboard")

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


@app.route("/api/create-account", methods=["POST"])
def create_account():
    """Create new account with JSON from AJAX."""

    fname = request.json.get("fname")
    email = request.json.get("email")
    password = request.json.get("password")
    phone_number = request.json.get("phone_number")
    # Make this clean for DB
    urge_1 = request.json.get("urge1")
    urge_2 = request.json.get("urge2")
    urge_3 = request.json.get("urge3")
    action_1 = request.json.get("action1")
    action_2 = request.json.get("action2")
    entry_reminders = crud.convert_radio_to_bool(
        request.json.get("entry_reminders")
    )
    med_tracking = crud.convert_radio_to_bool(
        request.json.get("med_tracking")
    )
    med_reminders = crud.convert_radio_to_bool(
        request.json.get("med_reminders")
    )
    
    if not crud.get_user_by_email(email):
        crud.create_account_helper(
            fname, email, password, phone_number, entry_reminders,
            med_tracking, med_reminders, urge_1, urge_2, urge_3, 
            action_1, action_2)

        flash("Successfully created account")
        return jsonify({
            "success": True,
        })

    flash("That email is already associated with an account")
    return redirect("/create-account")


@app.route("/dashboard")
def dashboard():
    """Render the dashboard page."""

    if not session.get("user_id"):
        return redirect("/")
    
    current_user_id = session.get("user_id")
    urges = crud.get_urges_by_user_id(current_user_id)
    actions = crud.get_actions_by_user_id(current_user_id)
    weeks = crud.get_dict_for_weeks(current_user_id)

    this_week = crud.get_this_week_for_user(session.get("user_id"))

    # TODO possibly move this to helper func
    entries = make_entries_jsonifiable(this_week)

    # Is this an ok place for this?
    show_edit = False
    if crud.check_entry_today(current_user_id):
        show_edit = True

    return render_template(
        "dashboard.html", urges=urges, actions=actions,
        weeks=weeks, entries=entries, show_edit=show_edit)


@app.route("/new-diary-entry")
def new_diary_entry():
    """Render the new diary entry form."""

    current_user_id = session.get("user_id")

    if not session.get("user_id"):
        return redirect("/")

    if crud.check_entry_today(current_user_id):
        flash("You've already made an entry today. Try editing it!")
        return redirect("/dashboard")
    
    user_urges = crud.get_urges_by_user_id(session.get("user_id"))
    user_actions = crud.get_actions_by_user_id(session.get("user_id"))
    user_urges_descs = get_descs_from_object_list(user_urges)
    user_actions_descs = get_descs_from_object_list(user_actions)

    return render_template(
        "diary-entry.html", user_actions=user_actions_descs,
        user_urges=user_urges_descs)

# Combine these routes with multiple view functions in one route

@app.route("/new-diary-entry", methods=["POST"])
def create_new_diary_entry():
    """Create new DiaryEntry and pushes to DB given user input."""

    current_user_id = session.get("user_id")

    sad_score = int(request.form.get("sad"))
    angry_score = int(request.form.get("angry"))
    fear_score = int(request.form.get("fear"))
    happy_score = int(request.form.get("happy"))
    shame_score = int(request.form.get("shame"))
    urge_1_score = int(request.form.get("urge-1"))
    urge_2_score = int(request.form.get("urge-2"))
    urge_3_score = int(request.form.get("urge-3"))
    action_1 = crud.convert_radio_to_bool(request.form.get("action-1"))
    action_2 = crud.convert_radio_to_bool(request.form.get("action-2"))
    used_skills = int(request.form.get("used-skills"))

    crud.create_d_u_a_entries_helper(
        current_user_id, sad_score, angry_score, fear_score, happy_score,
        shame_score, urge_1_score, urge_2_score, urge_3_score, action_1,
        action_2, used_skills)
        
    flash("Entry successfully added")

    return redirect("/dashboard")


@app.route("/api/update-today-entry", methods=["PUT"])
def update_today_entry():
    """Updates today's entry in DB with info from AJAX request."""

    current_user_id = session.get("user_id")

    sad_score = int(request.json.get("sad_score"))
    angry_score = int(request.json.get("angry_score"))
    fear_score = int(request.json.get("fear_score"))
    happy_score = int(request.json.get("happy_score"))
    shame_score = int(request.json.get("shame_score"))
    urge_1_score = int(request.json.get("urge1_score"))
    urge_2_score = int(request.json.get("urge2_score"))
    urge_3_score = int(request.json.get("urge3_score"))
    action_1 = request.json.get("action1_score")
    action_2 = request.json.get("action2_score")
    used_skills = int(request.json.get("used_skills"))

    crud.update_today_entry(
        current_user_id, sad_score, angry_score, fear_score,
        happy_score, shame_score, urge_1_score, urge_2_score,
        urge_3_score, action_1, action_2, used_skills)

    return jsonify({
        "success": True,
        "status": "Your entry for today has been updated!",
    })


@app.route("/api/get-given-week")
def get_given_week():
    """Returns JSON for a week when given its start date as a string."""

    current_user_id = session.get("user_id")
    week_start_date_string = request.args.get("date_string")
    entries = crud.get_given_week_for_user_from_date_string(
        current_user_id,
        week_start_date_string
    )
    entries_as_dicts = make_entries_jsonifiable(entries)

    return jsonify(entries_as_dicts)


@app.route("/settings")
def settings():
    """Render the settings page."""

    if not session.get("user_id"):
        return redirect("/")

    current_user_id = session.get("user_id")
    current_user = crud.get_user_by_id(current_user_id)
    entry_reminders = convert_bool_to_y_n(current_user.entry_reminders)
    med_tracking = convert_bool_to_y_n(current_user.med_tracking)
    med_reminders = convert_bool_to_y_n(current_user.med_reminders)
    active_urges = crud.get_urges_by_user_id(current_user_id)
    active_actions = crud.get_actions_by_user_id(current_user_id)

    return render_template(
        "settings.html", user=current_user, entry_reminders=entry_reminders,
        med_tracking=med_tracking, med_reminders=med_reminders, 
        active_urges=active_urges, active_actions=active_actions)


@app.route("/logout")
def logout():
    """Log user out."""
    
    if session.get("user_id"):
        session.pop("user_id")
        session.pop("fname")

    return redirect("/")

# HELPERS

def convert_bool_to_y_n(value):
    """Convert a boolean value to yes or no."""
    
    if value:
        return "yes"

    return "no"


def get_descs_from_object_list(objects):
    """Get descriptions from list of user's custom Urge or Action object."""
    
    descriptions = []

    for object in objects:
        descriptions.append(object.description)

    return descriptions


def make_entries_jsonifiable(entries_as_objs):
    """Turn list of dicts of entry objects into list of dicts of dicts."""

    entries = []
    for entry in entries_as_objs:
        if entry is not None:
            entry_contents = {
                "date": datetime.strftime(entry["diary"].dt, "%A %d"),
                "sad score": entry["diary"].sad_score,
                "angry score": entry["diary"].angry_score,
                "fear score": entry["diary"].fear_score,
                "happy score": entry["diary"].happy_score,
                "shame score": entry["diary"].shame_score,
                "urge1 score": entry["urges"][0].score,
                "urge2 score": entry["urges"][1].score,
                "urge3 score": entry["urges"][2].score,
                "action1 score": convert_bool_to_y_n(
                    entry["actions"][0].score),
                "action2 score": convert_bool_to_y_n(
                    entry["actions"][1].score),
                "skills used": entry["diary"].skills_used
            }
        else:
            entry_contents = None
        entries.append(entry_contents)

    return entries


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///test-db")
    app.run(host="0.0.0.0", debug=True)