from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

DATA_FORMAT_CHOICES = [
    (0, 'Default (0)'),
    (32, '$GPRMC (32)'),
]

class GeoPoint(models.Model):
    dataformat = models.IntegerField('Data format', choices=DATA_FORMAT_CHOICES, default=32)
    valid = models.BooleanField('Data is valid', default=True)
    latitude = models.FloatField('Latitude', validators=(MinValueValidator(-90), MaxValueValidator(90)))
    longitude = models.FloatField('Longitude', validators=(MinValueValidator(-180), MaxValueValidator(180)))
    speed = models.FloatField('Speed', validators=(MinValueValidator(0),), default=0)
    timestamp = models.DateTimeField('GPS Timestamp')
    created_at = models.DateTimeField(auto_now=True)
