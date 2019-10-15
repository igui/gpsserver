from socket import socket, AF_INET, SOCK_DGRAM
from .handle_gps_packet import handle_gps_packet

MAX_PACKAGE_SIZE = 4096

def serve(address: str, port: int):
    server = socket(AF_INET, SOCK_DGRAM)
    server.bind((address, port))
    print('Listening on {}:{}'.format(address, port))

    while True:
        raw_data, _address = server.recvfrom(MAX_PACKAGE_SIZE)
        handle_gps_packet(raw_data)
