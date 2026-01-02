from random import choice
import random
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
scenario_colliders = []
object_tiles = []
object_colliders = []

# Enemy Settings
enemies_list = []
enemy_spawn_positions = [
    (64, 112),
    (328, 96),
    (112, 192)

]

enemy_spawn_time = 0
enemy_spawn_interval = 300
enemy_speed = 1.5
enemy_life = 3;
enemies_image_paths = [
    "enemies/enemy_1/tile_0000",
    "enemies/enemy_2/tile_0004",
    "enemies/enemy_3/tile_0008"
]

# Enemy Animation Frames
enemy_1_right_walk_frames = [
    "enemies/enemy_1/tile_0000",
    "enemies/enemy_1/tile_0001",
]

enemy_1_left_walk_frames = [
    "enemies/enemy_1/tile_0002",
    "enemies/enemy_1/tile_0004",
]

enemy_2_right_walk_frames = [
    "enemies/enemy_2/tile_0004",
    "enemies/enemy_2/tile_0005",
]

enemy_2_left_walk_frames = [
    "enemies/enemy_2/tile_0006",
    "enemies/enemy_2/tile_0008",
]

enemy_3_right_walk_frames = [
    "enemies/enemy_3/tile_0008",
    "enemies/enemy_3/tile_0009",
]

enemy_3_left_walk_frames = [
    "enemies/enemy_3/tile_0010",
    "enemies/enemy_3/tile_0012",
]

# Player Creation
player = Actor("player/tile_0000")
player.pos = (WIDTH // 2, HEIGHT // 2)
player._anchor = (player.width // 2, player.height // 2)
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

# Weapon creation
weapon = Actor("weapon/tile_0005")
weapon.anchor = (-10, 10)
weapon.pos = (player.x, player.y)
# END - Weapon creation

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

def load_colliders(tiles):
    colliders = []

    for tile in tiles:
        collider = Actor(tile.image)
        collider.pos = (tile.x, tile.y)
        collider.width = 5
        collider.height = 5
        collider.center = tile.center
        colliders.append(collider)

    return colliders

#Collision Functions
def get_collision_tiles():
    return scenario_colliders + object_colliders

def collides_with_world(actor):
    for tile in get_collision_tiles():
        if actor.colliderect(tile):
            return True
    return False
# END - Collision Functions

# Enemy Functions
def create_enemy(pos, image_path, right_walk_frames, left_walk_frames):
    enemy = Actor(image_path)
    enemy.pos = pos
    enemy.speed = enemy_speed
    enemy.anim_timer = 0
    enemy.frame = 0
    enemy.moving = False
    enemy.life = enemy_life
    enemy.right_walk_frames = right_walk_frames
    enemy.left_walk_frames = left_walk_frames
    enemy.facing_right = True
    enemies_list.append(enemy)

def handle_enemy_spawning():
    global enemy_spawn_time

    enemy_spawn_time += 1
    if enemy_spawn_time >= enemy_spawn_interval:
        enemy_spawn_time = 0

        spawn_pos = random.choice(enemy_spawn_positions)
        random_index = random.randint(0, len(enemies_image_paths) - 1)
        random_enemy_image = enemies_image_paths[random_index]
        
        if random_index == 0:
            right_frames, left_frames = enemy_1_right_walk_frames, enemy_1_left_walk_frames
        elif random_index == 1:
            right_frames, left_frames = enemy_2_right_walk_frames, enemy_2_left_walk_frames
        else:
            right_frames, left_frames = enemy_3_right_walk_frames, enemy_3_left_walk_frames
        
        create_enemy(spawn_pos, random_enemy_image, right_frames, left_frames)

def update_enemies():
    for enemy in enemies_list:
        dx = player.x - enemy.x
        dy = player.y - enemy.y

        length = (dx ** 2 + dy ** 2) ** 0.5
        if length != 0:
            dx /= length
            dy /= length

        # Move X
        enemy.x += dx * enemy.speed
        if collides_with_world(enemy):
            enemy.x -= dx * enemy.speed

        # Move Y
        enemy.y += dy * enemy.speed
        if collides_with_world(enemy):
            enemy.y -= dy * enemy.speed

        enemy.moving = True

        if dx < 0:
            enemy.facing_right = False
        else:
            enemy.facing_right = True

        enemy.anim_timer += 1
        if enemy.anim_timer >= 10:
            enemy.anim_timer = 0
            if enemy.facing_right:
                enemy.frame = (enemy.frame + 1) % len(enemy.right_walk_frames)
                enemy.image = enemy.right_walk_frames[enemy.frame]
            else:
                enemy.frame = (enemy.frame + 1) % len(enemy.left_walk_frames)
                enemy.image = enemy.left_walk_frames[enemy.frame]
#---------------- LEVEL LOADING ------------------#
background_tiles = load_level("level_1_background")
scenario_tiles = load_level("level_1_scenario")
object_tiles = load_level("level_1_objects")

scenario_colliders = load_colliders(scenario_tiles)
object_colliders = load_colliders(object_tiles)

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

    # Move X
    player.x += move_x
    if collides_with_world(player):
        player.x -= move_x  # undo movement
    
    # Move Y
    player.y += move_y
    if collides_with_world(player):
        player.y -= move_y  # undo movement

    weapon.pos = (player.x, player.y)

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

    # Enemy spawning and updating
    handle_enemy_spawning()
    update_enemies()

def on_mouse_move(pos):
    player_position = player.pos
    mouse_x = pos[0]

    cursor.pos = pos
    weapon.angle = player.angle_to(pos)

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
    weapon.draw()

    for enemy in enemies_list:
        enemy.draw()


pgzrun.go()
