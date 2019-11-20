import re
from base64 import b64decode
from datetime import datetime
from django.conf import settings
from Crypto.Cipher import AES
from .models import GeoPoint
from hexdump import hexdump

def latlng_to_decimal(latlng: str, cardinal_direction: str) -> float:
    latlngregex = re.compile(
        r'(?P<degrees>\d+)(?P<minutes>\d{2}\.\d+)'
    )
    match = latlngregex.match(latlng)
    if not match:
        return 0
    degrees = int(match.group('degrees'))
    minutes = float(match.group('minutes'))
    sign = 1
    if(cardinal_direction.lower() in ('s', 'w')):
        sign = -1
    return sign * (degrees + minutes / 60.0)

def parse_data(data: bytes) -> GeoPoint:
    gpsregex = re.compile(
        r'^\+CGPSINF:\s*(?P<format>\d+),(?P<timeofday>\d+\.\d+),(?P<validity>\w),' +
        r'(?P<latitude>\d+\.\d+),(?P<southnorth>\w),(?P<longitude>\d+\.\d+),' +
        r'(?P<westeast>\w),(?P<speed>\d+\.\d+),(?P<course>\d+\.\d+),(?P<date>\d{6}),' + 
        r'(?P<variation>\d+\.\d+)?,(?P<variationwesteast>\w)?,\w\r\n.*$'
    )

    encryption_key = b64decode(settings.GPS_ENCRYPTION_KEY)
    aes = AES.new(encryption_key, AES.MODE_CBC, data[:AES.block_size])
    decrypted = aes.decrypt(data[AES.block_size:])
    decoded = decrypted.decode('ascii', errors='ignore')
    matches = gpsregex.match(decoded)
    if not matches:
        print('Data does not match regex: {}'.format(decoded))
        return
    print('Received valid line: {}'.format(decoded))
    
    return GeoPoint(
        dataformat=int(matches.group('format')),
        valid=matches.group('validity').upper() == 'A',
        latitude=latlng_to_decimal(matches.group('latitude'), matches.group('southnorth')),
        longitude=latlng_to_decimal(matches.group('longitude'), matches.group('westeast')),
        course=float(matches.group('course')),
        speed=float(matches.group('speed')),
        timestamp=datetime.strptime(
            '{} {} +0000'.format(matches.group('date'), matches.group('timeofday')),
            '%d%m%y %H%M%S.000 %z'
        )
    )

def handle_gps_packet(raw_data: bytes) -> None:
    point = parse_data(raw_data)
    if not point:
        return
    point.save()
    if point.valid:
        point.update_trip()
        point.save()

