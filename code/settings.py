# Screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
MAX_DT = 0.05  # s, caps the frame time so a hitch can't make sprites skip through each other

# Size of every sprite relative to its original size in the atlas
SPRITE_SCALE = 0.6

# Speeds are in pixels per second and times in seconds

# Player
PLAYER_SPEED = 300
PLAYER_LIVES = 3
PLAYER_LASER_SPEED = -480
PLAYER_LASER_COOLDOWN = 0.6

# Enemy fleet
ENEMY_ROW_COLORS = ['black', 'blue', 'green', 'red']  # from the back row to the front
ENEMY_POINTS = {'red': 10, 'green': 20, 'blue': 30, 'black': 40}
ENEMY_MODELS = 5  # enemyRed1 to enemyRed5 in the atlas, and the same for every color
ENEMY_COLS = 6
ENEMY_X_DISTANCE = 90
ENEMY_Y_DISTANCE = 70
ENEMY_X_OFFSET = 50
ENEMY_Y_OFFSET = 120
ENEMY_SPEED = 60
ENEMY_DROP = 3  # px per edge hit
ENEMY_LASER_SPEED = 360
ENEMY_LASER_INTERVAL = 0.8
ENEMY_FLASH_TIME = 0.1  # how long an armored enemy flashes white when hit

# Waves
WAVE_SPEED_UP = 1.10  # fleet speed multiplier per wave
WAVE_FIRE_RATE_UP = 1.08  # fleet shots per second multiplier per wave
ARMORED_FROM_WAVE = 3  # from this wave on, the back row takes two hits
WAVE_BANNER_TIME = 1.5

# Bonus ufo
UFO_SPRITES = ['ufoRed', 'ufoGreen', 'ufoYellow', 'ufoBlue']
UFO_SPEED = 180
UFO_Y = 45
UFO_POINTS = 100
UFO_FIRST_SPAWN = (0.7, 1.3)  # random delay range
UFO_SPAWN = (6.7, 13.3)  # random delay range

# Obstacles
OBSTACLE_AMOUNT = 4
OBSTACLE_Y = 650

# Scenes
BLINK_PERIOD = 1.0  # s, for the blinking "press a key" prompts
OVERLAY_ALPHA = 180  # how much the pause and game over screens darken the game behind them

# CRT effect
CRT_LINE_HEIGHT = 3
CRT_ALPHA = (80, 90)
CRT_VIGNETTE_SIZE = 100  # px from the edge to where the darkening fades out
CRT_CORNER_RADIUS = 140  # px
