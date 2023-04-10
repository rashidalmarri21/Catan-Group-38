import pygame

from catan import button

# screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080
# icon
ICON_32x = pygame.image.load("assets/Icon/honeycomb32.png")

MOUSE_BUFFER = 20
VIC_POINT_THRESHOLD = 10

# colour constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BEIGE = (245, 245, 220)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)
MAROON = (128, 255, 0)
BLUE = "#6633FF"
ORANGE = "#FF9901"
RED = "#FF001A"
PURPLE = "#BC17E5"
COLOR_LIST = [RED, ORANGE, PURPLE, BLUE]

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

DEV_CARDS = [
    "knight", "knight", "knight", "knight", "knight", "knight", "knight",  # 14x knight cards
    "knight", "knight", "knight", "knight", "knight", "knight", "knight",
    "victory", "victory", "victory", "victory", "victory",  # 5x victory point cards
    "monopoly", "monopoly",  # 2x monopoly cards
    "build", "build",  # 2x Road building cards
    "year", "year"  # 2x Year of plenty cards
]

# fonts
pygame.font.init()
FONT = pygame.font.SysFont("comicsansms", 32)
TITLE_FONT = pygame.font.SysFont("comicsansms", 42)
NUMBER_FONT = pygame.font.SysFont("comicsansms", 29)
BANK_NUMBER_FONT = pygame.font.SysFont("comicsansms", 15)
PLAYER_NAME_FONT = pygame.font.SysFont("comicsansms", 23)

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
MENU_BUTTON_LIST = [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]

# game images
DEV_CARDS_IMAGE = pygame.image.load("assets/UI/dev cards.png")
PLAYER_TRADING_IMAGE = pygame.image.load("assets/UI/player trading.png")
DEV_CARDS_UI_IMAGE = pygame.image.load("assets/UI/dev cards UI.png")
DEV_CARDS_UI_RECT = DEV_CARDS_UI_IMAGE.get_rect(topleft=(0, 486))
DEV_CARDS_KNIGHT_UI_IMAGE = pygame.image.load("assets/UI/dev cards/knight UI static.png")
DEV_CARDS_KNIGHT_UI_RECT = DEV_CARDS_KNIGHT_UI_IMAGE.get_rect(topleft=(0, 486))
DEV_CARDS_VICTORY_UI_IMAGE = pygame.image.load("assets/UI/dev cards/victory UI static.png")
DEV_CARDS_VICTORY_UI_RECT = DEV_CARDS_VICTORY_UI_IMAGE.get_rect(topleft=(0, 486))
DEV_CARDS_ROAD_BUILDING_UI_IMAGE = pygame.image.load("assets/UI/dev cards/road building UI static.png")
DEV_CARDS_ROAD_BUILDING_UI_RECT = DEV_CARDS_ROAD_BUILDING_UI_IMAGE.get_rect(topleft=(0, 486))
DEV_CARDS_MONOPOLY_UI_IMAGE = pygame.image.load("assets/UI/dev cards/monopoly UI static.png")
DEV_CARDS_MONOPOLY_UI_RECT = DEV_CARDS_MONOPOLY_UI_IMAGE.get_rect(topleft=(0, 486))
DEV_CARDS_YEAR_UI_IMAGE = pygame.image.load("assets/UI/dev cards/year UI static.png")
DEV_CARDS_YEAR_UI_RECT = DEV_CARDS_YEAR_UI_IMAGE.get_rect(topleft=(0, 486))


# game buttons
END_TURN_BUTTON = button.Button(image=MENU_BUTTON, pos=(1656, 967), text_input="End Turn", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_HOUSE_BUTTON = button.Button(image=MENU_BUTTON, pos=(718, 967), text_input="Place House", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_CITY_BUTTON = button.Button(image=MENU_BUTTON, pos=(1207, 967), text_input="Place City", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_ROAD_BUTTON = button.Button(image=MENU_BUTTON, pos=(269, 967), text_input="Place Road", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
BACK_BUTTON = button.Button(image=MENU_BUTTON, pos=(269, 967), text_input="Back", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
BACK_DEV_TRADE_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 967), text_input="Back", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
ROLL_DICE_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 967), text_input="Roll Dice", font=NUMBER_FONT, base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
DEV_CARDS_BUTTON = button.Button(image=DEV_CARDS_IMAGE, pos=(95, 540), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=10, border_color=BLACK)
PLAYER_TRADING_BUTTON = button.Button(image=PLAYER_TRADING_IMAGE, pos=(1825, 540), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
# bank assets
SHEEP_IMAGE = pygame.image.load("assets/UI/bank buttons/sheep.png")
WHEAT_IMAGE = pygame.image.load("assets/UI/bank buttons/wheat.png")
WOOD_IMAGE = pygame.image.load("assets/UI/bank buttons/wood.png")
ORE_IMAGE = pygame.image.load("assets/UI/bank buttons/ore.png")
BRICK_IMAGE = pygame.image.load("assets/UI/bank buttons/bricks.png")
DEV_IMAGE = pygame.image.load("assets/UI/bank buttons/dev.png")
QUESTION_MARK_DICE = pygame.image.load("assets/UI/dice/dice_roll.png")

# bank buttons
SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(161, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(272, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(51, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(381, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(491, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
DEV_BUTTON = button.Button(image=DEV_IMAGE, pos=(602, 169), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))

# dev cards images
KNIGHT_DEV = pygame.image.load("assets/UI/dev cards/knight.png")
VICTORY_POINT_DEV = pygame.image.load("assets/UI/dev cards/victory.png")
ROAD_BUILDING_DEV = pygame.image.load("assets/UI/dev cards/road building.png")
MONOPOLY_DEV = pygame.image.load("assets/UI/dev cards/monopoly.png")
YEAR_OF_PLENTY_DEV = pygame.image.load("assets/UI/dev cards/year of plenty.png")
BLACK_CARD_DEV = pygame.image.load("assets/UI/dev cards/blank card.png")
USE_DEV = pygame.image.load("assets/UI/dev cards/use button.png")
GREY_USE_DEV = pygame.image.load("assets/UI/dev cards/grey use button.png")

# dev cards buttons
KNIGHT_BUTTON = button.Button(image=KNIGHT_DEV, pos=(81, 692), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
VICTORY_POINT_BUTTON = button.Button(image=VICTORY_POINT_DEV, pos=(267, 692), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
ROAD_BUILDING_BUTTON = button.Button(image=ROAD_BUILDING_DEV, pos=(451, 692), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
MONOPOLY_BUTTON = button.Button(image=MONOPOLY_DEV, pos=(81, 842), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
YEAR_OF_PLENTY_BUTTON = button.Button(image=YEAR_OF_PLENTY_DEV, pos=(267, 842), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
BLANK_CARD_BUTTON = button.Button(image=BLACK_CARD_DEV, pos=(451, 842), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(127, 127, 127), border=True,border_width=5, border_color=(127, 127, 127))
USE_BUTTON = button.Button(image=USE_DEV, pos=(503, 1007), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True,border_width=5, border_color=(127, 127, 127))
GREY_USE_RECT = GREY_USE_DEV.get_rect(center=(503, 1007))

# dev card info images
KNIGHT_INFO_DEV = pygame.image.load("assets/UI/dev cards/knight info.png")
VICTORY_INFO_DEV = pygame.image.load("assets/UI/dev cards/victory info.png")
ROAD_BUILDING_INFO_DEV = pygame.image.load("assets/UI/dev cards/road building info.png")
MONOPOLY_INFO_DEV = pygame.image.load("assets/UI/dev cards/monopoly info.png")
YEAR_INFO_DEV = pygame.image.load("assets/UI/dev cards/year of plenty info.png")
BLANK_INFO_DEV = pygame.image.load("assets/UI/dev cards/blank info.png")

# dev card info rects
KNIGHT_INFO_DEV_RECT = KNIGHT_INFO_DEV.get_rect(center=(217, 1012))
VICTORY_INFO_RECT = VICTORY_INFO_DEV.get_rect(center=(217, 1012))
ROAD_BUILDING_INFO_DEV_RECT = ROAD_BUILDING_INFO_DEV.get_rect(center=(217, 1012))
MONOPOLY_INFO_DEV_RECT = MONOPOLY_INFO_DEV.get_rect(center=(217, 1012))
YEAR_INFO_DEV_RECT = YEAR_INFO_DEV.get_rect(center=(217, 1012))
BLANK_INFO_DEV_RECT = BLANK_INFO_DEV.get_rect(center=(217, 1012))

# button lists
UI_BUTTONS = [END_TURN_BUTTON, PLACE_HOUSE_BUTTON, PLACE_ROAD_BUTTON, SHEEP_BUTTON, WHEAT_BUTTON, WOOD_BUTTON, ORE_BUTTON, BRICK_BUTTON,
              DEV_BUTTON, DEV_CARDS_BUTTON, PLAYER_TRADING_BUTTON, PLACE_CITY_BUTTON]
PLACE_HOUSE_BUTTONS = [END_TURN_BUTTON, BACK_BUTTON]
PLACE_ROAD_BUTTONS = [BACK_BUTTON, END_TURN_BUTTON]
DEV_CARDS_BUTTONS_LIST = [KNIGHT_BUTTON, VICTORY_POINT_BUTTON, ROAD_BUILDING_BUTTON, MONOPOLY_BUTTON, YEAR_OF_PLENTY_BUTTON, BLANK_CARD_BUTTON, BACK_DEV_TRADE_BUTTON]

# ui elements
BACKGROUND_UI_IMAGE = pygame.image.load("assets/UI/UI_Background.png")

# houses
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

ROAD_POSITIONS = [
    ((821.4359353944899, 220.0), (751.4359353944899, 260.0)),
    ((751.4359353944899, 260.0), (752.1539030917347, 340.0)),
    ((752.1539030917347, 340.0), (821.4359353944899, 380.0)),
    ((821.4359353944899, 380.0), (890.717967697245, 340.0)),
    ((890.717967697245, 340.0), (890.0, 260.0)),
    ((890.0, 260.0), (821.4359353944899, 220.0)),
    ((890.0, 260.0), (960.0, 220.0)),
    ((960.0, 220.0), (1028.56406460551, 260.0)),
    ((1028.56406460551, 260.0), (1029.282032302755, 340.0)),
    ((1029.282032302755, 340.0), (960.0, 380.0)),
    ((960.0, 380.0), (890.717967697245, 340.0)),
    ((1028.56406460551, 260.0), (1098.56406460551, 220.0)),
    ((1098.56406460551, 220.0), (1167.1281292110202, 260.0)),
    ((1167.1281292110202, 260.0), (1167.8460969082653, 340.0)),
    ((1167.8460969082653, 340.0), (1098.56406460551, 380.0)),
    ((1098.56406460551, 380.0), (1029.282032302755, 340.0)),
    ((1167.8460969082653, 340.0), (1237.1281292110202, 380.0)),
    ((1237.1281292110202, 380.0), (1237.1281292110202, 460.0)),
    ((1237.1281292110202, 460.0), (1167.8460969082653, 500.0)),
    ((1167.8460969082653, 500.0), (1098.56406460551, 460.0)),
    ((1098.56406460551, 460.0), (1098.56406460551, 380.0)),
    ((1098.56406460551, 460.0), (1029.282032302755, 500.0)),
    ((1029.282032302755, 500.0), (960.0, 460.0)),
    ((960.0, 460.0), (960.0, 380.0)),
    ((960.0, 460.0), (890.717967697245, 500.0)),
    ((890.717967697245, 500.0), (821.4359353944899, 460.0)),
    ((821.4359353944899, 460.0), (821.4359353944899, 380.0)),
    ((821.4359353944899, 460.0), (752.1539030917347, 500.0)),
    ((752.1539030917347, 500.0), (682.8718707889797, 460.0)),
    ((682.8718707889797, 460.0), (682.8718707889797, 380.0)),
    ((682.8718707889797, 380.0), (752.1539030917347, 340.0)),
    ((682.8718707889797, 460.0), (612.8718707889797, 500.0)),
    ((612.8718707889797, 500.0), (612.8718707889797, 580.0)),
    ((612.8718707889797, 580.0), (682.8718707889797, 620.0)),
    ((682.8718707889797, 620.0), (752.1539030917347, 580.0)),
    ((752.1539030917347, 580.0), (752.1539030917347, 500.0)),
    ((752.1539030917347, 580.0), (821.4359353944899, 620.0)),
    ((821.4359353944899, 620.0), (890.717967697245, 580.0)),
    ((890.717967697245, 580.0), (890.717967697245, 500.0)),
    ((890.717967697245, 580.0), (960.0, 620.0)),
    ((960.0, 620.0), (1029.282032302755, 580.0)),
    ((1029.282032302755, 580.0), (1029.282032302755, 500.0)),
    ((1029.282032302755, 580.0), (1098.56406460551, 620.0)),
    ((1098.56406460551, 620.0), (1167.8460969082653, 580.0)),
    ((1167.8460969082653, 580.0), (1167.8460969082653, 500.0)),
    ((1167.8460969082653, 580.0), (1237.1281292110202, 620.0)),
    ((1237.1281292110202, 620.0), (1307.1281292110202, 580.0)),
    ((1306.4101615137754, 500.0), (1237.1281292110202, 460.0)),
    ((1237.1281292110202, 620.0), (1237.8460969082653, 700.0)),
    ((1237.8460969082653, 700.0), (1167.8460969082653, 740.0)),
    ((1167.8460969082653, 740.0), (1098.56406460551, 700.0)),
    ((1098.56406460551, 700.0), (1098.56406460551, 620.0)),
    ((1098.56406460551, 700.0), (1029.282032302755, 740.0)),
    ((1029.282032302755, 740.0), (960.0, 700.0)),
    ((960.0, 700.0), (960.0, 620.0)),
    ((960.0, 700.0), (890.717967697245, 740.0)),
    ((890.717967697245, 740.0), (821.4359353944899, 700.0)),
    ((821.4359353944899, 700.0), (821.4359353944899, 620.0)),
    ((821.4359353944899, 700.0), (752.1539030917347, 740.0)),
    ((752.1539030917347, 740.0), (682.1539030917347, 700.0)),
    ((682.1539030917347, 700.0), (682.8718707889797, 620.0)),
    ((752.1539030917347, 740.0), (751.4359353944899, 820.0)),
    ((751.4359353944899, 820.0), (821.4359353944899, 860.0)),
    ((821.4359353944899, 860.0), (890.0, 820.0)),
    ((890.0, 820.0), (890.717967697245, 740.0)),
    ((890.0, 820.0), (960.0, 860.0)),
    ((960.0, 860.0), (1028.56406460551, 820.0)),
    ((1028.56406460551, 820.0), (1029.282032302755, 740.0)),
    ((1028.56406460551, 820.0), (1098.56406460551, 860.0)),
    ((1098.56406460551, 860.0), (1167.1281292110202, 820.0)),
    ((1167.1281292110202, 820.0), (1167.8460969082653, 740.0)),
    ((1306.4101615137754, 500.0), (1307.1281292110202, 580.0))

]

HOUSE_TILE_CHECK = {
    (1, 0):
        [(752.1539030917347, 340.0),
         (821.4359353944899, 380.0),
         (890.717967697245, 340.0),
         (890.0, 260.0),
         (821.4359353944899, 220.0),
         (751.4359353944899, 260.0)],

    (2, 0):
        [(890.717967697245, 340.0),
         (960.0, 380.0),
         (1029.282032302755, 340.0),
         (1028.56406460551, 260.0),
         (960.0, 220.0),
         (890.0, 260.0)],

    (3, 0):
        [(1029.282032302755, 340.0),
         (1098.56406460551, 380.0),
         (1167.8460969082653, 340.0),
         (1167.1281292110202, 260.0),
         (1098.56406460551, 220.0),
         (1028.56406460551, 260.0)],

    (0, 1):
        [(752.1539030917347, 500.0),
         (821.4359353944899, 460.0),
         (821.4359353944899, 380.0),
         (752.1539030917347, 340.0),
         (682.8718707889797, 380.0),
         (682.8718707889797, 460.0)],

    (1, 1):
        [(821.4359353944899, 460.0),
         (890.717967697245, 500.0),
         (960.0, 460.0),
         (960.0, 380.0),
         (890.717967697245, 340.0),
         (821.4359353944899, 380.0)],

    (2, 1):
        [(960.0, 460.0),
         (1029.282032302755, 500.0),
         (1098.56406460551, 460.0),
         (1098.56406460551, 380.0),
         (1029.282032302755, 340.0),
         (960.0, 380.0)],

    (3, 1):
        [(1098.56406460551, 460.0),
         (1098.56406460551, 380.0),
         (1167.8460969082653, 340.0),
         (1237.1281292110202, 380.0),
         (1237.1281292110202, 460.0),
         (1167.8460969082653, 500.0)],

    (0, 2):
        [(682.8718707889797, 460.0),
         (612.8718707889797, 500.0),
         (612.8718707889797, 580.0),
         (682.8718707889797, 620.0),
         (752.1539030917347, 580.0),
         (752.1539030917347, 500.0)],

    (1, 2):
        [(752.1539030917347, 580.0),
         (821.4359353944899, 620.0),
         (890.717967697245, 580.0),
         (890.717967697245, 500.0),
         (821.4359353944899, 460.0),
         (752.1539030917347, 500.0)],

    (2, 2):
        [(890.717967697245, 500.0),
         (960.0, 460.0),
         (1029.282032302755, 500.0),
         (1029.282032302755, 580.0),
         (960.0, 620.0),
         (890.717967697245, 580.0)],

    (3, 2):
        [(1029.282032302755, 500.0),
         (1098.56406460551, 460.0),
         (1167.8460969082653, 500.0),
         (1167.8460969082653, 580.0),
         (1098.56406460551, 620.0),
         (1029.282032302755, 580.0)],

    (4, 2):
        [(1167.8460969082653, 580.0),
         (1167.8460969082653, 500.0),
         (1237.1281292110202, 460.0),
         (1306.4101615137754, 500.0),
         (1307.1281292110202, 580.0),
         (1237.1281292110202, 620.0)],

    (0, 3):
        [(752.1539030917347, 580.0),
         (682.8718707889797, 620.0),
         (682.1539030917347, 700.0),
         (752.1539030917347, 740.0),
         (821.4359353944899, 700.0),
         (821.4359353944899, 620.0)],

    (1, 3):
        [(821.4359353944899, 700.0),
         (890.717967697245, 740.0),
         (960.0, 700.0),
         (960.0, 620.0),
         (890.717967697245, 580.0),
         (821.4359353944899, 620.0)],

    (2, 3):
        [(960.0, 700.0),
         (1029.282032302755, 740.0),
         (1098.56406460551, 700.0),
         (1098.56406460551, 620.0),
         (1029.282032302755, 580.0),
         (960.0, 620.0)],

    (3, 3):
        [(1098.56406460551, 700.0),
         (1167.8460969082653, 740.0),
         (1237.8460969082653, 700.0),
         (1237.1281292110202, 620.0),
         (1167.8460969082653, 580.0),
         (1098.56406460551, 620.0)],

    (1, 4):
        [(752.1539030917347, 740.0),
         (751.4359353944899, 820.0),
         (821.4359353944899, 860.0),
         (890.0, 820.0),
         (890.717967697245, 740.0),
         (821.4359353944899, 700.0)],

    (2, 4):
        [(890.717967697245, 740.0),
         (890.0, 820.0),
         (960.0, 860.0),
         (1028.56406460551, 820.0),
         (1029.282032302755, 740.0),
         (960.0, 700.0)],

    (3, 4):
        [(1029.282032302755, 740.0),
         (1028.56406460551, 820.0),
         (1098.56406460551, 860.0),
         (1167.1281292110202, 820.0),
         (1167.8460969082653, 740.0),
         (1098.56406460551, 700.0)]


}
