from pgzhelper import Actor
import pgzrun

# Screen resolution (change as needed)
WIDTH = 512
HEIGHT = 288

TILE_SIZE = 16
background_tiles = []
scenario_tiles = []
object_tiles = []

def load_level(filename):
    tiles = []

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

            tiles.append(tile)

    return tiles
    

# 🔹 Load level on startup
background_tiles = load_level("level_1_background")
scenario_tiles = load_level("level_1_scenario")
object_tiles = load_level("level_1_objects")

def draw():
    screen.clear()

    for tile in background_tiles:
        tile.draw()

    for tile in scenario_tiles:
        tile.draw()

    for tile in object_tiles:
        tile.draw()

pgzrun.go()
