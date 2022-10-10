"""Models for diary card app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    pw_hash = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(20))
    entry_reminders = db.Column(db.Boolean, nullable=False)
    med_tracking = db.Column(db.Boolean, nullable=False)
    med_reminders = db.Column(db.Boolean, nullable=False)
    init_dt = db.Column(db.DateTime, nullable=False)

    diary_entries = db.relationship("DiaryEntry", back_populates="user")
    med_entries = db.relationship("MedEntry", back_populates="user")
    urges = db.relationship("Urge", back_populates="user")
    actions = db.relationship("Action", back_populates="user")
    sent_reminders = db.relationship("SentReminder", back_populates="user")
    sent_med_reminders = db.relationship("SentMedReminder", back_populates="user")

    def __repr__(self):
        """String representation for User object."""

        return f"<User email={self.email}>"
        

class Urge(db.Model):
    """Model for an urge entry."""

    __tablename__ = "urges"

    urge_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False
    )
    description = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    position = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="urges")
    urge_entries = db.relationship("UrgeEntry", back_populates="urge")

    def __repr__(self):
        """String representation for Urge object."""

        return f"<Urge urge_id={self.urge_id} user_id={self.user_id}>"
        

class Action(db.Model):
    """Model for an action entry."""

    __tablename__ = "actions"

    action_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.user_id"), nullable=False
    )
    description = db.Column(db.String(50), nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    position = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="actions")
    action_entries = db.relationship("ActionEntry", back_populates="action")

    def __repr__(self):
        """String representation for Action object."""

        return f"<Action action_id={self.action_id} user_id={self.user_id}>"


class DiaryEntry(db.Model):
    """Model for a diary entry."""

    __tablename__ = "diary_entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    dt = db.Column(db.DateTime, nullable=False)
    sad_score = db.Column(db.Integer, nullable=False)
    angry_score = db.Column(db.Integer, nullable=False)
    fear_score = db.Column(db.Integer, nullable=False)
    happy_score = db.Column(db.Integer, nullable=False)
    shame_score = db.Column(db.Integer, nullable=False)
    skills_used = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="diary_entries")
    urge_entries = db.relationship("UrgeEntry", back_populates="diary_entry")
    action_entries = db.relationship(
        "ActionEntry", back_populates="diary_entry"
    )

    def __repr__(self):
        """String representation for DiaryEntry object."""

        return f"<DiaryEntry entry_id={self.entry_id} user_id={self.user_id}>"


class MedEntry(db.Model):
    """Model for a med entry."""

    __tablename__ = "med_entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    dt = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="med_entries")

    def __repr__(self):
        """String representation for MedEntry object."""

        return f"<MedEntry entry_id={self.entry_id} user_id={self.user_id}>"

    
class UrgeEntry(db.Model):
    """Model for an urge entry."""

    __tablename__ = "urge_entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    urge_id = db.Column(
        db.Integer, db.ForeignKey("urges.urge_id"), nullable=False
    )
    d_entry_id = db.Column(
        db.Integer, db.ForeignKey("diary_entries.entry_id"), nullable=False
    )
    user_id = db.Column(db.Integer, nullable=False)
    dt = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Integer, nullable=False)

    diary_entry = db.relationship("DiaryEntry", back_populates="urge_entries")
    urge = db.relationship("Urge", back_populates="urge_entries")

    def __repr__(self):
        """String representation for UrgeEntry object."""

        return f"<UrgeEntry entry_id={self.entry_id} urge_id={self.urge_id}>"


class ActionEntry(db.Model):
    """Model for an action entry."""

    __tablename__ = "action_entries"

    entry_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    action_id = db.Column(
        db.Integer, db.ForeignKey("actions.action_id"), nullable=False
    )
    d_entry_id = db.Column(
        db.Integer, db.ForeignKey("diary_entries.entry_id"), nullable=False
    )
    user_id = db.Column(db.Integer, nullable=False)
    dt = db.Column(db.DateTime, nullable=False)
    score = db.Column(db.Boolean, nullable=False)

    diary_entry = db.relationship(
        "DiaryEntry", back_populates="action_entries"
    )
    action = db.relationship("Action", back_populates="action_entries")

    def __repr__(self):
        """String representation for ActionEntry object."""

        return (f"<ActionEntry entry_id={self.entry_id} action_id={self.action_id}>")


class SentReminder(db.Model):
    """Model for a sent reminder."""

    __tablename__ = "sent_reminders"

    rem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    dt = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="sent_reminders")

    def __repr__(self):
        """String representation for SentReminder object."""

        return f"<SentReminder rem_id={self.rem_id} user_id={self.user_id}>"


class SentMedReminder(db.Model):
    """Model for a sent med reminder."""

    __tablename__ = "sent_med_reminders"

    rem_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    dt = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", back_populates="sent_med_reminders")

    def __repr__(self):
        """String representation for SentMedReminder object."""

        return f"<SentMedReminder rem_id={self.rem_id} user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///diary-card-app", 
                  echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    db.create_all()

    print("Connected to the db!")
