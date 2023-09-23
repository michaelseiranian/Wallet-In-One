import unittest
from datetime import datetime, timezone
from ...services import iso8601_to_datetime


class TestIso8601ToDatetime(unittest.TestCase):

    def test_iso8601_to_datetime(self):

        iso_string = '2022-03-22 12:00:00.000000+00:00'
        expected_dt = datetime(2022, 3, 22, 12, 0, 0, tzinfo=timezone.utc)
        self.assertEqual(iso8601_to_datetime(iso_string), expected_dt)

        iso_string = '2022-03-22 12:00:00+00:00'
        with self.assertRaises(ValueError):
            iso8601_to_datetime(iso_string)