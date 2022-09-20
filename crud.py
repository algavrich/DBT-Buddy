"""CRUD functions."""

from model import (SentReminder, db, connect_to_db, User, Urge, Action, DiaryEntry, 
                   UrgeEntry, ActionEntry)
from datetime import date, datetime, timedelta
from sqlalchemy import cast, DATE
from random import randint, choice

# HELPER

def convert_radio_to_bool(var):
    """Convert a radio value to boolean."""

    if var is None:
        return False
    
    return var == "yes"

# CREATE

def create_user(
    fname, email, password, phone_number,
    entry_reminders, med_tracking, med_reminders):
    """Create and return a new user."""

    user = User(
        fname=fname,
        email=email, 
        password=password, 
        phone_number=phone_number, 
        entry_reminders=entry_reminders, 
        med_tracking=med_tracking, 
        med_reminders=med_reminders
    )

    return user


def create_urge(user_id, description):
    """Create and return a new urge."""

    urge = Urge(
        user_id=user_id, 
        description=description
    )

    return urge


def create_action(user_id, description):
    """Create and return a new action."""

    action = Action(
        user_id=user_id, 
        description=description
    )

    return action


def create_account_helper(
        fname, email, password, phone_number, entry_reminders, med_tracking, 
        med_reminders, urge_1, urge_2, urge_3, action_1, action_2):
    """Create new User, Urge, and Action objects and commit to DB."""

    new_user = create_user(fname, email, password, phone_number,
                                        entry_reminders, med_tracking, 
                                        med_reminders)

    db.session.add(new_user)
    db.session.commit()

    new_user = get_user_by_email(email)
    new_urges = []
    new_actions = []

    for urge in [urge_1, urge_2, urge_3]:
        new_urges.append(create_urge(new_user.user_id, urge))

    for action in [action_1, action_2]:
        new_urges.append(create_action(new_user.user_id, action))

    db.session.add_all(new_urges)
    db.session.add_all(new_actions)
    db.session.commit()


def create_diary_entry(
    user_id, dt, sad_score, angry_score, fear_score,
    happy_score, shame_score, skills_used):
    """Create and return a new diary entry."""

    d_entry = DiaryEntry(
        user_id=user_id, 
        dt=dt, 
        sad_score=sad_score, 
        angry_score=angry_score, 
        fear_score=fear_score, 
        happy_score=happy_score, 
        shame_score=shame_score, 
        skills_used=skills_used
    )

    return d_entry


# def create_med_entry(user_id, dt):
#     """Create and return a new med entry."""

#     m_entry = MedEntry(
#         user_id=user_id, 
#         dt=dt
#     )

#     return m_entry


def create_urge_entry(urge_id, d_entry_id, user_id, dt, score):
    """Create and return a new urge entry."""

    u_entry = UrgeEntry(
        urge_id=urge_id, 
        d_entry_id=d_entry_id,
        user_id=user_id, 
        dt=dt,
        score=score
    )

    return u_entry


def create_action_entry(action_id, d_entry_id, user_id, dt, score):
    """Create and return a new action entry."""

    a_entry = ActionEntry(
        action_id=action_id, 
        d_entry_id=d_entry_id, 
        user_id=user_id, 
        dt=dt,
        score=score
    )

    return a_entry


def create_d_u_a_entries_helper(
        current_user_id, sad_score, angry_score, fear_score, happy_score,
        shame_score, urge_1_score, urge_2_score, urge_3_score, action_1,
        action_2, used_skills):
    """Create new Diary, Urge, and Action entries and commit to DB."""

    new_d_entry = create_diary_entry(
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

    new_d_entry = get_diary_entry_by_user_date(
        current_user_id, 
        date.today()
    )
    user_urges = get_urges_by_user_id(current_user_id)
    urge_scores = [urge_1_score, urge_2_score, urge_3_score]
    new_entries = []
    for i in range(3):
        new_entries.append(create_urge_entry(
            user_urges[i].urge_id, 
            new_d_entry.entry_id, 
            current_user_id,
            datetime.now(),
            urge_scores[i]
        ))
    user_actions = get_actions_by_user_id(current_user_id)
    action_scores = [action_1, action_2]
    for i in range(2):
        new_entries.append(create_action_entry(
            user_actions[i].action_id,
            new_d_entry.entry_id,
            current_user_id,
            datetime.now(),
            action_scores[i]
        ))
    db.session.add_all(new_entries)
    db.session.commit()


def create_sent_rem(user_id, dt):
    """Create new SentReminder object."""

    sent_reminder = SentReminder(
        user_id=user_id,
        dt=dt
    )

    return sent_reminder


def add_new_rem_to_db(user_id):
    """Create new SentReminder object and commit it to DB"""

    new_reminder = create_sent_rem(
        user_id,
        datetime.now()
    )

    db.session.add(new_reminder)
    db.session.commit()

# READ

def get_user_by_id(user_id):
    """Return user with given ID."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return user with given email."""

    return User.query.filter(User.email == email).first()


def get_users_entry_reminders():
    """Return all users who opted in to entry reminders."""

    return User.query.filter(User.entry_reminders == True).all()


# def get_users_med_reminders():
#     """Return all users who opted in to med reminders."""

#     return User.query.filter(User.med_reminders == True).all()


# def get_fav_trend_by_user_id(user_id):
#     """Return user's favorite trend when given their ID."""

#     user = get_user_by_id(user_id)

#     return user.fav_trend


def get_diary_entries_by_user_id(user_id):
    """Return list of user's diary entries when given their ID."""

    user = get_user_by_id(user_id)
    
    return user.diary_entries


# def get_med_entries_by_user_id(user_id):
#     """Return list of user's med entries when given their ID."""

#     user = get_user_by_id(user_id)
    
#     return user.med_entries


def get_urges_by_user_id(user_id):
    """Return a list of user's urges when given their ID."""

    user = get_user_by_id(user_id)

    return user.urges


def get_actions_by_user_id(user_id):
    """Return a list of user's actions when given their ID."""

    user = get_user_by_id(user_id)

    return user.actions


def get_diary_entry_by_user_date(user_id, q_date):
    """Return a user's diary entry for a given date."""

    return DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id,
        cast(DiaryEntry.dt, DATE) == q_date
    ).first()


def get_this_week_for_user(user_id):
    """Return a list of a user's entries for the current week."""

    entries = []

    for i in range(7, 0, -1):
        date_get = date.today() - timedelta(days=(i-1))
        diary_entry = get_diary_entry_by_user_date(user_id, date_get)
        if diary_entry:
            entries.append(
                {
                    "diary": diary_entry,
                    "urges": diary_entry.urge_entries,
                    "actions": diary_entry.action_entries
                }
            )
        else:
            entries.append(None)

    return entries


def check_entry_today(user_id):
    """Returns True if user made an entry already, False if not."""

    if get_diary_entry_by_user_date(user_id, date.today()):
        return True

    return False


def check_entry_past_24(user_id):
    """Returns True if user made an entry in the past 24 hours, False if not."""

    entry = DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id,
        DiaryEntry.dt > (datetime.now() - timedelta(days=1))
    ).first()

    if entry:
        return True

    return False


def check_for_reminder(user_id):
    """Check if the given user has been reminded in the last day."""

    reminder = SentReminder.query.filter(
        SentReminder.user_id == user_id,
        SentReminder.dt > (datetime.now() - timedelta(days=1))
    ).first()

    if reminder:
        return True

    return False

# UPDATE

def update_today_entry(
        current_user_id, sad_score, angry_score, fear_score,
        happy_score, shame_score, urge_1_score, urge_2_score,
        urge_3_score, action_1, action_2, used_skills):
    """Updates Diary, Urge, and Action entries for the current day."""
    
    current_d_entry = get_diary_entry_by_user_date(
        current_user_id, 
        date.today()
    )
    new_u_scores = [
        urge_1_score,
        urge_2_score,
        urge_3_score
    ]
    current_u_entries = current_d_entry.urge_entries
    new_a_scores = [
        action_1,
        action_2
    ]
    current_a_entries = current_d_entry.action_entries

    current_d_entry.sad_score = sad_score
    current_d_entry.angry_score = angry_score
    current_d_entry.fear_score = fear_score
    current_d_entry.happy_score = happy_score
    current_d_entry.shame_score = shame_score
    current_d_entry.sad_score = sad_score
    current_d_entry.skills_used = used_skills

    for i in range(3):
        current_u_entries[i].score = new_u_scores[i]

    for i in range(2):
        current_a_entries[i].score = convert_radio_to_bool(new_a_scores[i])

    db.session.commit()

# POPULATE TEST DATABASE

def example_data():
    """Add example data to DB for Lucy's user."""

    lucy = create_user(
    "Lucy", "annalgav@gmail.com", "password",
    "5108469189", True, False, False)
    db.session.add(lucy)
    db.session.commit()

    urges = []
    for i in range(3):
            urges.append(create_urge(1, f"Urge {i}"))
    db.session.add_all(urges)

    actions = []
    for j in range(2):
        actions.append(create_action(1, f"Action {j}"))
    db.session.add_all(actions)
    db.session.commit()

    for k in range(30, 0, -1):
        dt = datetime.now() - timedelta(days=(k - 1))

        diary_entry = create_diary_entry(
            1, dt, randint(0, 5), randint(0, 5), randint(0, 5),
            randint(0, 5), randint(0, 5), randint(0, 5))
        db.session.add(diary_entry)
        db.session.commit()

        current_date = dt.date()
        diary_entry = get_diary_entry_by_user_date(1, current_date)
        d_entry_id = diary_entry.entry_id
        urge_entries = []
        for m in range(3):
            urge_entries.append(
                create_urge_entry(
                    (m + 1), d_entry_id, 1, dt, randint(0, 5)
                )
            )
        db.session.add_all(urge_entries)

        action_entries = []
        for n in range(2):
            action_entries.append(
                create_action_entry(
                    (n + 1), d_entry_id, 1, dt, choice([True, False])
                )
            )
        db.session.add_all(action_entries)
        db.session.commit()



if __name__ == '__main__':
    from server import app
    connect_to_db(app, db_uri="postgresql:///test-db")