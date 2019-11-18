from django.contrib import admin

from .models import GeoPoint, Trip

@admin.register(GeoPoint)
class GeoPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid', 'latitude', 'longitude', 'speed', 'timestamp')

@admin.register(Trip)
class TripAdin(admin.ModelAdmin):
    list_display = ('id', 'start', 'end', 'point_count')

    def point_count(self, obj):
        return obj.points.count()
    point_count.short_description = 'Points'