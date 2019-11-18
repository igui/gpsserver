from django.db import models
from django.core.serializers import serialize
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import timedelta

DATA_FORMAT_CHOICES = [
    (0, 'Default (0)'),
    (32, '$GPRMC (32)'),
]

class Trip(models.Model):
    TRIP_END_THRESHOLD = timedelta(minutes=10)

    start = models.DateTimeField('Start time')
    end = models.DateTimeField('End time')

    def points_json(self):
        return serialize('json', self.points.filter(valid=True))

    def __str__(self):
        return 'Trip<{}<-->{}>'.format(
            self.start.isoformat(),
            self.end.isoformat()
        )

class GeoPoint(models.Model):
    dataformat = models.IntegerField('Data format', choices=DATA_FORMAT_CHOICES, default=32)
    valid = models.BooleanField('Data is valid', default=True)
    latitude = models.FloatField('Latitude', validators=(MinValueValidator(-90), MaxValueValidator(90)))
    longitude = models.FloatField('Longitude', validators=(MinValueValidator(-180), MaxValueValidator(180)))
    speed = models.FloatField('Speed', validators=(MinValueValidator(0),), default=0)
    course = models.FloatField('Course', validators=(MinValueValidator(0), MaxValueValidator(360)), default=0)
    timestamp = models.DateTimeField('GPS Timestamp')
    created_at = models.DateTimeField(auto_now=True)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='points', null=True)

    def __str__(self):
        if self.valid:
            return 'GeoPoint<id={} latlng={},{}>'.format(self.id, self.latitude, 
                self.longitude)
        else:
            return 'GeoPoint<id={} invalid>'.format(self.id)

    def update_trip(self):
        """
        Updates the trip of the object, and extends the trip to contain the point
        if there is a trip within the threshold
        """
        trip = Trip.objects.filter(
            start__lte = self.timestamp,
            end__gte = self.timestamp - Trip.TRIP_END_THRESHOLD).first()
        if not trip: 
            trip = Trip.objects.create(start=self.timestamp, end=self.timestamp)
        elif trip.end < self.timestamp:
            trip.end = self.timestamp
            trip.save()

        self.trip = trip