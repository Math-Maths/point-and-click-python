from pgzhelper import Actor, keyboard
import pgzrun

#---------------- CONSTANTS ----------------#
# Game resolution settings
WIDTH = 512
HEIGHT = 288
TILE_SIZE = 16

# Map layers
background_tiles = []
scenario_tiles = []
object_tiles = []

#---------------- ENTITIES ----------------#
# Player Creation
player = Actor("player/tile_0000")
player.pos = (WIDTH // 2, HEIGHT // 2)
player.speed = 2
player.facing_right = True
player.anim_timer = 0
player.frame = 0

player_right_walk_frames = [
    "player/tile_0000",
    "player/tile_0001",
]

player_left_walk_frames = [
    "player/tile_0004",
    "player/tile_0005",
]

player_right_idle_frames = [ 
    "player/tile_0000",
    "player/tile_0007",
    "player/tile_0000",
    "player/tile_0008"
]

player_left_idle_frames = [
    "player/tile_0004",
    "player/tile_0006",
    "player/tile_0004",
    "player/tile_0009"
]
# END - Player creation

# Cursor creation
cursor = Actor("cursor/tile_0025")
cursor.pos = (WIDTH // 2, HEIGHT // 2)
# END - Cursor creation

#---------------- FUNCTIONS ----------------#
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


#---------------- LEVEL LOADING ------------------#
background_tiles = load_level("level_1_background")
scenario_tiles = load_level("level_1_scenario")
object_tiles = load_level("level_1_objects")

#---------------- UPDATE -------------------------#
def update():
    # Player movement and animation
    move_x = 0
    move_y = 0
    moving = False

    if keyboard.a:
        move_x -= player.speed
        #player.facing_right = False
        moving = True

    if keyboard.d:
        move_x += player.speed
        #player.facing_right = True
        moving = True

    if keyboard.w:
        move_y -= player.speed
        moving = True

    if keyboard.s:
        move_y += player.speed
        moving = True

    player.x += move_x
    player.y += move_y

    if moving:
        player.anim_timer += 1
        if player.anim_timer >= 10:
            player.anim_timer = 0
            if player.facing_right:
                player.frame = (player.frame + 1) % len(player_right_walk_frames)
                player.image = player_right_walk_frames[player.frame]
            else:
                player.frame = (player.frame + 1) % len(player_left_walk_frames)
                player.image = player_left_walk_frames[player.frame]
    else:
        player.anim_timer += 1
        if player.anim_timer >= 15:
            player.anim_timer = 0
            if player.facing_right:
                player.frame = (player.frame + 1) % len(player_right_idle_frames)
                player.image = player_right_idle_frames[player.frame]
            else:
                player.frame = (player.frame + 1) % len(player_left_idle_frames)
                player.image = player_left_idle_frames[player.frame]
    #END - Player movement and animation

def on_mouse_move(pos):
    player_position = player.pos
    mouse_x, mouse_y = pos

    cursor.pos = pos

    if mouse_x < player_position[0]:
        player.facing_right = False
    else:
        player.facing_right = True



#---------------- PIECES CREATION ----------------#
def draw():
    screen.clear()

    for tile in background_tiles:
        tile.draw()

    for tile in scenario_tiles:
        tile.draw()

    for tile in object_tiles:
        tile.draw()

    player.draw()
    cursor.draw()

pgzrun.go()
