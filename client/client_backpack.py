from client_config import *


class Item:
    """
    Item object in player's backpack.
    """
    def __init__(self, my_name, count):
        self.name = my_name
        self.count = count
        self.count_img = item_font.render(str(self.count), False, (0, 0, 0))

    def change_count(self, count):
        self.count = count
        self.count_img = item_font.render(str(self.count), False, (0, 0, 0))

    def draw(self, x, y):
        if self.name != "empty":
            screen.blit(texture_lib["item_"+self.name], (x, y))
            screen.blit(self.count_img, (x + 7, y + 3))


class Backpack:
    def __init__(self):
        self.slots = [[Item("empty", 0) for _ in range(6)] for _ in range(3)]
        self.slots[0][0] = Item("grass", 999)

    def draw(self):
        if env_vars["opened_backpack"]:
            x, y = 138, 10
            for row in self.slots:
                x = 138
                for item in row:
                    screen.blit(texture_lib["itemslot1"], (x, y))
                    item.draw(x, y)
                    x += 55
                if y == 10:
                    y += 100
                else:
                    y += 55
        else:
            self.draw_row()

    def draw_row(self):
        x = 5
        for item in self.slots[0]:
            screen.blit(texture_lib["itemslot1"], (x, 5))
            item.draw(x, 5)
            x += 55
