# exceptions

from flask import jsonify


class ToothException(Exception):
    """generic base exception class for this project"""
    status_code = 400
    message = None

    def to_dict(self):
        return {"message": self.message, "status_code": self.status_code}


class NoUserId(ToothException):
    """exception thrown when there is no valid user id payload for token endpoint"""
    message = "No user id in payload"


class NoUserIdInToken(ToothException):
    """exception thrown when there is no valid user id in the parsed jwt token"""
    status_code = 401
    message = "JWT has no valid user id"


class InvalidEventType(ToothException):
    """exception thrown when there is an invalid event type in add event payload"""

    def __init__(self, enum_type):
        self.message = "Request payload has invalid event type: %s" % enum_type


class InvalidEventLevel(ToothException):
    """exception thrown when there is an invalid event level in add event payload"""

    def __init__(self, enum_level):
        self.message = "Request payload has invalid event level: %s" % enum_level


class InvalidJson(ToothException):
    """exception thrown when there is incorrectly formatted json in add event payload"""

    def __init__(self, json):
        self.message = "Request payload has invalid json: %s" % json


class InvalidDatetime(ToothException):
    """exception thrown when there is incorrectly formatted datetime in add event payload"""

    def __init__(self, datetime):
        self.message = "Request payload has invalid datetime: %s" % datetime


class InvalidToothId(ToothException):
    """exception thrown when there is incorrectly formatted datetime in add event payload"""

    def __init__(self, tooth_id):
        self.message = "Request payload has invalid tooth_id: %s" % tooth_id


def handle_exception(error):
    """handler to register all exceptions -- converts exception fields into a json that can be used as a response"""
    return jsonify(error.to_dict())
