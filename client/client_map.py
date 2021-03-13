from client_config import *


class Player:
    def __init__(self, my_name):
        self.my_name = my_name
        self.pos = [0, 0]
        self.name_offset = (int(PLAYER_SIZE/2 - name_font.size(my_name)[0]/2), -name_font.size(my_name)[1])
        self.name_img = name_font.render(my_name, False, (0, 0, 0))
        self.frame = 0
        self.direction = ""

    def get_draw_pos(self):
        return self.pos[0] - draw_offset[0] + screen_offset[0], self.pos[1] - draw_offset[1] + screen_offset[1]

    def draw(self):
        pos = self.get_draw_pos()
        screen.blit(self.name_img, (pos[0] + self.name_offset[0], pos[1] + self.name_offset[1]))
        actual_frame = self.frame % 10
        if self.frame < 10:
            screen.blit(texture_lib["player_stand" + self.direction],
                        (pos[0], pos[1]),
                        pygame.Rect(0, actual_frame * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE))
        else:
            screen.blit(texture_lib["player_walk" + self.direction],
                        (pos[0], pos[1]),
                        pygame.Rect(0, actual_frame * PLAYER_SIZE, PLAYER_SIZE, PLAYER_SIZE))

    def update_position(self, new_x, new_y):
        self.pos[0] = int(new_x)
        self.pos[1] = int(new_y)


class WorldObject:
    def __init__(self, item_name, x, y):
        self.name = item_name
        self.pos = [int(x), int(y)]
        self.size = texture_lib[item_name].get_size()

    def get_draw_pos(self):
        return self.pos[0] - draw_offset[0] + screen_offset[0], \
               self.pos[1] - draw_offset[1] + screen_offset[1] - self.size[1]

    def draw(self):
        pos = self.get_draw_pos()
        if pos[0] < screen_size[0] and pos[0] + self.size[0] > 0:
            screen.blit(texture_lib[self.name], self.get_draw_pos())


class World:
    def __init__(self):
        self.players = {}
        self.objects = {}

    def draw(self):
        break_point_back = (-draw_offset[0]/3)%screen_size[0]
        break_point = (-draw_offset[0]) % screen_size[0]
        break_point_fore = (-draw_offset[0]*1.5) % screen_size[0]
        screen.blit(texture_lib["scroll_background1"], (break_point_back, 0),
                    pygame.Rect(0, 0, 600-break_point_back, 400))
        screen.blit(texture_lib["scroll_background1"], (0, 0),
                    pygame.Rect(600 - break_point_back, 0, break_point_back, 400))
        for object_id in self.objects:
            self.objects[object_id].draw()
        for player_id in self.players:
            self.players[player_id].draw()

        screen.blit(texture_lib["scroll_ground1"], (break_point, -draw_offset[1] + 203),
                    pygame.Rect(0, 0, 600 - break_point, 400))
        screen.blit(texture_lib["scroll_ground1"], (0, -draw_offset[1] + 203),
                    pygame.Rect(600 - break_point, 0, break_point, 400))

        screen.blit(texture_lib["scroll_foreground1"], (break_point_fore, 0),
                    pygame.Rect(0, 0, 600 - break_point_fore, 400))
        screen.blit(texture_lib["scroll_foreground1"], (0, 0),
                    pygame.Rect(600 - break_point_fore, 0, break_point_fore, 400))

    def update_player_position_by_packets(self, packets):
        for packet in packets:
            if packet.get("player_id") in self.players:
                if packet.get("player_id") == env_vars["my_id"]:
                    draw_offset[0] = int(packet.get("pos_x"))
                    draw_offset[1] = int(packet.get("pos_y"))
                self.players[packet.get("player_id")].update_position(packet.get("pos_x"), packet.get("pos_y"))
                if packet.get("frame")[0] == "0":
                    self.players[packet.get("player_id")].direction = "_left"
                else:
                    self.players[packet.get("player_id")].direction = ""
                self.players[packet.get("player_id")].frame = abs(int(packet.get("frame")[1:]))

    def add_new_players_by_packets(self, packets):
        for packet in packets:
            self.players[packet.get("player_id")] = Player(packet.get("player_name"))

    def add_map_items(self, packets):
        for packet in packets:
            self.objects[packet.get("id")] = WorldObject(packet.get("name"), packet.get("x"), packet.get("y"))

    def remove_player(self, packets):
        del self.players[packets[0].get("player_id")]
