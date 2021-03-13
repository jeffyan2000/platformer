from server_config import *
from server_cycles import *


class PlayerCharacter(Packable):
    # states: stand, move, attack
    def __init__(self, my_id):
        Packable.__init__(self)

        self.my_id = my_id
        self.my_name = "Player" + str(self.my_id)
        self.pos = [0, 0]
        self.size = [30, 50]
        self.state = "stand"
        self.dead = False
        self.attacking = False
        self.vertical_speed = 0
        self.horizontal_speed = 3
        self.world = None
        self.jump_counter = 0
        self.jump_height = 10

        self.direction = "right"
        self.moving_direction = [0, 0]
        self.attack_stamps = (0, 2, 7, 10, 15)
        self.current_attack_stamp = 1
        self.cycles = {"stand": TimedCycle(4, (5, 5, 5, 5), 0),
                       "move": TimedCycle(8, (5, 5, 5, 5, 5, 5, 5, 5), 0),
                       "attack": TimedCycle(2, (5, 5, 10, 3, 1, 2, 5, 3, 10, 5, 15, 2, 1, 2, 20),
                                            (4, 5, 0, 15, 15, 4, 0, -2, -2, 0, 0, -30, -10, -1, 0))}

    def move_in_direction(self, dx, dy):
        self.pos[0] += dx * self.moving_direction[0] * self.world.delta_time
        if dy:
            self.pos[1] += dy * self.world.delta_time

    def is_on_ground(self):
        return self.pos[1] + self.vertical_speed > 200

    def get_frame(self):
        tick = str(self.cycles[self.state].get_frame())
        dir = ""
        if self.direction == "left":
            dir = "0"
        else:
            dir = "1"
        if self.state == "stand":
            return dir + tick
        elif self.state == "move":
            return dir + "1" + tick

    def get_packet(self):
        return assemble_packet(self.my_id, int(self.pos[0]), int(self.pos[1]), self.get_frame())

    def current_cycle(self):
        return self.cycles[self.state]

    def update(self):
        prev_pos = (self.pos[0], self.pos[1])

        if self.state == "stand":
            self.current_cycle().tick()
        elif self.state == "move":
            if not (self.moving_direction[0] or self.moving_direction[1]):
                self.switch_state("stand")
            else:
                self.current_cycle().tick()

        self.move_in_direction(self.horizontal_speed, self.vertical_speed)

        if self.world:
            if self.vertical_speed is not None:
                if self.is_on_ground():
                    self.pos[1] = 201
                    self.vertical_speed = None
                    self.jump_counter = 0
                else:
                    self.vertical_speed += self.world.gravity
            if self.pos[0] > self.world.range[1]:
                self.pos[0] = self.world.range[1]
            elif self.pos[0] < self.world.range[0]:
                self.pos[0] = self.world.range[0]

    def continue_attack(self):
        if self.attack_stamps[self.current_attack_stamp - 1] < self.current_cycle().frame < self.attack_stamps[
                self.current_attack_stamp]:
            self.current_attack_stamp += 1
            if self.current_attack_stamp < len(self.attack_stamps):
                self.current_cycle().max_frame = self.attack_stamps[self.current_attack_stamp]

    def switch_state(self, target_state):
        self.state = target_state
        self.cycles[target_state].reset()
        self.current_attack_stamp = 1

    def handle_keypress(self, key_event):
        if key_event[1]:
            if key_event[0] == "right":
                self.direction = "right"
                self.switch_state("move")
                self.moving_direction[0] = 1
            elif key_event[0] == "left":
                self.direction = "left"
                self.switch_state("move")
                self.moving_direction[0] = -1
            elif key_event[0] == "up":
                if self.jump_counter < 2:
                    self.vertical_speed = -self.jump_height
                    self.jump_counter += 1
        else:
            if self.state == "move":
                if key_event[0] == "right" and self.moving_direction[0] == 1:
                    self.moving_direction[0] = 0
                elif key_event[0] == "left" and self.moving_direction[0] == -1:
                    self.moving_direction[0] = 0


