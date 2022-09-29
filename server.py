"""Flask server for diary card app."""

# IMPORTS

from flask import (Flask, session, request, flash,
                   render_template, redirect, jsonify)
from model import connect_to_db
import crud
import helpers
from jinja2 import StrictUndefined
import os
from datetime import date

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "")
app.jinja_env.undefined = StrictUndefined

# ROUTES

@app.route("/")
def index():
    """Render homepage."""

    current_user_id = session.get("user_id")
    
    if current_user_id:
        return redirect(f"/dashboard/{current_user_id}")

    return render_template("login.html")


@app.route("/login")
def login():
    """Log user in."""

    current_user_id = session.get("user_id")

    if current_user_id:
        return redirect(f"/dashboard/{current_user_id}")

    email = request.args.get("email")
    password = request.args.get("password")

    user = crud.get_user_by_email(email)

    if user and user.password == password:
        session["user_id"] = user.user_id
        session["fname"] = user.fname
        flash(f"Successfully logged in as {user.fname}")
        return redirect(f"/dashboard/{user.user_id}")

    else:
        flash("Incorrect email or password")
        return redirect("/")


@app.route("/create-account")
def create_account_form():
    """Render create account page."""

    current_user_id = session.get("user_id")
    
    if current_user_id:
        return redirect(f"/dashboard/{current_user_id}")
    
    return render_template("create-account.html")


@app.route("/api/create-account", methods=["POST"])
def create_account():
    """Create new account with JSON from AJAX."""

    if not session.get("user_id"):
        return redirect("/")

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
    entry_reminders = helpers.convert_radio_to_bool(
        request.json.get("entry_reminders")
    )
    med_tracking = helpers.convert_radio_to_bool(
        request.json.get("med_tracking")
    )
    med_reminders = helpers.convert_radio_to_bool(
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
    return jsonify({
        "success": False,
    })


@app.route("/dashboard/<user_id>")
def dashboard(user_id):
    """Render the dashboard page."""

    if not session.get("user_id"):
        return redirect("/")
    
    weeks = crud.get_dict_for_weeks(user_id)

    this_week = crud.get_this_week_for_user(session.get("user_id"))

    entries = helpers.make_entries_jsonifiable(this_week)

    # Is this an ok place for this?
    show_edit = False
    if crud.check_entry_today(user_id):
        show_edit = True

    return render_template(
        "dashboard.html", weeks=weeks, entries=entries,
        show_edit=show_edit, user_id=user_id)


@app.route("/new-diary-entry/<user_id>")
def new_diary_entry(user_id):
    """Render the new diary entry form."""

    if not session.get("user_id"):
        return redirect("/")

    if crud.check_entry_today(user_id):
        flash("You've already made an entry today. Try editing it!")
        return redirect(f"/dashboard/{user_id}")
    
    user_urges = helpers.get_descs_from_object_list(
        crud.get_urges_by_user_id(
            session.get("user_id")
        )
    )
    user_actions = helpers.get_descs_from_object_list(
        crud.get_actions_by_user_id(
            session.get("user_id")
        )
    )

    return render_template(
        "diary-entry.html", user_actions=user_actions,
        user_urges=user_urges, user_id=user_id)

# Combine these routes with multiple view functions in one route

@app.route("/new-diary-entry/<user_id>", methods=["POST"])
def create_new_diary_entry(user_id):
    """Create new DiaryEntry and pushes to DB given user input."""

    if not session.get("user_id"):
        return redirect("/")

    sad_score = int(request.form.get("sad"))
    angry_score = int(request.form.get("angry"))
    fear_score = int(request.form.get("fear"))
    happy_score = int(request.form.get("happy"))
    shame_score = int(request.form.get("shame"))
    urge_1_score = int(request.form.get("urge-1"))
    urge_2_score = int(request.form.get("urge-2"))
    urge_3_score = int(request.form.get("urge-3"))
    action_1 = helpers.convert_radio_to_bool(request.form.get("action-1"))
    action_2 = helpers.convert_radio_to_bool(request.form.get("action-2"))
    used_skills = int(request.form.get("used-skills"))

    crud.create_d_u_a_entries_helper(
        user_id, sad_score, angry_score, fear_score, happy_score,
        shame_score, urge_1_score, urge_2_score, urge_3_score,
        action_1, action_2, used_skills)
        
    flash("Entry successfully added")

    return redirect(f"/dashboard/{user_id}")


@app.route("/api/update-today-entry", methods=["PUT"])
def update_today_entry():
    """Updates today's entry in DB with info from AJAX request."""

    if not session.get("user_id"):
        return redirect("/")

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

    updated_d_entry = crud.get_diary_entry_by_user_date(
        current_user_id, date.today()
    )
    updated_d_entry = helpers.dict_for_day(updated_d_entry)

    return jsonify(updated_d_entry)


@app.route("/api/get-given-week")
def get_given_week():
    """Returns JSON for a week when given its start date as a string."""

    if not session.get("user_id"):
        return redirect("/")

    current_user_id = session.get("user_id")

    week_start_date_string = request.args.get("date_string")
    entries = crud.get_given_week_for_user_from_date_string(
        current_user_id,
        week_start_date_string
    )
    entries_as_dicts = helpers.make_entries_jsonifiable(entries)

    return jsonify(entries_as_dicts)


@app.route("/settings")
def settings():
    """Render the settings page."""

    if not session.get("user_id"):
        return redirect("/")

    current_user_id = session.get("user_id")

    current_user = crud.get_user_by_id(current_user_id)
    entry_reminders = helpers.convert_bool_to_y_n(current_user.entry_reminders)
    med_tracking = helpers.convert_bool_to_y_n(current_user.med_tracking)
    med_reminders = helpers.convert_bool_to_y_n(current_user.med_reminders)
    active_urges = crud.get_urges_by_user_id(current_user_id)
    active_actions = crud.get_actions_by_user_id(current_user_id)

    return render_template(
        "settings.html", user=current_user, entry_reminders=entry_reminders,
        med_tracking=med_tracking, med_reminders=med_reminders, 
        active_urges=active_urges, active_actions=active_actions)


@app.route("/api/update-settings", methods=["PUT"])
def update_settings():
    """Updates user's settings in DB with info from AJAX request."""

    current_user_id = session.get("user_id")

    if not current_user_id:
        return redirect("/")

    fname = request.json.get("fname")
    email = request.json.get("email")
    phone_number = request.json.get("phone_number")
    urge1 = request.json.get("urge1")
    urge2 = request.json.get("urge2")
    urge3 = request.json.get("urge3")
    old_urge1_id = request.json.get("old_urge1_id")
    old_urge2_id = request.json.get("old_urge2_id")
    old_urge3_id = request.json.get("old_urge3_id")
    action1 = request.json.get("action1")
    action2 = request.json.get("action2")
    old_action1_id = request.json.get("old_action1_id")
    old_action2_id = request.json.get("old_action2_id")
    entry_reminders = helpers.convert_radio_to_bool(
        request.json.get("entry_reminders")
    )
    med_tracking = helpers.convert_radio_to_bool(
        request.json.get("med_tracking")
    )
    med_reminders = helpers.convert_radio_to_bool(
        request.json.get("med_reminders")
    )

    crud.update_user(
        current_user_id, fname, email, phone_number,
        entry_reminders, med_tracking, med_reminders)

    new_urges = [urge1, urge2, urge3]
    old_urges = [old_urge1_id, old_urge2_id, old_urge3_id]
    for i in range(3):
        crud.update_urge(current_user_id, old_urges[i], new_urges[i])

    new_actions = [action1, action2]
    old_actions = [old_action1_id, old_action2_id]
    for i in range(2):
        crud.update_action(current_user_id, old_actions[i], new_actions[i])

    flash("Saved changes")
    return jsonify({
        "success": True,
    })


@app.route("/logout")
def logout():
    """Log user out."""
    
    if session.get("user_id"):
        session.pop("user_id")
        session.pop("fname")

    return redirect("/")


if __name__ == "__main__":
    connect_to_db(app, db_uri="postgresql:///test-db")
    app.run(host="0.0.0.0", debug=True)