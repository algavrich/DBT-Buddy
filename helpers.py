"""Helper functions for DBT Buddy"""

from model import Urge, Action, DiaryEntry
import crud
from typing import TypeVar
from datetime import datetime, date, timedelta
import re
from argon2 import PasswordHasher

UA = TypeVar("UA", Urge, Action)

ph = PasswordHasher()

def convert_radio_to_bool(s: str) -> bool:
    """Convert a radio value to boolean.
    
    Takes in a string ('yes' or 'no'),
    returns True if string is 'yes',
    returns False if string is 'no'.

    >>> convert_radio_to_bool('yes')
    True
    >>> convert_radio_to_bool('no')
    False
    >>> convert_radio_to_bool('foo')
    False
    >>> convert_radio_to_bool(3)
    False

    """
    
    if type(s) == str:
        return s == "yes"

    return False


def convert_bool_to_y_n(value: bool) -> str:
    """Convert a boolean value to yes or no.
    
    Takes in a boolean value,
    returns "yes" if value is True,
    returns "no" if value is False.

    >>> convert_bool_to_y_n(True)
    'yes'
    >>> convert_bool_to_y_n(False)
    'no'
    >>> convert_bool_to_y_n('x')
    'invalid input'

    """
    
    if type(value) == bool:
        if value:
            return "yes"
        
        return "no"
    
    return "invalid input"


def given_week_dates(date_string):
    """Return dictionary of date strings for the given week."""

    start_date = datetime.strptime(date_string, "%d_%m_%Y").date()

    date_strings = []

    for i in range(7):
        current_day = start_date + timedelta(days=i)
        date_strings.append({"date": date.strftime(current_day, "%b %-d")})

    return date_strings


def check_for_entry_in_week(entries):
    for entry in entries:
        if entry:
            return True
    return False


def get_descs_from_object_list(objects: list[UA]) -> list[str]:
    """Get descriptions from list of user's custom Urge or Action object.
    
    Takes in a list of Urge or Action objects,
    Returns a list of their descriptions.
    """
    
    descriptions = []

    for object in objects:
        descriptions.append(object.description)

    return descriptions


def order_urge_entries(urge_entries):
    """Orders list of urge entries."""

    for urge_entry in urge_entries:
        if urge_entry.urge.position == 1:
            urge_entry1 = urge_entry
        elif urge_entry.urge.position == 2:
            urge_entry2 = urge_entry
        else:
            urge_entry3 = urge_entry

    return [urge_entry1, urge_entry2, urge_entry3]


def order_action_entries(action_entries):
    """Orders list of action entries."""

    for action_entry in action_entries:
        if action_entry.action.position == 1:
            action_entry1 = action_entry
        else:
            action_entry2 = action_entry

    return [action_entry1, action_entry2]


def dict_for_day(entry: DiaryEntry) -> dict:
    """Create dictionary of info for given diary entry."""

    ordered_urge_entries = order_urge_entries(
        entry.urge_entries
    )
    ordered_action_entries = order_action_entries(
        entry.action_entries
    )

    return {
        "date": datetime.strftime(entry.dt, "%A %d"),
        "sad score": entry.sad_score,
        "angry score": entry.angry_score,
        "fear score": entry.fear_score,
        "happy score": entry.happy_score,
        "shame score": entry.shame_score,
        "urge1 name": crud.get_urge_desc_by_id(
            ordered_urge_entries[0].urge_id),
        "urge2 name": crud.get_urge_desc_by_id(
            ordered_urge_entries[1].urge_id),
        "urge3 name": crud.get_urge_desc_by_id(
            ordered_urge_entries[2].urge_id),
        "urge1 score": ordered_urge_entries[0].score,
        "urge2 score": ordered_urge_entries[1].score,
        "urge3 score": ordered_urge_entries[2].score,
        "action1 name": crud.get_action_desc_by_id(
            ordered_action_entries[0].action_id),
        "action2 name": crud.get_action_desc_by_id(
            ordered_action_entries[1].action_id),
        "action1 score": convert_bool_to_y_n(
            ordered_action_entries[0].score),
        "action2 score": convert_bool_to_y_n(
            ordered_action_entries[1].score),
        "skills used": entry.skills_used
    }


def make_entries_jsonifiable(
        entries_as_objs: list[DiaryEntry]) -> list[dict]:
    """Turn list of entry objects into list of dicts.
    
    Takes in a list (week) of DiaryEntry obejcts,
    returns a list of dictionaries of info from those entries.
    
    """

    entries = []
    for entry in entries_as_objs:
        if entry is not None:
            entry_contents = dict_for_day(entry)
        else:
            entry_contents = None
        entries.append(entry_contents)

    return entries


def extract_phone_number(s: str) -> str:
    """Extracts digits of phone number from various formats."""

    x = re.search(
        "^[(]?([0-9]{3})[)]?[-\s\.]?([0-9]{3})[-\s\.]?([0-9]{4})$",
        s
    )

    if x:
        return x.group(1) + x.group(2) + x.group(3)


def hash_pw(pw):
    """Hashe a password."""

    return ph.hash(pw)


def verify_pw(hash, pw):
    """Verify a password."""

    return ph.verify(hash, pw)
