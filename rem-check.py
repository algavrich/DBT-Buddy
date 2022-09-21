"""Sends reminders to DBT Buddy users."""

import os
from twilio.rest import Client
import crud

account_sid = os.environ["TWILIO_ACCOUNT_SID"]
auth_token = os.environ["TWILIO_AUTH_TOKEN"]

client = Client(account_sid, auth_token)

def reminders():
    """Check for users who need reminders and send them."""

    users_entry_reminders = crud.get_users_entry_reminders()

    for user in users_entry_reminders:
        if (not crud.check_entry_past_24(user.user_id)
            and not crud.check_for_reminder(user.user_id)):
            message = " ".join([
                f"Hi {user.fname}!",
                "We noticed that you haven't made a",
                "diary card entry in the past day.",
                "Head to link to make one!"
            ])

            client.api.account.messages.create(
                to=f"+1{user.phone_number}",
                from_="+19855895115",
                body=message
            )
            # Threading, queue
            crud.add_new_rem_to_db(user.user_id)

if __name__ == '__main__':
    from server import app
    crud.connect_to_db(app, db_uri="postgresql:///test-db")
    reminders()