from django.core.management.base import BaseCommand, CommandError
from gpspoints import gps_server

class Command(BaseCommand):
    help = 'Run the GPS Server for receiving points'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help="IP to listen to")
        parser.add_argument('port', type=int, help="Port to listen to")

    def handle(self, *args, **options):
        gps_server.serve(options['ip'], options['port'])
