# simple unit tests of util functions

import datetime
import unittest

import enums
import exceptions
import models
import utils


class TestUtilityMethods(unittest.TestCase):
    def test_is_json(self):
        self.assertTrue(utils.is_json('{"hi": "my tooth hurts"}'))
        self.assertTrue(utils.is_json('{"hi": {"my tooth": "hurts"}}'))
        self.assertTrue(utils.is_json('{"this": {"number is": 3}}'))
        self.assertTrue(utils.is_json('{"this": {"list is": [1, 2, 3]}}'))
        self.assertTrue(utils.is_json("{}"))
        self.assertTrue(utils.is_json("[]"))
        self.assertFalse(utils.is_json(""))
        self.assertFalse(utils.is_json("asdf"))
        self.assertFalse(utils.is_json('{{"asdf": "qqqq"}'))

    def test_convert_datetime(self):
        test_dt = datetime.datetime(2022, 5, 17)
        self.assertIsNone(utils.convert_datetime(None))
        self.assertEquals(test_dt, utils.convert_datetime(1652770800))
        self.assertEquals(test_dt, utils.convert_datetime("2022-05-17T00:00:00"))
        self.assertEquals(test_dt, utils.convert_datetime(test_dt))
        self.assertRaises(exceptions.InvalidDatetime, utils.convert_datetime, "hello")
        self.assertIsNone(utils.convert_datetime("hello", raise_exc=False))

    def test_convert_event_enum(self):
        self.assertEquals(1, utils.convert_event_enum("BRUSH", enums.EventType))
        self.assertEquals(1, utils.convert_event_enum(1, enums.EventType))
        self.assertEquals(None, utils.convert_event_enum(None, enums.EventType))
        self.assertEquals(10, utils.convert_event_enum("CUSTOM", enums.EventType))
        self.assertEquals(1, utils.convert_event_enum("LOW", enums.EventLevel))

    def test_tooth_id_to_type(self):
        self.assertEquals(enums.ToothType.MOLAR, utils.TOOTH_ID_TO_TYPE[1])
        self.assertEquals(enums.ToothType.PREMOLAR, utils.TOOTH_ID_TO_TYPE[4])
        self.assertEquals(enums.ToothType.CANINE, utils.TOOTH_ID_TO_TYPE[6])
        self.assertEquals(enums.ToothType.INCISOR, utils.TOOTH_ID_TO_TYPE[7])

    def test_event_as_dict(self):
        test_event = models.Event(
            user_id=1,
            event_id=1,
            dt=datetime.datetime(2022, 5, 17),
            event_type=2,
            event_level=2,
            metadata_json={"tooth": "metadata"},
            tooth_id=3,
            tooth_type=4,
        )
        expected_event_dict = {
            "user_id": 1,
            "event_id": 1,
            "dt": "2022-05-17T00:00:00",
            "event_type": 2,
            "event_level": 2,
            "metadata_json": {"tooth": "metadata"},
            "tooth_id": 3,
            "tooth_type": 4,
        }
        self.assertEquals(expected_event_dict, utils.event_as_dict(test_event))
        expected_event_dict["event_type"] = "CAVITY"
        expected_event_dict["event_level"] = "MEDIUM"
        expected_event_dict["tooth_type"] = "MOLAR"
        self.assertEquals(expected_event_dict, utils.event_as_dict(test_event, verbose=True))
