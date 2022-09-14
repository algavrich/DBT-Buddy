"""CRUD functions."""

from model import (db, connect_to_db, User, DiaryEntry, MedEntry, UrgeEntry,
                   ActionEntry, Urge, Action)
from datetime import date, datetime, timedelta
from sqlalchemy import cast, DATE


def create_user(fname, email, password, phone_number, entry_reminders, med_tracking,
                med_reminders):
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


def create_diary_entry(user_id, dt, sad_score, angry_score, fear_score,
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


def create_med_entry(user_id, dt):
    """Create and return a new med entry."""

    m_entry = MedEntry(
        user_id=user_id, 
        dt=dt
        )

    return m_entry


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


def get_user_by_id(user_id):
    """Returns user with given ID."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Returns user with given email."""

    return User.query.filter(User.email == email).first()


def get_users_entry_reminders():
    """Returns all users who opted in to entry reminders."""

    return User.query.filter(User.entry_reminders == True).all()


def get_users_med_reminders():
    """Returns all users who opted in to med reminders."""

    return User.query.filter(User.med_reminders == True).all()


def get_fav_trend_by_user_id(user_id):
    """Returns user's favorite trend when given their ID."""

    user = get_user_by_id(user_id)

    return user.fav_trend


def get_diary_entries_by_user_id(user_id):
    """Returns list of user's diary entries when given their ID."""

    user = get_user_by_id(user_id)
    
    return user.diary_entries


def get_med_entries_by_user_id(user_id):
    """Returns list of user's med entries when given their ID."""

    user = get_user_by_id(user_id)
    
    return user.med_entries


def get_urges_by_user_id(user_id):
    """Returns a list of user's urges when given their ID."""

    user = get_user_by_id(user_id)

    return user.urges


def get_actions_by_user_id(user_id):
    """Returns a list of user's actions when given their ID."""

    user = get_user_by_id(user_id)

    return user.actions


def get_diary_entry_by_user_date(user_id, q_date):
    """Returns a list of user's diary entries when given user ID and date."""

    return DiaryEntry.query.filter(
        DiaryEntry.user_id == user_id,
        cast(DiaryEntry.dt, DATE) == q_date
        ).first()


def get_this_week_for_user(user_id):
    """Returns a list of DiaryEntry objects for the current week when given a user ID."""
    
    today = date.today()

    entries = []

    for i in range(7):
        date_get = today - timedelta(days = i)
        entries.append(get_diary_entry_by_user_date(user_id, date_get))

    return entries



def example_data():
    """Create test data."""

    stuff_to_add = []
    for i in range(10):
        # Create ten test users
        stuff_to_add.append(create_user("User{i}", f"user{i}@test.com",
                                        f"password{i}",
                                        f"{i}{i}{i}{i}{i}{i}{i}{i}{i}{i}",
                                        True, True, True))
        for j in range(3):
            # For each test user, create three test urges
            stuff_to_add.append(create_urge((i + 1), "Urge Description"))
        for k in range(2):
            # For each test user, create two test actions
            stuff_to_add.append(create_action((i + 1), "Action Description"))
        for l in range(10):
            # For each test user, create ten test diary entries
            stuff_to_add.append(create_diary_entry((i + 1), datetime.now(), 5, 5,
                                                    5, 5, 5, 8))
            for m in range(3):
                # For each test diary entry, create three test urge entries
                stuff_to_add.append(create_urge_entry((m + 1), (l + 1), (i + 1), datetime.now(), 5))
            for n in range(2):
                # For each test diary entry, create two test action entries
                stuff_to_add.append(create_action_entry((n + 1), (l + 1), (i + 1), datetime.now(), 5))
            # For each test user, create ten test med entries
            stuff_to_add.append(create_med_entry((i + 1), datetime.now()))

    db.session.add_all(stuff_to_add)
    db.session.commit()
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app, db_uri="postgresql:///test-db")