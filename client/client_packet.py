class Packet:
    def __init__(self):
        self.data = {}

    def get(self, key):
        return self.data[key]

    def set(self, key, value):
        self.data[key] = value


PACKET_TYPES = {
    "001": "map_player_position",
    "002": "map_new_player",
    "003": "info_my_id",
    "004": "map_load",
    "005": "map_remove_player",
}

PACKET_DATA = {
    "001": ("player_id", "pos_x", "pos_y", "frame"),
    "002": ("player_id", "player_name"),
    "003": ("my_id", ),
    "004": ("id", "name", "x", "y"),
    "005": ("player_id", ),
}


def disassemble_packet(text_string):
    packets = []
    header = text_string[:3]
    data = text_string[3:]
    splited = data.split("@")

    name = PACKET_TYPES[header]
    for segment in splited:
        if segment:
            values = segment.split(";")
            packet = Packet()
            for i, data_key in enumerate(PACKET_DATA[header]):
                packet.set(data_key, values[i])
            packets.append(packet)

    return name, packets
