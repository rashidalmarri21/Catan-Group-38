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

# menu assets
MENU_BG = pygame.image.load('assets/menu/Catan_BG.jpg')
MENU_BUTTON = pygame.image.load('assets/menu/Play Rect.png')


# resource tile assets
DESERT = pygame.image.load('assets/tile/desert.png')
FIELDS = pygame.image.load('assets/tile/fields.png')
FOREST = pygame.image.load('assets/tile/forest.png')
HILLS = pygame.image.load('assets/tile/hills.png')
MOUNTAINS = pygame.image.load('assets/tile/mountains.png')
PASTURE = pygame.image.load('assets/tile/pasture.png')

RESOURCE_TYPES = [DESERT, FIELDS, FIELDS, FIELDS, FOREST, FOREST, FOREST, FOREST, HILLS, HILLS, HILLS, MOUNTAINS,
                  MOUNTAINS, MOUNTAINS, MOUNTAINS, PASTURE, PASTURE, PASTURE, PASTURE]