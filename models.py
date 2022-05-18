# model definitions for the tooth project

import datetime

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Event(db.Model):
    """Model definition for event object"""
    event_id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime, nullable=True, default=datetime.datetime.utcnow)
    event_type = db.Column(db.Integer, nullable=True)
    event_level = db.Column(db.Integer, nullable=True)
    metadata_json = db.Column(db.JSON, nullable=True)
    tooth_id = db.Column(db.Integer, nullable=True)
    tooth_type = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.Integer, nullable=False)
