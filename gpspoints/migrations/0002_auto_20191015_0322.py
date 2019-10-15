# Generated by Django 2.2.6 on 2019-10-15 03:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gpspoints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geopoint',
            name='dataformat',
            field=models.IntegerField(choices=[(0, 'Default (0)'), (32, '$GPRMC (32)')], default=32, verbose_name='Data format'),
        ),
        migrations.AlterField(
            model_name='geopoint',
            name='speed',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Speed'),
        ),
        migrations.AlterField(
            model_name='geopoint',
            name='valid',
            field=models.BooleanField(default=True, verbose_name='Data is valid'),
        ),
    ]