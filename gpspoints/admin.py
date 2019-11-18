from django.conf import settings
from django.contrib import admin
from django.forms import ModelForm, TextInput

from .models import GeoPoint, Trip

@admin.register(GeoPoint)
class GeoPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'valid', 'latitude', 'longitude', 'speed', 'timestamp')

class GeoPointInline(admin.TabularInline):
    template = 'geopoint_inline_form.html'
    fields = ('id', 'valid', 'latitude', 'longitude', 'speed', 'timestamp')
    readonly_fields = ('id', 'timestamp')
    model = GeoPoint

    class Media:
        js = (
            'trip_admin.js',
            'https://maps.googleapis.com/maps/api/js?key={}'.format(
                settings.GOOGLE_MAPS_API_KEY),
            
        )

    def data_points_json(self):
        return 'manganga'

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('id', 'start', 'end', 'point_count')
    ordering = ('-start',)
    inlines = [ GeoPointInline ]

    def point_count(self, obj):
        return obj.points.count()
    point_count.short_description = 'Points'