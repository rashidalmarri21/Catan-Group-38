import pygame

from catan import button

# screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

# colour constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
CYAN = (0, 255, 255)

# board constants
HEXAGON_RADIUS = 75
BUFFER = 5
HEX_RAD_BUFF = HEXAGON_RADIUS + BUFFER
GRID_SIZE = 5
# this is the x,y indices that we DO NOT want in our final board.
EXCLUDED_INDICES = [(0, 0), (0, 4), (4, 0), (4, 1), (4, 3), (4, 4)]

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
# resource tile list. Can adj the freq. ENTRIES MUST BE = 19 AND AT LEAST 1 DESERT TILE.
RESOURCE_TYPES = [
    "desert",  # 1x
    "fields", "fields", "fields",  # 3x
    "forest", "forest", "forest", "forest",  # 4x
    "hills", "hills", "hills",  # 3x
    "mountains", "mountains", "mountains", "mountains",  # 4x
    "pasture", "pasture", "pasture", "pasture"  # 4x
]

# fonts
pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 32)
TITLE_FONT = pygame.font.SysFont("comicsansms", 42)
NUMBER_FONT = pygame.font.SysFont("comicsansms", 30)

# menu assets
MENU_BG = pygame.image.load('assets/menu/Catan_BG.jpg')
MENU_BUTTON = pygame.image.load('assets/menu/Play Rect.png')
# menu title
MENU_TITLE_TEXT = TITLE_FONT.render("The SETTLERS of CATAN", True, "#b68f40")
MENU_TITLE_RECT = MENU_TITLE_TEXT.get_rect(center=(960, 150))
# menu buttons
PLAY_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 500), text_input="PLAY", font=FONT, base_color=BLACK,
                            hovering_color=WHITE)
OPTIONS_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 650), text_input="OPTIONS", font=FONT, base_color=BLACK,
                               hovering_color=WHITE)
QUIT_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 800), text_input="QUIT", font=FONT, base_color=BLACK,
                            hovering_color=WHITE)


# player constants
EXCLUDED_INTERSECTIONS = []
HOUSE_POSITIONS = [
    (821.4359353944899, 220.0), (960.0, 220.0), (1098.56406460551, 220.0), (752.1539030917347, 340.0),
    (890.717967697245, 340.0), (1029.282032302755, 340.0), (1167.8460969082653, 340.0), (682.8718707889797, 460.0),
    (821.4359353944899, 460.0), (960.0, 460.0), (1098.56406460551, 460.0), (1237.1281292110202, 460.0),
    (752.1539030917347, 580.0), (890.717967697245, 580.0), (1029.282032302755, 580.0), (1167.8460969082653, 580.0),
    (821.4359353944899, 700.0), (960.0, 700.0), (1098.56406460551, 700.0), (682.8718707889797, 380.0),
    (821.4359353944899, 380.0), (960.0, 380.0), (1098.56406460551, 380.0), (1237.1281292110202, 380.0),
    (752.1539030917347, 500.0), (890.717967697245, 500.0), (1029.282032302755, 500.0), (1167.8460969082653, 500.0),
    (1306.4101615137754, 500.0), (682.8718707889797, 620.0), (821.4359353944899, 620.0), (960.0, 620.0),
    (1098.56406460551, 620.0), (1237.1281292110202, 620.0), (752.1539030917347, 740.0), (890.717967697245, 740.0),
    (1029.282032302755, 740.0), (1167.8460969082653, 740.0), (821.4359353944899, 860.0), (960.0, 860.0),
    (1098.56406460551, 860.0), (612.8718707889797, 580.0), (682.1539030917347, 700.0), (751.4359353944899, 820.0),
    (890.0, 820.0), (1028.56406460551, 820.0), (1167.1281292110202, 820.0), (612.8718707889797, 500.0),
    (751.4359353944899, 260.0), (890.0, 260.0), (1028.56406460551, 260.0), (1167.1281292110202, 260.0),
    (1307.1281292110202, 580.0), (1237.8460969082653, 700.0)

                   ]



"""
(0, 0 : (752.8718707889797, 340.0),
(1, 0 : (891.4359353944899, 340.0),
(2, 0 : (1030.0, 340.0),
(3, 0 : (1168.56406460551, 340.0),
(4, 0 : (1307.1281292110202, 340.0),
(0, 1 : (822.1539030917347, 460.0),
(1, 1 : (960.717967697245, 460.0),
(2, 1 : (1099.282032302755, 460.0),
(3, 1 : (1237.8460969082653, 460.0),
(4, 1 : (1376.4101615137754, 460.0),
(0, 2 : (752.8718707889797, 580.0),
(1, 2 : (891.4359353944899, 580.0),
(2, 2 : (1030.0, 580.0),
(3, 2 : (1168.56406460551, 580.0),
(4, 2 : 
(0, 3 : (822.1539030917347, 700.0),
(1, 3 : (960.717967697245, 700.0),
(2, 3 : (1099.282032302755, 700.0),
(3, 3 : 
(4, 3 : (1376.4101615137754, 700.0),
(0, 4 : (752.8718707889797, 820.0),
(1, 4 : (891.4359353944899, 820.0),
(2, 4 : (1030.0, 820.0),
(3, 4 : (1168.56406460551, 820.0),
(4, 4 : (1307.1281292110202, 820.0),
(0, 0 : (752.8718707889797, 340.0),







"""