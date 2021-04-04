import random

setting_1 = {
    "map_items": (
        ("tree1", 4),
        ("rock1", 1),
        ("tall_grass1", 8),
        ("flower1", 2),
        ("melon1", 2),
        ("melon2", 1)
    ),
    "map_range": (-800, 800)
}

settings = [setting_1]


def generate_by_setting(setting_id):
    setting = settings[setting_id]
    result = {"map_range": setting["map_range"], "map_items": []}
    item_id = 0
    for item in setting["map_items"]:
        for count in range(item[1]):
            result["map_items"].append((str(item_id), item[0],
                                       random.randint(setting["map_range"][0], setting["map_range"][1]), 275))
            item_id += 1
    return result

