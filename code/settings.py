# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
MAX_DT = 0.05  # s, caps the frame time so a hitch can't make sprites skip through each other

# Size of every sprite relative to its original size in the atlas
SPRITE_SCALE = 1.0

# Speeds are in pixels per second and times in seconds

# Player
PLAYER_SPEED = 300
PLAYER_LIVES = 3
PLAYER_LASER_SPEED = -480
PLAYER_LASER_COOLDOWN = 0.6

# Ufo fleet
UFO_ROW_COLORS = ['yellow', 'green', 'red']
UFO_SPRITES = {'red': 'ufoRed', 'yellow': 'ufoYellow', 'green': 'ufoGreen'}
UFO_COLS = 5
UFO_X_DISTANCE = 120
UFO_Y_DISTANCE = 120
UFO_X_OFFSET = 50
UFO_Y_OFFSET = 130
UFO_SPEED = 60
UFO_DROP = 3  # px per edge hit
UFO_POINTS = {'red': 10, 'yellow': 20, 'green': 30}
UFO_LASER_SPEED = 360
UFO_LASER_INTERVAL = 0.8

# Bonus alien
ALIEN_SPEED = 180
ALIEN_Y = 15
ALIEN_POINTS = 100
ALIEN_FIRST_SPAWN = (0.7, 1.3)  # random delay range
ALIEN_SPAWN = (6.7, 13.3)  # random delay range

# Obstacles
OBSTACLE_AMOUNT = 4
OBSTACLE_Y = 650

# CRT effect
CRT_LINE_HEIGHT = 3
CRT_ALPHA = (80, 90)
