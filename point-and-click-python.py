import pgzrun

# Screen resolution (change as needed)
WIDTH = 512
HEIGHT = 288

TILE_SIZE = 16
background_tiles = []
scenario_tiles = []

def load_level(filename):
    global background_tiles
    global scenario_tiles

    if filename == "level_1_background":
        background_tiles = []
    elif filename == "level_1_scenario":
        scenario_tiles = []

    with open(f"levels/{filename}.txt", "r") as file:
        rows = file.read().strip().splitlines()

    for y, row in enumerate(rows):
        cols = row.split(",")
        for x, tile_id in enumerate(cols):
            tile_id = tile_id.strip()

            if tile_id == "" or tile_id == "x":
                continue
            
            tile_id = int(tile_id)

            tile_name = f"scenario/tile_{tile_id:04d}"
            tile = Actor(tile_name)
            tile.topleft = (x * TILE_SIZE, y * TILE_SIZE)

            if filename == "level_1_background":
                background_tiles.append(tile)
            elif filename == "level_1_scenario":
                scenario_tiles.append(tile)

# 🔹 Load level on startup
load_level("level_1_background")
load_level("level_1_scenario")

def draw():
    screen.clear()

    for tile in background_tiles:
        tile.draw()

    for tile in scenario_tiles:
        tile.draw()

pgzrun.go()
