from django.contrib import admin

from .models import GeoPoint

@admin.register(GeoPoint)
class GeoPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid', 'latitude', 'longitude', 'speed', 'timestamp')
