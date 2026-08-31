# Game Configuration
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Player Stats
PLAYER_HEALTH = 130
PLAYER_DAMAGE = 5
PLAYER_SPEED = 5
PLAYER_SIZE = 40

# Enemy Base Stats
ENEMY_HEALTH_BASE = 30
ENEMY_HEALTH_ROLLER = 20
ENEMY_HEALTH_BIG_ROLLER = 35
BOSS_HEALTH = 130
BOSS_DAMAGE = 5

# Enemy Speeds
INSECT_SPEED = 2
FLYING_ENEMY_SPEED = 2.5
ROLLER_SPEED = 4
BIG_ROLLER_SPEED = 3

# Projectile Stats
PROJECTILE_SPEED = 7
PROJECTILE_SIZE = 8
PROJECTILE_DAMAGE = 5

# Game Phases
PHASE_COLORS = {
    1: {"ground": (139, 69, 19), "background": (34, 139, 34)},
    2: {"ground": (34, 139, 34), "background": (34, 139, 34)},
    3: {"ground": (128, 128, 128), "background": (34, 139, 34)},
    4: {"ground": (64, 64, 64), "background": (30, 30, 30)},
    5: {"ground": (139, 69, 19), "background": (50, 20, 20)},
}

# Difficulty Scaling
DIFFICULTY_MULTIPLIER = {
    0: 1.0,
    1: 2.0,
}

DAMAGE_MULTIPLIER = {
    0: 1.0,
    1: 1.4,
}
