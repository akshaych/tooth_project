# utils for all modules

import datetime
import json

import enums
import exceptions
import models


TOOTH_ID_TO_TYPE = {
    1: enums.ToothType.MOLAR,
    2: enums.ToothType.MOLAR,
    3: enums.ToothType.MOLAR,
    4: enums.ToothType.PREMOLAR,
    5: enums.ToothType.PREMOLAR,
    6: enums.ToothType.CANINE,
    7: enums.ToothType.INCISOR,
    8: enums.ToothType.INCISOR,
    9: enums.ToothType.INCISOR,
    10: enums.ToothType.INCISOR,
    11: enums.ToothType.CANINE,
    12: enums.ToothType.PREMOLAR,
    13: enums.ToothType.PREMOLAR,
    14: enums.ToothType.MOLAR,
    15: enums.ToothType.MOLAR,
    16: enums.ToothType.MOLAR,
    17: enums.ToothType.MOLAR,
    18: enums.ToothType.MOLAR,
    19: enums.ToothType.MOLAR,
    20: enums.ToothType.PREMOLAR,
    21: enums.ToothType.PREMOLAR,
    22: enums.ToothType.CANINE,
    23: enums.ToothType.INCISOR,
    24: enums.ToothType.INCISOR,
    25: enums.ToothType.INCISOR,
    26: enums.ToothType.INCISOR,
    27: enums.ToothType.CANINE,
    28: enums.ToothType.PREMOLAR,
    29: enums.ToothType.PREMOLAR,
    30: enums.ToothType.MOLAR,
    31: enums.ToothType.MOLAR,
    32: enums.ToothType.MOLAR
}


def add_event(**kwargs):
    """adds event to database based on key word arguments given"""
    event = models.Event(**kwargs)
    models.db.session.add(event)
    models.db.session.commit()
    return event_as_dict(event)


def get_events_by_user(user_id, start_dt=None, end_dt=None, event_type=None, event_level=None, verbose=False):
    """gets events by user_id -- converting function arguments appropriately"""
    query = models.Event.query.filter(models.Event.user_id == user_id)
    start_dt = convert_datetime(start_dt, raise_exc=False)
    end_dt = convert_datetime(end_dt, raise_exc=False)
    event_type = convert_event_enum(event_type, enums.EventType)
    event_level = convert_event_enum(event_level, enums.EventLevel)
    if start_dt:
        query = query.filter(models.Event.dt > start_dt)
    if end_dt:
        query = query.filter(models.Event.dt < end_dt)
    if event_type:
        query = query.filter(models.Event.event_type == event_type)
    if event_level:
        query = query.filter(models.Event.event_level == event_level)
    events = query.all()
    return [event_as_dict(e, verbose) for e in events]


def convert_datetime(dt, raise_exc=True):
    """converts datetime if isoformat or timestamp. throws exception by default and returns None otherwise"""
    if dt is None or isinstance(dt, datetime.datetime):
        return dt
    try:
        if isinstance(dt, str):
            dt = datetime.datetime.fromisoformat(dt)
        else:
            dt = datetime.datetime.fromtimestamp(dt)
    except Exception:
        if raise_exc:
            raise exceptions.InvalidDatetime(dt)
        return None
    return dt


def convert_event_enum(element, enum):
    """converts given element argument into enum value based on the enum provided"""
    if isinstance(element, str):
        if element.upper() in enum.names():
            element = enum[element].value
    return element


def event_as_dict(e, verbose=False):
    """converts event model object into dict. if verbose flag is set, returns enum names instead of values"""
    return {
        "user_id": e.user_id,
        "event_id": e.event_id,
        "dt": e.dt.isoformat(),
        "event_type": enums.EventType(e.event_type).name if verbose and e.event_type else e.event_type,
        "event_level": enums.EventLevel(e.event_level).name if verbose and e.event_level else e.event_level,
        "metadata_json": e.metadata_json,
        "tooth_id": e.tooth_id,
        "tooth_type": enums.ToothType(e.tooth_type).name if verbose and e.tooth_type else e.tooth_type,
    }


def is_json(json_str):
    """delineates whether argument json string is actually json"""
    if isinstance(json_str, dict):
        return True
    try:
        json.loads(json_str)
    except Exception:
        return False
    return True
