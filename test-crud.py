"""Unit tests for CRUD functions"""

from model import (connect_to_db, db, User, Urge, Action, DiaryEntry,
                   UrgeEntry, ActionEntry)
import crud
import unittest
from datetime import datetime, date

class ConversionTestCase(unittest.TestCase):
    """Unit tests for conversion functions."""

    def test_radio_to_bool(self):
        """Tests convert_radio_to_bool."""

        self.assertEqual(crud.convert_radio_to_bool("yes"), True)
        self.assertEqual(crud.convert_radio_to_bool("no"), False)
        self.assertEqual(crud.convert_radio_to_bool("foo"), False)
        self.assertEqual(crud.convert_radio_to_bool(3), False)

    def test_bool_to_y_n(self):
        """Tests convert_bool_to_y_n."""

        self.assertEqual(crud.convert_bool_to_y_n(True), "yes")
        self.assertEqual(crud.convert_bool_to_y_n(False), "no")
        self.assertEqual(crud.convert_bool_to_y_n("x"), "invalid input")


class InitializeUserTestCase(unittest.TestCase):
    """Unit tests for functions that initialize a user."""
        
    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///testdb")
        db.create_all()
        crud.example_data()

        test_user = User(
            fname="Test",
            email="test@test.test",
            password="testpassword",
            phone_number="1234567890",
            entry_reminders=True,
            med_tracking=True,
            med_reminders=True
        )
        db.session.add(test_user)
        db.session.commit()

    def tearDown(self):
        """Stuff to do after every test."""
        
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
   

    def test_create_user(self):
        """Test create_user."""

        test_user = crud.create_user(
            "Test", "test@test.test", "testpassword",
            "1234567890", True, True, True
        )
        
        self.assertIsInstance(test_user, User)
        self.assertEqual(test_user.email, "test@test.test")
        self.assertEqual(test_user.med_reminders, True)

    def test_create_urge(self):
        """Test create_urge."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        test_urge = crud.create_urge(test_user.user_id, "Test Urge")

        self.assertIsInstance(test_urge, Urge)
        self.assertEqual(test_urge.description, "Test Urge")
        self.assertEqual(test_urge.active, True)

    def test_create_action(self):
        """Test create_action."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        test_action = crud.create_action(test_user.user_id, "Test Action")

        self.assertIsInstance(test_action, Action)
        self.assertEqual(test_action.description, "Test Action")
        self.assertEqual(test_action.active, True)

    def test_create_account_helper(self):
        """Test create_account_helper."""

        crud.create_account_helper(
            "Test2", "test2@test.test", "testpassword", "1234567890", True,
            True, True, "Urge1", "Urge2", "Urge3", "Action1", "Action2"
        )

        test_user = User.query.filter(
            User.email == "test2@test.test"
        ).first()

        test_user_urges = []
        for urge in test_user.urges:
            test_user_urges.append(urge.description)

        test_user_actions = []
        for action in test_user.actions:
            test_user_actions.append(action.description)

        self.assertIsInstance(test_user, User)
        self.assertEqual(test_user.fname, "Test2")
        self.assertEqual(test_user.med_reminders, True)
        self.assertEqual(test_user_urges, ["Urge1", "Urge2", "Urge3"])
        self.assertEqual(test_user_actions, ["Action1", "Action2"])


class InitializeEntriesTestCase(unittest.TestCase):
    """Unit tests for functions that initialize a group of entry."""

    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///testdb")
        db.create_all()
        crud.example_data()

        test_user = User(
            fname="Test",
            email="test@test.test",
            password="testpassword",
            phone_number="1234567890",
            entry_reminders=True,
            med_tracking=True,
            med_reminders=True
        )
        db.session.add(test_user)
        db.session.commit()

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        new_urges = []
        urge_names = ["Urge1", "Urge2", "Urge3"]
        for urge_name in urge_names:
            new_urges.append(
                Urge(
                    user_id=test_user.user_id,
                    description=urge_name,
                    active=True
                )
            )
        new_actions = []
        action_names = ["Action1", "Action2"]
        for action_name in action_names:
            new_actions.append(
                Action(
                    user_id=test_user.user_id,
                    description=action_name,
                    active=True
                )
            )
        db.session.add_all(new_urges)
        db.session.add_all(new_actions)

        test_diary_entry = DiaryEntry(
            user_id=test_user.user_id, 
            dt=datetime.now(), 
            sad_score=1, 
            angry_score=2, 
            fear_score=3, 
            happy_score=4, 
            shame_score=5, 
            skills_used=7
        )
        db.session.add(test_diary_entry)
        db.session.commit()
        

    def tearDown(self):
        """Stuff to do after every test."""
        
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_create_diary_entry(self):
        """Test create_diary_entry."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()

        test_diary_entry = crud.create_diary_entry(
            test_user.user_id, datetime.now(), 1, 2, 3, 4, 5, 7
        )

        self.assertIsInstance(test_diary_entry, DiaryEntry)
        self.assertEqual(test_diary_entry.dt.date(), date.today())
        self.assertEqual(test_diary_entry.angry_score, 2)
        self.assertEqual(test_diary_entry.skills_used, 7)

    def test_create_urge_entry(self):
        """Test create_urge_entry."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        test_diary_entry = DiaryEntry.query.filter(
            DiaryEntry.user == test_user
        ).first()

        test_urge_entry = crud.create_urge_entry(
            1, test_diary_entry.entry_id, test_user.user_id,
            datetime.now(), 4
        )

        self.assertIsInstance(test_urge_entry, UrgeEntry)
        self.assertEqual(
            test_urge_entry.d_entry_id, test_diary_entry.entry_id
        )
        self.assertEqual(test_urge_entry.dt.date(), date.today())
        self.assertEqual(test_urge_entry.score, 4)

    def test_create_action_entry(self):
        """Test create_action_entry."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        test_diary_entry = DiaryEntry.query.filter(
            DiaryEntry.user == test_user
        ).first()

        test_action_entry = crud.create_action_entry(
            1, test_diary_entry.entry_id, test_user.user_id,
            datetime.now(), 2
        )

        self.assertIsInstance(test_action_entry, ActionEntry)
        self.assertEqual(
            test_action_entry.d_entry_id, test_diary_entry.entry_id
        )
        self.assertEqual(test_action_entry.dt.date(), date.today())
        self.assertEqual(test_action_entry.score, 2)

    def test_create_d_u_a_entries_helper(self):
        """Test create_d_u_a_entries_helper."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()

        old_test_diary_entry = DiaryEntry.query.filter(
            DiaryEntry.user == test_user
        ).first()
        db.session.delete(old_test_diary_entry)
        db.session.commit()

        crud.create_d_u_a_entries_helper(
            test_user.user_id, 5, 4, 3, 2, 1, 1, 2, 3, True, False, 7
        )

        new_test_diary_entry = DiaryEntry.query.filter(
            DiaryEntry.user == test_user
        ).first()

        self.assertIsInstance(new_test_diary_entry, DiaryEntry)
        self.assertEqual(new_test_diary_entry.user_id, test_user.user_id)
        self.assertEqual(new_test_diary_entry.sad_score, 5)
        self.assertEqual(new_test_diary_entry.urge_entries[1].score, 2)
        self.assertEqual(new_test_diary_entry.action_entries[1].score, False)
        self.assertEqual(new_test_diary_entry.skills_used, 7)

        



    

if __name__ == '__main__':
    from server import app
    unittest.main()