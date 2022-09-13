"""CRUD functions."""

from model import db, User, DiaryEntry, MedEntry, connect_to_db
from datetime import date, datetime


def create_user(email, password, phone_number, entry_reminders, med_tracking,
                med_reminders, emgcy_contact, fav_trend):
    """Create and return a new user."""

    user = User(
        email=email, 
        password=password, 
        phone_number=phone_number, 
        entry_reminders=entry_reminders, 
        med_tracking=med_tracking, 
        med_reminders=med_reminders,
        emgcy_contact=emgcy_contact, 
        fav_trend=fav_trend
        )

    return user


def create_diary_entry(user_id, dt, sad_score, angry_score, fear_score,
                 happy_score, shame_score, urge_1, urge_2, urge_3, action_1,
                 action_2, skills_used):
    """Create and return a new diary entry."""

    d_entry = DiaryEntry(
        user_id=user_id, 
        dt=dt, 
        sad_score=sad_score, 
        angry_score=angry_score, 
        fear_score=fear_score, 
        happy_score=happy_score, 
        shame_score=shame_score, 
        urge_1=urge_1, 
        urge_2=urge_2, 
        urge_3=urge_3, 
        action_1=action_1, 
        action_2=action_2, 
        skills_used=skills_used
        )

    return d_entry


def create_med_entry(user_id, dt):
    """Create and return a new med entry."""

    m_entry = MedEntry(user_id=user_id, dt=dt)

    return m_entry


def example_data():
    """Create test data."""

    new_users = []
    new_d_entries = []
    new_m_entries = []
    for i in range(1, 11):
        new_users.append(create_user(f"user{i}@test.com", f"password{i}",
                                     f"{i}{i}{i}{i}{i}{i}{i}{i}{i}{i}", True,
                                     True, True, f"6666666666", "a_1"))
        for j in range(10):
            new_d_entries.append(create_diary_entry(i, datetime.now(), 5, 5,
                                                    5, 5, 5, 5, 5, 5, True,
                                                    True, 8))
            new_m_entries.append(create_med_entry(i, datetime.now()))

    db.session.add_all(new_users)
    db.session.add_all(new_d_entries)
    db.session.add_all(new_m_entries)
    db.session.commit()
    


if __name__ == '__main__':
    from server import app
    connect_to_db(app, db_uri="postgresql:///test-db")