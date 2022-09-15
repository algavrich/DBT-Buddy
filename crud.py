"""CRUD functions."""

from model import (db, connect_to_db, User, DiaryEntry, MedEntry, 
                   UrgeEntry, ActionEntry, Urge, Action)
from datetime import date, datetime, timedelta
from sqlalchemy import cast, DATE

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


def get_users_med_reminders():
    """Return all users who opted in to med reminders."""

    return User.query.filter(User.med_reminders == True).all()


def get_fav_trend_by_user_id(user_id):
    """Return user's favorite trend when given their ID."""

    user = get_user_by_id(user_id)

    return user.fav_trend


def get_diary_entries_by_user_id(user_id):
    """Return list of user's diary entries when given their ID."""

    user = get_user_by_id(user_id)
    
    return user.diary_entries


def get_med_entries_by_user_id(user_id):
    """Return list of user's med entries when given their ID."""

    user = get_user_by_id(user_id)
    
    return user.med_entries


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


def get_urge_entries_by_d_entry_id(d_entry_id):
    """Return a list of a diary entry's corresponding urge entries."""
    return UrgeEntry.query.filter(
        UrgeEntry.d_entry_id == d_entry_id
    ).all()


def get_action_entries_by_d_entry_id(d_entry_id):
    """Return a list of a diary entry's corresponding action entries."""
    return ActionEntry.query.filter(
        ActionEntry.d_entry_id == d_entry_id
    ).all()


def get_this_week_for_user(user_id):
    """Return a list of a user's entries for the current week."""
    
    today = date.today()

    entries = []

    for i in range(7):
        date_get = today - timedelta(days = i)
        entries.append(get_diary_entry_by_user_date(user_id, date_get))

    return entries

# POPULATE TEST DATABASE

def example_data():
    """Create test data."""

    stuff_to_add = []
    for i in range(10):
        # Create ten test users
        stuff_to_add.append(create_user(
            "User{i}", f"user{i}@test.com", f"password{i}",
            f"{i}{i}{i}{i}{i}{i}{i}{i}{i}{i}", True, True, True))

        for j in range(3):
            # For each test user, create three test urges
            stuff_to_add.append(create_urge((i + 1), "Urge Description"))

        for k in range(2):
            # For each test user, create two test actions
            stuff_to_add.append(create_action((i + 1), "Action Description"))

        for l in range(10):
            # For each test user, create ten test diary entries
            stuff_to_add.append(
                create_diary_entry(
                    (i + 1), datetime.now(), 5, 5, 5, 5, 5, 8))
            for m in range(3):
                # For each test diary entry, create three test urge entries
                stuff_to_add.append(
                    create_urge_entry(
                        (m + 1), (l + 1), (i + 1), datetime.now(), 5))
            
            for n in range(2):
                # For each test diary entry, create two test action entries
                stuff_to_add.append(
                    create_action_entry(
                        (n + 1), (l + 1), (i + 1), datetime.now(), 5))
            
            # For each test user, create ten test med entries
            stuff_to_add.append(create_med_entry((i + 1), datetime.now()))

    db.session.add_all(stuff_to_add)
    db.session.commit()
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app, db_uri="postgresql:///test-db")