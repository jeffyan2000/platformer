import socket, pygame, threading, random, os

pygame.init()


host = "localhost"
udp_listen_port = random.randint(20100, 21100)
udp_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

clock = pygame.time.Clock()

screen_size = (600, 400)
screen = pygame.display.set_mode(screen_size)

env_vars = {"mouse_x": 0, "mouse_y": 0, "delta_time": 0, "delta_x": 0, "delta_y": 0,
            "mouse_button_down": False, "mouse_button_changed": False, "keys": pygame.key.get_pressed(),
            "in_battle": False, "my_id": 0, "opened_backpack": False}

tcp_queue = []

# Texture --------------------------------------------------------------------------------------------------------------

textures = os.listdir("textures")
texture_lib = {}


def load(n):
    return pygame.image.load(os.path.join("textures", n + ".png")).convert_alpha()


def add_left(names):
    for name in names:
        texture_lib[name+"_left"] = pygame.transform.flip(texture_lib[name], True, False)


texture_names = [name[:-4] for name in textures]
for name in texture_names:
    texture_lib[name] = load(name)

add_left(("player_stand", "player_walk"))

name_font = pygame.font.SysFont('Comic Sans MS', 15)
item_font = pygame.font.SysFont('Comic Sans MS', 12)

PLAYER_SIZE = 75

draw_offset = [0, 0]
screen_offset = [screen_size[0]/2 - PLAYER_SIZE/2, screen_size[1]*3/5 - PLAYER_SIZE/2]
pygame.mouse.set_visible(False)
