from server_prepacket import *
from server_packet import *
from server_player import PlayerCharacter
import datetime


class ClientSocket:
    def __init__(self, addr, my_id):
        self.addr = addr
        self.udp_port = 0
        self.player = PlayerCharacter(my_id)
        self.header = str(self.player.my_id)
        while len(self.header) < 4:
            self.header = "0" + self.header

    def id_packet(self):
        return assemble_header("002", assemble_packet(self.player.my_id, self.player.my_name))

    def set_udp_port(self, udp_port):
        self.udp_port = udp_port

    def is_udp_ready(self):
        return not self.udp_port == 0

    def send_udp(self, data):
        if self.is_udp_ready():
            s_udp.sendto(data.encode(), (self.addr[0], self.udp_port))

    def send_udps(self, data):
        for item in data:
            if self.is_udp_ready():
                s_udp.sendto(item.encode(), (self.addr[0], self.udp_port))


def handle_client_listener(client_socket, addr):
    my_id = random.randint(0, 100)
    while my_id in connect_sockets:
        my_id = random.randint(0, 1000)
    print("process  " + str(my_id) + " started")
    my_socket = ClientSocket(addr, my_id)
    my_player = my_socket.player

    world_test.add_player(my_socket.player)

    connect_sockets[my_id] = my_socket
    connect_id_list.append(my_id)

    while True:
        payload = client_socket.recv(BUFFER_SIZE).decode()
        if payload:
            if payload.startswith("udp_port"):
                payload = payload[9:].split(";")
                my_socket.set_udp_port(int(payload[0]))
                my_player.name = payload[1]
                my_socket.send_udp("003" + str(my_id))
                my_socket.send_udps(world_test.get_map_packet())
                for socket_id in connect_sockets:
                    my_socket.send_udp(connect_sockets[socket_id].id_packet())
                    if socket_id != my_id:
                        connect_sockets[socket_id].send_udp(my_socket.id_packet())
            elif payload.startswith("key"):
                key_event = payload[3:].split(";")
                key_event[1] = int(key_event[1])
                my_player.handle_keypress(key_event)
            else:
                print(payload)

        else:
            del connect_sockets[my_id]
            print("client disconnected")
            for socket_id in connect_sockets:
                connect_sockets[socket_id].send_udp("005" + str(my_id))
            world_test.remove_player(my_id)
            break


class BattleUpdateLoop(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.dead = False
        self.timed_map_update = 5
        self.timed_map_tick = 0
        self.start()

    def run(self):
        while not self.dead:
            world_test.delta_time = clock.tick(50)/20
            world_test.update()
            for i in range(len(connect_id_list)-1, -1, -1):
                socket_id = connect_id_list[i]
                if socket_id in connect_sockets:
                    packets = world_test.get_player_packets()
                    if packets:
                        connect_sockets[socket_id].send_udp(packets)
                else:
                    del connect_id_list[i]

    def stop(self):
        self.dead = True

