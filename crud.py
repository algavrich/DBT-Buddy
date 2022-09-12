"""CRUD functions."""

from model import db, User, DiaryEntry, MedEntry, connect_to_db


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

    # is this ok? or should i do the indentation like in the def line
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

if __name__ == '__main__':
    from server import app
    connect_to_db(app)