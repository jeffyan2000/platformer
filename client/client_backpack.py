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
        count = int(count)
        if self.count != count:
            self.count_img = item_font.render(str(count), False, (0, 0, 0))
        self.count = count

    def draw(self, x, y):
        if self.name:
            screen.blit(texture_lib["item_"+self.name], (x, y))
            screen.blit(self.count_img, (x + 7, y + 3))


ITEM_BY_ID = {
    "1": "grass",
    "2": "melon",
    "3": "stone",
    "4": "wood",
}
class Backpack:
    def __init__(self):
        self.width = 6
        self.slots = [[Item("", 0) for _ in range(6)] for _ in range(3)]

    def draw(self):
        if env_vars["opened_backpack"]:
            x, y = 5, 5
            for row in self.slots:
                x = 5
                for item in row:
                    screen.blit(texture_lib["itemslot1"], (x, y))
                    item.draw(x, y)
                    x += 55
                else:
                    y += 55
            self.draw_crafting()
        else:
            self.draw_row()

    def update_items(self, packets):
        for y in range(len(self.slots)):
            for x in range(len(self.slots[y])):
                if packets[x + y*self.width].get("name") != "0":
                    self.slots[y][x].name = ITEM_BY_ID[packets[x + y*self.width].get("name")]
                    self.slots[y][x].change_count(packets[x + y*self.width].get("count"))

    def add_item(self, item, count):
        for row in self.slots:
            for slot in row:
                if not slot.name:
                    slot.name = ITEM_BY_ID[item]
                    slot.change_count(count)
                    return
                elif slot.name == ITEM_BY_ID[item]:
                    slot.change_count(slot.count + int(count))
                    return

    def draw_row(self):
        x = 5
        for item in self.slots[0]:
            screen.blit(texture_lib["itemslot1"], (x, 5))
            item.draw(x, 5)
            x += 55

    def draw_crafting(self):
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(350, 10, 230, 300))
