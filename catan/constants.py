import pygame

# screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

# colour constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
CYAN = (0, 255, 255)

# board constants
HEXAGON_RADIUS = 75
BUFFER = 10
GRID_SIZE = 5

# this is the x,y indices that we DO NOT want in our final board.
EXCLUDED_INDICES = [(0, 0), (0, 4), (4, 0), (4, 1), (4, 3), (4, 4)]

# fonts
pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 32)
TITLE_FONT = pygame.font.SysFont("comicsansms", 42)
NUMBER_FONT = pygame.font.SysFont("comicsansms", 30)

# menu assets
MENU_BG = pygame.image.load('assets/menu/Catan_BG.jpg')
MENU_BUTTON = pygame.image.load('assets/menu/Play Rect.png')

# numbers to be drawn on to tiles and their freq given 2x 6 sided die.
NUMBER_LIST = [
    2, 2,  # 2x
    3, 3, 3, 3,  # 4x
    4, 4, 4, 4,  # 4x
    5, 5, 5, 5, 5,  # 5x
    6, 6, 6, 6, 6, 6,  # 6x
    8, 8, 8, 8, 8, 8,  # 6x
    9, 9, 9, 9, 9,  # 5x
    10, 10, 10, 10  # 4x

]
# resource tile assets
RESOURCE_TYPES = [
    "desert",                                               # 1x
    "fields", "fields", "fields",                           # 3x
    "forest", "forest", "forest", "forest",                 # 4x
    "hills", "hills", "hills",                              # 3x
    "mountains", "mountains", "mountains", "mountains",     # 4x
    "pasture", "pasture", "pasture", "pasture"              # 4x
]
