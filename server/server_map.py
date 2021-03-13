from server_config import *
from server_map_generator import generate_by_setting


class Wall:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)


class MapItem(Packable):
    def __init__(self, tuple_item):
        self.id = tuple_item[0]
        self.name = tuple_item[1]
        self.x = tuple_item[2]
        self.y = tuple_item[3]

    def get_packet(self):
        return assemble_packet(self.id, self.name, self.x, self.y)


class World(Packable):
    def __init__(self):
        Packable.__init__(self)
        self.players = {}
        self.gravity = 0.6
        self.items = {}
        self.range = (0, 0)
        self.load_json(generate_by_setting(0))

    def load_json(self, json_map):
        self.range = json_map["map_range"]
        for item in json_map["map_items"]:
            self.items[item[0]] = MapItem(item)

    def get_packet(self):
        return "world packet"

    def get_map_packet(self):
        results = ["004"]
        for item in self.items:
            if len(results[-1] + self.items[item].get_packet()) < 900:
                results[-1] += self.items[item].get_packet()
            else:
                results.append("004")
                results[-1] += self.items[item].get_packet()
        return results

    def get_player_packets(self):
        if not self.players:
            return ""
        result = ""
        for playerID in self.players:
            result += self.players[playerID].get_packet()
        return assemble_header("001", result)

    def add_player(self, player):
        self.players[player.my_id] = player
        player.world = self

    def remove_player(self, player_id):
        del self.players[player_id]

    def update(self):
        for playerID in self.players:
            self.players[playerID].update()
