from client_pre_socket import *
from client_packet import *
from threading import Thread
import time


class ClientSocket(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dead = False
        self.start()

    def run(self):
        udp_listen_socket.bind(("localhost", udp_listen_port))
        print("udp listening at " + str(udp_listen_port))
        while not self.dead:
            try:
                data, addr = udp_listen_socket.recvfrom(1024)
            except:
                print("udp stopped")
            packets = disassemble_packet(data.decode())

            if packets[0] == "map_player_position":
                test_world.update_player_position_by_packets(packets[1])
            elif packets[0] == "map_new_player":
                test_world.add_new_players_by_packets(packets[1])
            elif packets[0] == "info_my_id":
                env_vars["my_id"] = packets[1][0].get("my_id")
            elif packets[0] == "map_load":
                test_world.add_map_items(packets[1])
            elif packets[0] == "map_remove_player":
                test_world.remove_player(packets[1])
            elif packets[0] == "player_backpack_info":
                test_backpack.update_items(packets[1])
            elif packets[0] == "map_remove_item":
                test_world.remove_item(packets[1][0].get("id"))
            elif packets[0] == "pack_add_item":
                test_backpack.add_item(packets[1][0].get("name"), packets[1][0].get("count"))

    def stop(self):
        self.dead = True
        udp_listen_socket.close()


class TcpSocket(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.dead = False
        self.server_tcp_port = 13412
        self.start()

    def run(self):
        print("tcp socket started")
        tcp_listen = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_listen.connect((host, self.server_tcp_port))

        hello_packet = "udp_port=" + str(udp_listen_port) + ";Player"

        tcp_listen.send(hello_packet.encode())
        print("sent udp port")
        while not self.dead:
            for i in range(len(tcp_queue)):
                tcp_listen.send(tcp_queue.pop().encode())
            time.sleep(0.03)
        print("tcp stopped")

    def stop(self):
        self.dead = True

