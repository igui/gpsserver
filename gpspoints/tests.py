from django.test import TestCase
from gpspoints.models import Trip, GeoPoint
from datetime import datetime, timedelta
from pytz import utc

# Create your tests here.

class GeoPointTestCase(TestCase):
    def setUp(self):
        self.timestamp = datetime(2019,4,21,17,50, tzinfo=utc)
        self.tripstart = datetime(2019,4,21,14,00, tzinfo=utc)
        self.tripend = datetime(2019,4,21,15,45, tzinfo=utc)
        self.point = GeoPoint.objects.create(
            latitude=40,
            longitude=60,
            timestamp=self.timestamp
        )
        self.trip = Trip.objects.create(start=self.tripstart, end=self.tripend)

    def test_no_trip(self):
        """Test no Trip"""
        self.assertIsNone(self.point.trip, None)

    def test_update_trip_no_trip(self):
        self.point.update_trip()
        self.assertIsNotNone(self.point.trip)
        self.assertGreaterEqual(self.point.trip.start, self.point.timestamp)
        self.assertLessEqual(self.point.trip.end, self.point.timestamp)

    def test_update_trip_with_save(self):
        self.point.timestamp = self.tripstart + timedelta(minutes=3)
        self.point.save()
        self.point.refresh_from_db()
        self.point.update_trip()
        self.assertEqual(self.point.trip, self.trip)

    def test_update_trip_including(self):
        self.point.timestamp = self.tripstart + timedelta(minutes=3)
        self.point.update_trip()
        self.assertEqual(self.point.trip, self.trip)

    def test_update_trip_start(self):
        self.point.timestamp = self.tripstart
        self.point.update_trip()
        self.assertEqual(self.point.trip, self.trip)

    def test_update_trip_end(self):
        self.point.timestamp = self.tripend
        self.point.update_trip()
        self.assertEqual(self.point.trip, self.trip)
    
    def test_update_trip_in_threshold(self):
        past_end = self.tripend + timedelta(minutes=3)
        self.point.timestamp = past_end
        self.point.update_trip()
        self.assertEqual(self.point.trip, self.trip)
        self.assertEqual(self.point.trip.end, past_end)

