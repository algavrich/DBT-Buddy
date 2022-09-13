"""Models for diary card app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """Model for a user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(25), nullable=False)
    phone_number = db.Column(db.String(20))
    entry_reminders = db.Column(db.Boolean, nullable=False)
    med_tracking = db.Column(db.Boolean, nullable=False)
    med_reminders = db.Column(db.Boolean, nullable=False)
    emgcy_contact = db.Column(db.String(20))
    fav_trend = db.Column(db.String(5))

    diary_entries = db.relationship("DiaryEntry", back_populates="user")
    med_entries = db.relationship("MedEntry", back_populates="user")

    def __repr__(self):
        """String representation for User object."""

        return f"<User email={self.email}>"


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
    urge_1 = db.Column(db.Integer, nullable=False)
    urge_2 = db.Column(db.Integer, nullable=False)
    urge_3 = db.Column(db.Integer, nullable=False)
    action_1 = db.Column(db.Boolean, nullable=False)
    action_2 = db.Column(db.Boolean, nullable=False)
    skills_used = db.Column(db.Integer, nullable=False)

    user = db.relationship("User", back_populates="diary_entries")

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


def connect_to_db(flask_app, db_uri="postgresql:///diary-card-app", 
                  echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)
    db.create_all()

    print("Connected to the db!")
