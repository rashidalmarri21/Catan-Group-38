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
BLUE = (102, 51, 255)
ORANGE = (255, 153, 1)
RED = (255, 0, 26)
PURPLE = (188, 23, 229)
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
    "victory", "victory", "victory",  # 3x victory point cards
    "road", "road",  # 2x road building
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
PLAY_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 500), text_input="PLAY", font=FONT, base_color=WHITE,
                            hovering_color=(160, 32, 220))
LOAD_GAME_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 650), text_input="LOAD GAME", font=FONT, base_color=WHITE,
                               hovering_color=(160, 32, 220))
QUIT_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 800), text_input="QUIT", font=FONT, base_color=WHITE,
                            hovering_color=(160, 32, 220))
MENU_BUTTON_LIST = [PLAY_BUTTON, LOAD_GAME_BUTTON, QUIT_BUTTON]

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
ROBBER = pygame.image.load("assets/UI/robber/robber.png")


# pause menu
PAUSE_IMAGE = pygame.image.load("assets/UI/pause/pause button.png")
PAUSE_MENU_UI = pygame.image.load("assets/UI/pause/pause menu.png")
PAUSE_MENU_RECT = PAUSE_MENU_UI.get_rect(center=(960, 550))
PAUSE_BUTTON = button.Button(image=PAUSE_IMAGE, pos=(65, 272), text_input="", font=NUMBER_FONT,
                                base_color=BLACK,
                                hovering_color=(160, 32, 220), border=True, border_width=5, border_color=BLACK)
SAVE_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 650), text_input="SAVE", font=NUMBER_FONT,
                                base_color=(160, 32, 220),
                                hovering_color=(160, 32, 220), border=True, border_width=5, border_color=BLACK)
RESUME_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 500), text_input="RESUME", font=NUMBER_FONT,
                                base_color=(160, 32, 220),
                                hovering_color=(160, 32, 220), border=True, border_width=5, border_color=BLACK)
# game buttons

END_TURN_BUTTON = button.Button(image=MENU_BUTTON, pos=(1656, 967), text_input="End Turn", font=NUMBER_FONT,
                                base_color=(160, 32, 220),
                                hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_HOUSE_BUTTON = button.Button(image=MENU_BUTTON, pos=(718, 967), text_input="Place House", font=NUMBER_FONT,
                                   base_color=(160, 32, 220),
                                   hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_CITY_BUTTON = button.Button(image=MENU_BUTTON, pos=(1207, 967), text_input="Place City", font=NUMBER_FONT,
                                  base_color=(160, 32, 220),
                                  hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
PLACE_ROAD_BUTTON = button.Button(image=MENU_BUTTON, pos=(269, 967), text_input="Place Road", font=NUMBER_FONT,
                                  base_color=(160, 32, 220),
                                  hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
BACK_BUTTON = button.Button(image=MENU_BUTTON, pos=(269, 967), text_input="Back", font=NUMBER_FONT,
                            base_color=(160, 32, 220),
                            hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
BACK_DEV_TRADE_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 967), text_input="Back", font=NUMBER_FONT,
                                      base_color=(160, 32, 220),
                                      hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
ROLL_DICE_BUTTON = button.Button(image=MENU_BUTTON, pos=(960, 967), text_input="Roll Dice", font=NUMBER_FONT,
                                 base_color=(160, 32, 220),
                                 hovering_color=(160, 32, 220), border=True, border_width=10, border_color=BLACK)
DEV_CARDS_BUTTON = button.Button(image=DEV_CARDS_IMAGE, pos=(95, 540), text_input="", font=NUMBER_FONT,
                                 base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=10,
                                 border_color=BLACK)
PLAYER_TRADING_BUTTON = button.Button(image=PLAYER_TRADING_IMAGE, pos=(1825, 540), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=10,
                                      border_color=BLACK)
# bank assets
SHEEP_IMAGE = pygame.image.load("assets/UI/bank buttons/sheep.png")
WHEAT_IMAGE = pygame.image.load("assets/UI/bank buttons/wheat.png")
WOOD_IMAGE = pygame.image.load("assets/UI/bank buttons/wood.png")
ORE_IMAGE = pygame.image.load("assets/UI/bank buttons/ore.png")
BRICK_IMAGE = pygame.image.load("assets/UI/bank buttons/bricks.png")
DEV_IMAGE = pygame.image.load("assets/UI/bank buttons/dev.png")
QUESTION_MARK_DICE = pygame.image.load("assets/UI/dice/dice_roll.png")
MARITIME_TRADE = pygame.image.load("assets/UI/bank buttons/maritime trade.png")
BUY_DEV_TRADE = pygame.image.load("assets/UI/bank buttons/buy dev card.png")

# bank buttons
SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(161, 169), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(272, 169), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(51, 169), text_input="", font=NUMBER_FONT,
                            base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                            border_color=(127, 127, 127))
ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(381, 169), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(491, 169), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
DEV_BUTTON = button.Button(image=DEV_IMAGE, pos=(602, 169), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))

# dev cards images
KNIGHT_DEV = pygame.image.load("assets/UI/dev cards/knight.png")
VICTORY_POINT_DEV = pygame.image.load("assets/UI/dev cards/victory.png")
ROAD_BUILDING_DEV = pygame.image.load("assets/UI/dev cards/road building.png")
MONOPOLY_DEV = pygame.image.load("assets/UI/dev cards/monopoly.png")
YEAR_OF_PLENTY_DEV = pygame.image.load("assets/UI/dev cards/year of plenty.png")
BLACK_CARD_DEV = pygame.image.load("assets/UI/dev cards/blank card.png")
USE_DEV = pygame.image.load("assets/UI/dev cards/use button.png")
GREY_USE_DEV = pygame.image.load("assets/UI/dev cards/grey use button.png")
ROBBER_EFFECT = pygame.image.load("assets/UI/dev cards buy/robber effect.png")
ROBBER_EFFECT_RECT = ROBBER_EFFECT.get_rect(center=(960, 540))

# dev cards BUY DEV CARD static rects.
KNIGHT_BUY_DEV = pygame.image.load("assets/UI/dev cards buy/knight.png")
ROAD_BUILDING_BUY_DEV = pygame.image.load("assets/UI/dev cards buy/road building.png")
MONOPOLY_BUY_DEV = pygame.image.load("assets/UI/dev cards buy/monopoly.png")
VICTORY_BUY_DEV = pygame.image.load("assets/UI/dev cards buy/victory.png")
YEAR_BUY_DEV = pygame.image.load("assets/UI/dev cards buy/year of plenty.png")
BUY_BUTTON_IMAGE = pygame.image.load("assets/UI/dev cards buy/buy button.png")
PLAYER_ROBBER_IMAGE = pygame.image.load("assets/UI/dev cards buy/blank button.png")
BACK_BUTTON_IMAGE = pygame.image.load("assets/UI/dev cards buy/back button.png")
BUY_BUTTON_BUY_DEV = button.Button(image=BUY_BUTTON_IMAGE, pos=(851, 685), text_input="", font=NUMBER_FONT,
                              base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                              border_color=(127, 127, 127))
BACK_BUTTON_BUY_DEV = button.Button(image=BACK_BUTTON_IMAGE, pos=(1069, 685), text_input="", font=NUMBER_FONT,
                              base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                              border_color=(127, 127, 127))

# dev cards buttons
KNIGHT_BUTTON = button.Button(image=KNIGHT_DEV, pos=(81, 692), text_input="", font=NUMBER_FONT,
                              base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                              border_color=(127, 127, 127))
VICTORY_POINT_BUTTON = button.Button(image=VICTORY_POINT_DEV, pos=(267, 692), text_input="", font=NUMBER_FONT,
                                     base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                     border_color=(127, 127, 127))
ROAD_BUILDING_BUTTON = button.Button(image=ROAD_BUILDING_DEV, pos=(451, 692), text_input="", font=NUMBER_FONT,
                                     base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                     border_color=(127, 127, 127))
MONOPOLY_BUTTON = button.Button(image=MONOPOLY_DEV, pos=(81, 842), text_input="", font=NUMBER_FONT,
                                base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                border_color=(127, 127, 127))
YEAR_OF_PLENTY_BUTTON = button.Button(image=YEAR_OF_PLENTY_DEV, pos=(267, 842), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                      border_color=(127, 127, 127))
BLANK_CARD_BUTTON = button.Button(image=BLACK_CARD_DEV, pos=(451, 842), text_input="", font=NUMBER_FONT,
                                  base_color=BLACK, hovering_color=(127, 127, 127), border=True, border_width=5,
                                  border_color=(127, 127, 127))
USE_BUTTON = button.Button(image=USE_DEV, pos=(503, 1007), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
GREY_USE_RECT = GREY_USE_DEV.get_rect(center=(503, 1007))

# monopoly effect buttons and image
MONOPOLY_EFFECT_IMAGE = pygame.image.load("assets/UI/dev cards/monopoly effect.png")
MONOPOLY_EFFECT_RECT = MONOPOLY_EFFECT_IMAGE.get_rect(center=(960, 540))
YEAR_EFFECT_IMAGE = pygame.image.load("assets/UI/dev cards/year effect.png")
YEAR_EFFECT_RECT = YEAR_EFFECT_IMAGE.get_rect(center=(960, 540))

SHEEP_BUTTON_MONOPOLY = button.Button(image=SHEEP_IMAGE, pos=(851, 570), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                      border_color=(127, 127, 127))
WHEAT_BUTTON_MONOPOLY = button.Button(image=WHEAT_IMAGE, pos=(960, 570), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                      border_color=(127, 127, 127))
WOOD_BUTTON_MONOPOLY = button.Button(image=WOOD_IMAGE, pos=(742, 570), text_input="", font=NUMBER_FONT,
                                     base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                     border_color=(127, 127, 127))
ORE_BUTTON_MONOPOLY = button.Button(image=ORE_IMAGE, pos=(1069, 570), text_input="", font=NUMBER_FONT,
                                    base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                    border_color=(127, 127, 127))
BRICK_BUTTON_MONOPOLY = button.Button(image=BRICK_IMAGE, pos=(1178, 570), text_input="", font=NUMBER_FONT,
                                      base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                                      border_color=(127, 127, 127))
MONOPOLY_EFFECT_BUTTON_LIST = [SHEEP_BUTTON_MONOPOLY, WHEAT_BUTTON_MONOPOLY, WOOD_BUTTON_MONOPOLY, ORE_BUTTON_MONOPOLY,
                               BRICK_BUTTON_MONOPOLY]

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

# player trading images
NAME_PLATE = pygame.image.load("assets/UI/player trading/name plate.png")
PLAYER_TRADING_UI = pygame.image.load("assets/UI/player trading/player trading UI.png")
PLAYER_TRADE_UI = pygame.image.load("assets/UI/player trading/player trade UI.png")
PLAYER_TRADE_UI_RECT = PLAYER_TRADE_UI.get_rect(center=(960, 650))



BACK_TRADE_IMAGE = pygame.image.load("assets/UI/player trading/trade_back_button.png")
BACK_BUTTON_TRADE = button.Button(image=BACK_TRADE_IMAGE, pos=(962, 947), text_input="Back", font=NUMBER_FONT,
                             base_color=(127, 127, 127), hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=BLACK)
TRADE_BUTTON = button.Button(image=BACK_TRADE_IMAGE, pos=(962, 630), text_input="Trade", font=NUMBER_FONT,
                             base_color=(127, 127, 127), hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=BLACK)

LEFT_PLAYER_SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(574, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
LEFT_PLAYER_WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(676, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
LEFT_PLAYER_WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(472, 770), text_input="", font=NUMBER_FONT,
                            base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                            border_color=(127, 127, 127))
LEFT_PLAYER_ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(778, 770), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
LEFT_PLAYER_BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(880, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))

RIGHT_PLAYER_SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(1157, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
RIGHT_PLAYER_WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(1259, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
RIGHT_PLAYER_WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(1055, 770), text_input="", font=NUMBER_FONT,
                            base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                            border_color=(127, 127, 127))
RIGHT_PLAYER_ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(1361, 770), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
RIGHT_PLAYER_BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(1463, 770), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))

LEFT_TRADE_SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(574, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
LEFT_TRADE_WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(676, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
LEFT_TRADE_WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(472, 417), text_input="", font=NUMBER_FONT,
                            base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                            border_color=(127, 127, 127))
LEFT_TRADE_ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(778, 417), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
LEFT_TRADE_BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(880, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))

RIGHT_TRADE_SHEEP_BUTTON = button.Button(image=SHEEP_IMAGE, pos=(1157, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
RIGHT_TRADE_WHEAT_BUTTON = button.Button(image=WHEAT_IMAGE, pos=(1259, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))
RIGHT_TRADE_WOOD_BUTTON = button.Button(image=WOOD_IMAGE, pos=(1055, 417), text_input="", font=NUMBER_FONT,
                            base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                            border_color=(127, 127, 127))
RIGHT_TRADE_ORE_BUTTON = button.Button(image=ORE_IMAGE, pos=(1361, 417), text_input="", font=NUMBER_FONT,
                           base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                           border_color=(127, 127, 127))
RIGHT_TRADE_BRICK_BUTTON = button.Button(image=BRICK_IMAGE, pos=(1463, 417), text_input="", font=NUMBER_FONT,
                             base_color=BLACK, hovering_color=(160, 32, 220), border=True, border_width=5,
                             border_color=(127, 127, 127))

# button lists
TRADE_BUTTONS = [LEFT_PLAYER_SHEEP_BUTTON, LEFT_PLAYER_WHEAT_BUTTON, LEFT_PLAYER_WOOD_BUTTON, LEFT_PLAYER_ORE_BUTTON, LEFT_PLAYER_BRICK_BUTTON,
                 RIGHT_PLAYER_SHEEP_BUTTON, RIGHT_PLAYER_WHEAT_BUTTON, RIGHT_PLAYER_WOOD_BUTTON, RIGHT_PLAYER_ORE_BUTTON, RIGHT_PLAYER_BRICK_BUTTON,
                 LEFT_TRADE_SHEEP_BUTTON, LEFT_TRADE_WHEAT_BUTTON, LEFT_TRADE_WOOD_BUTTON, LEFT_TRADE_ORE_BUTTON, LEFT_TRADE_BRICK_BUTTON,
                 RIGHT_TRADE_SHEEP_BUTTON, RIGHT_TRADE_WHEAT_BUTTON, RIGHT_TRADE_WOOD_BUTTON, RIGHT_TRADE_ORE_BUTTON, RIGHT_TRADE_BRICK_BUTTON,
                 TRADE_BUTTON, BACK_BUTTON_TRADE]
UI_BUTTONS = [END_TURN_BUTTON, PLACE_HOUSE_BUTTON, PLACE_ROAD_BUTTON, SHEEP_BUTTON, WHEAT_BUTTON, WOOD_BUTTON,
              ORE_BUTTON, BRICK_BUTTON,
              DEV_BUTTON, DEV_CARDS_BUTTON, PLAYER_TRADING_BUTTON, PLACE_CITY_BUTTON, PAUSE_BUTTON]
PLACE_HOUSE_BUTTONS = [END_TURN_BUTTON, BACK_BUTTON]
PLACE_ROAD_BUTTONS = [BACK_BUTTON, END_TURN_BUTTON]
DEV_CARDS_BUTTONS_LIST = [KNIGHT_BUTTON, VICTORY_POINT_BUTTON, ROAD_BUILDING_BUTTON, MONOPOLY_BUTTON,
                          YEAR_OF_PLENTY_BUTTON, BLANK_CARD_BUTTON, BACK_DEV_TRADE_BUTTON]

# ui elements
BACKGROUND_UI_IMAGE = pygame.image.load("assets/UI/UI_Background_ship.png")

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

WOOD_FLAG = pygame.image.load("assets/UI/flags/wood flag.png")
WHEAT_FLAG = pygame.image.load("assets/UI/flags/wheat flag.png")
SHEEP_FLAG = pygame.image.load("assets/UI/flags/sheep flag.png")
ORE_FLAG = pygame.image.load("assets/UI/flags/ore flag.png")
BRICK_FLAG = pygame.image.load("assets/UI/flags/brick flag.png")
ANY_FLAG = pygame.image.load("assets/UI/flags/any flag.png")
FLAG_LIST = [WOOD_FLAG, WHEAT_FLAG, ORE_FLAG, BRICK_FLAG, SHEEP_FLAG, ANY_FLAG, ANY_FLAG, ANY_FLAG, ANY_FLAG]

FLAG_POSITIONS = [
    (707, 174),
    (1036, 140),
    (1246, 265),
    (1397, 490),
    (1282, 724),
    (1054, 870),
    (711, 822),
    (571, 584),
    (561, 349)
]

FLAG_HOUSE_CHECK = {
    1: [(751.4359353944899, 260.0), (821.4359353944899, 220.0)],
    2: [(960.0, 220.0), (1028.56406460551, 260.0)],
    3: [(1167.8460969082653, 340.0), (1237.1281292110202, 380.0)],
    4: [(1306.4101615137754, 500.0), (1307.1281292110202, 580.0)],
    5: [(1237.8460969082653, 700.0), (1167.8460969082653, 740.0)],
    6: [(1028.56406460551, 820.0), (960.0, 860.0)],
    7: [(821.4359353944899, 860.0), (751.4359353944899, 820.0)],
    8: [(682.1539030917347, 700.0), (682.8718707889797, 620.0)],
    9: [(682.8718707889797, 460.0), (682.8718707889797, 380.0)]
}

EVERY_HOUSE_IN_PLAY = []
