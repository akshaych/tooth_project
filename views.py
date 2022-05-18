# view definitions

import datetime

from flask import request
from flask import jsonify

import flask_jwt_extended as flask_jwt

import enums
import exceptions
import utils


def token():
    """constructs and returns a jwt token back to the frontend if valid user_id is present in payload"""
    user_id = request.json.get("user_id", None)
    if not user_id:
        raise exceptions.NoUserId
    access_token = flask_jwt.create_access_token(identity=user_id)
    return jsonify(access_token=access_token)


@flask_jwt.jwt_required()
def add_event():
    """adds tooth related event. requires a jwt token to post a valid request"""
    request_json = request.json
    user_id = flask_jwt.get_jwt_identity()
    if not user_id:
        raise exceptions.NoUserIdInToken
    dt = utils.convert_datetime(request_json.get("datetime")) or datetime.datetime.utcnow()
    event_type = utils.convert_event_enum(request_json.get("event_type"), enums.EventType)
    if event_type not in enums.EventType.values():
        raise exceptions.InvalidEventType(event_type)
    event_level = utils.convert_event_enum(request_json.get("event_level"), enums.EventLevel)
    if event_level not in enums.EventLevel.values():
        raise exceptions.InvalidEventLevel(event_level)
    metadata_json = request_json.get("metadata_json")
    if not utils.is_json(metadata_json):
        raise exceptions.InvalidJson(metadata_json)
    tooth_id = request_json.get("tooth_id")
    tooth_type = None
    if tooth_id:
        if tooth_id not in utils.TOOTH_ID_TO_TYPE.keys():
            raise exceptions.InvalidToothId(tooth_id)
        tooth_type = utils.TOOTH_ID_TO_TYPE[tooth_id].value
    event_kwargs = {
        "dt": dt,
        "event_type": event_type,
        "event_level": event_level,
        "tooth_id": tooth_id,
        "tooth_type": tooth_type,
        "metadata_json": metadata_json,
        "user_id": user_id,
    }
    event = utils.add_event(**event_kwargs)
    return jsonify(**event), 201


@flask_jwt.jwt_required()
def get_events():
    """
    get all events for the user in the jwt token. can parametrize by start_dt, end_dt, event_type and verbose.
    requires a jwt token for access to endpoint.
    """
    args = request.args.to_dict()
    user_id = flask_jwt.get_jwt_identity()
    if not user_id:
        raise exceptions.NoUserIdInToken
    events = utils.get_events_by_user(
        user_id,
        start_dt=args.get("start_dt"),
        end_dt=args.get("end_dt"),
        event_type=args.get("event_type"),
        event_level=args.get("event_level"),
        verbose=args.get("verbose"),
    )
    return jsonify(events), 200
