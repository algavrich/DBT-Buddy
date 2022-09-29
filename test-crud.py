"""Unit tests for CRUD functions"""

from model import connect_to_db, db, User, Urge, Action
import crud
import unittest

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
        
        test_user = crud.create_user(
            "Test", "test@test.test", "testpassword",
            "1234567890", True, True, True
        )
        db.session.add(test_user)
        db.session.commit()

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()
        test_urge = crud.create_urge(test_user.user_id, "Test Urge")

        self.assertIsInstance(test_urge, Urge)
        self.assertEqual(test_urge.description, "Test Urge")
        self.assertEqual(test_urge.active, True)

    def test_create_action(self):
        """Test create_action."""

        test_user = crud.create_user(
            "Test", "test@test.test", "testpassword",
            "1234567890", True, True, True
        )
        db.session.add(test_user)
        db.session.commit()

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
            "Test", "test@test.test", "testpassword", "1234567890", True,
            True, True, "Urge1", "Urge2", "Urge3", "Action1", "Action2"
        )

        test_user = User.query.filter(
            User.email == "test@test.test"
        ).first()

        test_user_urges = []
        for urge in test_user.urges:
            test_user_urges.append(urge.description)

        test_user_actions = []
        for action in test_user.actions:
            test_user_actions.append(action.description)

        self.assertIsInstance(test_user, User)
        self.assertEqual(test_user.med_reminders, True)
        self.assertEqual(test_user_urges, ["Urge1", "Urge2", "Urge3"])
        self.assertEqual(test_user_actions, ["Action1", "Action2"])





if __name__ == '__main__':
    from server import app
    unittest.main()