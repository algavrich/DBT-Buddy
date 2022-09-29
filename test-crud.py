"""Unit tests for CRUD functions"""

from model import (ActionEntry, UrgeEntry, connect_to_db, db,
                   User, Urge, Action, DiaryEntry, SentReminder)
import crud
import unittest
from datetime import date, timedelta

class InitializeUserTestCase(unittest.TestCase):
    """Unit test for function that initializes a user."""
        
    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///testdb")

    def tearDown(self):
        """Stuff to do after every test."""
        
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

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
    """Unit test for function that initializes a group of entries."""

    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///testdb")
        
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

    def tearDown(self):
        """Stuff to do after every test."""
        
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_create_d_u_a_entries_helper(self):
        """Test create_d_u_a_entries_helper."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()

        crud.create_d_u_a_entries_helper(
            test_user.user_id, 5, 4, 3, 2, 1, 1, 2, 3, True, False, 7
        )

        test_diary_entry = DiaryEntry.query.filter(
            DiaryEntry.user == test_user
        ).first()

        self.assertIsInstance(test_diary_entry, DiaryEntry)
        self.assertEqual(test_diary_entry.user_id, test_user.user_id)
        self.assertEqual(test_diary_entry.dt.date(), date.today())
        self.assertEqual(test_diary_entry.sad_score, 5)
        self.assertEqual(test_diary_entry.urge_entries[1].score, 2)
        self.assertEqual(test_diary_entry.action_entries[1].score, False)
        self.assertEqual(test_diary_entry.skills_used, 7)


class RemindersTestCase(unittest.TestCase):
    """Unit test for function that creates SentReminder records."""

    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///testdb")

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

    def test_add_new_rem_to_db(self):
        """Test add_new_rem_to_db."""

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()

        crud.add_new_rem_to_db(test_user.user_id)

        test_rem = SentReminder.query.filter(
            SentReminder.user_id == test_user.user_id
        ).first()

        self.assertIsInstance(test_rem, SentReminder)
        self.assertEqual(test_rem.dt.date(), date.today())


class GetWeekTestCase(unittest.TestCase):
    """Unit test for function that gets a given week's entries."""

    def setUp(self):
        """Stuff to do before every test."""

        connect_to_db(app, db_uri="postgresql:///test-db")

    def test_get_given_week_for_user(self):
        """Test get_given_week_for_user."""

        lucy = User.query.get(1)

        start_date = date.today() - timedelta(days = 13)
        lucy_week = crud.get_given_week_for_user(
            lucy.user_id,
            start_date
        )

        self.assertIsInstance(lucy_week, list)
        day1_entry = lucy_week[0]
        if day1_entry:
            self.assertIsInstance(day1_entry, DiaryEntry)
            self.assertIsInstance(day1_entry.urge_entries[0], UrgeEntry)
            self.assertIsInstance(day1_entry.action_entries[0], ActionEntry)
            self.assertEqual(day1_entry.dt.date(), start_date)
        

if __name__ == '__main__':
    from server import app
    unittest.main()