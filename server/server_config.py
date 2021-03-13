import socket, threading, random, time, pygame
from server_packet import *
from server_types import *

BUFFER_SIZE = 2048
s_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

port = 13412

s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_tcp.bind(("localhost", port))
s_tcp.listen(5)
print("listening")

clock = pygame.time.Clock()

connect_sockets = {}
connect_id_list = []
