# various enums

from enum import Enum


class BaseEnum(Enum):
    """Base Enum classes that has names and values methods"""

    @classmethod
    def names(cls):
        return set(map(lambda c: c.name, cls))

    @classmethod
    def values(cls):
        return set(map(lambda c: c.value, cls))


class EventType(BaseEnum):
    """Enum for event type"""
    BRUSH = 1
    CAVITY = 2
    FLOSS = 3
    MOUTHWASH = 4
    TOOTHACHE = 5
    FALL = 6
    PLAQUE = 7
    STRAIGHTEN = 8
    WHITEN = 9
    CUSTOM = 10


class EventLevel(BaseEnum):
    """Enum for event level/severity"""
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class ToothType(BaseEnum):
    """Enum for tooth type. Often determined by the accompanying tooth id"""
    CANINE = 1
    INCISOR = 2
    PREMOLAR = 3
    MOLAR = 4
