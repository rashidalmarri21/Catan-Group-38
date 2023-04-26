import random, json, os
import sys
import pygame, operator
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, UI_BUTTONS, PLACE_HOUSE_BUTTON, PLACE_HOUSE_BUTTONS, BACK_BUTTON, \
    PLACE_ROAD_BUTTONS, PLACE_ROAD_BUTTON, ICON_32x, ROLL_DICE_BUTTON, DEV_CARDS_BUTTON, \
    BACK_DEV_TRADE_BUTTON, \
    DEV_CARDS_BUTTONS_LIST, KNIGHT_BUTTON, ROAD_BUILDING_BUTTON, MONOPOLY_BUTTON, YEAR_OF_PLENTY_BUTTON, \
    VICTORY_POINT_BUTTON, \
    USE_BUTTON, GREY_USE_RECT, GREY_USE_DEV, MONOPOLY_EFFECT_BUTTON_LIST, SHEEP_BUTTON_MONOPOLY, WHEAT_BUTTON_MONOPOLY, \
    WOOD_BUTTON_MONOPOLY, ORE_BUTTON_MONOPOLY, BRICK_BUTTON_MONOPOLY, PLACE_CITY_BUTTON, SHEEP_BUTTON, WHEAT_BUTTON, \
    WOOD_BUTTON, ORE_BUTTON, BRICK_BUTTON, DEV_BUTTON, BUY_BUTTON_BUY_DEV, BACK_BUTTON_BUY_DEV, \
    PLAYER_TRADING_BUTTON, TRADE_BUTTONS, TRADE_BUTTON, BACK_BUTTON_TRADE, LEFT_PLAYER_SHEEP_BUTTON, \
    LEFT_PLAYER_WHEAT_BUTTON, \
    LEFT_PLAYER_WOOD_BUTTON, LEFT_PLAYER_ORE_BUTTON, LEFT_PLAYER_BRICK_BUTTON, RIGHT_PLAYER_SHEEP_BUTTON, \
    RIGHT_PLAYER_WHEAT_BUTTON, \
    RIGHT_PLAYER_WOOD_BUTTON, RIGHT_PLAYER_ORE_BUTTON, RIGHT_PLAYER_BRICK_BUTTON, LEFT_TRADE_SHEEP_BUTTON, \
    LEFT_TRADE_WHEAT_BUTTON, \
    LEFT_TRADE_WOOD_BUTTON, LEFT_TRADE_ORE_BUTTON, LEFT_TRADE_BRICK_BUTTON, RIGHT_TRADE_SHEEP_BUTTON, \
    RIGHT_TRADE_WHEAT_BUTTON, \
    RIGHT_TRADE_WOOD_BUTTON, RIGHT_TRADE_ORE_BUTTON, RIGHT_TRADE_BRICK_BUTTON, PAUSE_BUTTON, RESUME_BUTTON, SAVE_BUTTON, \
    ARROW_BUTTON_LIST, GAME_OPTIONS_BUTTON, START_GAME_BUTTON, BACK_PLAY_BUTTON, PLAY_OPTIONS_BUTTONS, GAME_MODES, \
    NUM_OF_PLAYERS, AI_OPTION, PALETTE_BUTTON, GAME_MODE_TEXT, GAME_MODE_TEXT_RECT, NUM_PLAYERS_TEXT, \
    NUM_PLAYERS_TEXT_RECT, \
    AI_TEXT, AI_TEXT_RECT, COLOR_LIST, EDIT_PLAYERS_UI, EDIT_PLAYERS_UI_RECT, EDIT_NAME_PLATE, NUMBER_FONT, \
    MAIN_MENU_BUTTON, EDIT_NAME_PLATE_HOVER, EDIT_ARROWS_LIST, COLOR_IMAGE_LIST, BEIGE, VICTORY_IMAGE, VICTORY_IMAGE_RECT,\
    MAIN_MENU_VICTORY_BUTTON, QUIT_VICTORY_BUTTON, VICTORY_UI, VICTORY_UI_RECT, HELP_BUTTON, RED, DISCARD_UI, DISCARD_UI_RECT,\
    DISCARD_BUTTONS, DISCARD_PLAYER_WOOD_BUTTON, DISCARD_PLAYER_SHEEP_BUTTON, DISCARD_PLAYER_WHEAT_BUTTON, DISCARD_PLAYER_ORE_BUTTON,\
    DISCARD_PLAYER_BRICK_BUTTON, DISCARD_POOL_WOOD_BUTTON, DISCARD_POOL_SHEEP_BUTTON, DISCARD_POOL_WHEAT_BUTTON, DISCARD_POOL_ORE_BUTTON,\
    DISCARD_POOL_BRICK_BUTTON, DISCARD_BUTTON
from catan.game import Game
from catan.ai_agent import every_house_in_play
from catan.button import Button
from catan.timer import Timer

# Setting up the Pygame screen with the given screen size and initializing Pygame and Pygame font
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.init()
pygame.font.init()
# Creating the Pygame screen with the set screen size, and setting its caption and icon
SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Settlers Of Catan")
pygame.display.set_icon(ICON_32x)
# Setting up the Pygame clock and defining the game's frame rate
clock = pygame.time.Clock()
FPS = 60


def doesFileExists(filePathAndName):
    """
    Checks if a file or directory exists at the specified path.

    Parameters:
        filePathAndName (str): The path of the file or directory to check.

    Returns:
        bool: True if the file or directory exists, False otherwise.

    """
    return os.path.exists(filePathAndName)


def main_menu():
    """
    Pygame main menu function for starting and displaying the game menu.

    Parameters:
    None

    Returns:
    None

    Note:
    This function initializes various variables used in the game menu, such as the current game state,
    play option values and counters, player colors and names, and AI names. It then enters a while loop that continuously runs the game menu until
    an option is selected or the game is exited. The game menu displays the game options, such as game mode, number of players, and AI options, and
    allows the players to edit their names and colors. The function handles user input and updates the display accordingly. Once a valid option is
    selected, the function sets the corresponding play option values and exits the loop. The selected options are then passed on to the play function
    for the actual gameplay.
    """
    pygame.display.set_caption("Menu")
    game_state = "main menu"

    # play options helper counters
    game_mode_index = 0
    num_players_index = 0
    ai_option_index = 0
    name_plate_y_pos = 430

    # play option values
    game_modes = ["classic", "time trial"]
    num_players = [1, 2, 3, 4]
    ai_option = ["yes", "no"]
    color_list = COLOR_LIST.copy()
    color_image_list = COLOR_IMAGE_LIST.copy()

    # running play option values
    current_game_mode = "classic"
    time_trial = False
    current_num_players = 1
    current_ai_options = "yes"

    # edit players colors
    P1_color = color_list.pop(0)
    P2_color = color_list.pop(0)
    P3_color = color_list.pop(0)
    P4_color = color_list.pop(0)
    current_players_color_list = [P1_color, P2_color, P3_color, P4_color]

    P1_color_image = color_image_list.pop(0)
    P2_color_image = color_image_list.pop(0)
    P3_color_image = color_image_list.pop(0)
    P4_color_image = color_image_list.pop(0)

    # edit players values
    P1_name = "Bob"
    P2_name = "Jack"
    P3_name = "Sara"
    P4_name = "Mike"
    default_player_list = [P1_name, P2_name, P3_name, P4_name]
    default_player_list_2 = [P1_name, P2_name, P3_name, P4_name]

    # edit players name buttons
    player_1_button = None
    player_2_button = None
    player_3_button = None
    player_4_button = None

    player_button_list = []

    player_1_edit = False
    player_2_edit = False
    player_3_edit = False
    player_4_edit = False

    AI_1 = "AI Jack"
    AI_2 = "AI Sara"
    AI_3 = "AI Mike"
    default_ai_list = [AI_1, AI_2, AI_3]
    player_list = []
    edit_arrow_button_list = []

    while True:
        SCREEN.blit(MENU_BG.convert(), (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(MENU_TITLE_TEXT, MENU_TITLE_RECT)

        if game_state == "main menu":
            for butt in MENU_BUTTON_LIST:
                butt.change_color(menu_mouse_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MENU_BUTTON_LIST[0].check_for_input(menu_mouse_pos):
                        game_state = "play options"
                    if MENU_BUTTON_LIST[1].check_for_input(menu_mouse_pos):
                        if doesFileExists('./game_data.txt'):
                            with open('player_data.txt') as player_file:
                                player_data = json.load(player_file)
                                # load player names
                                load_player_names = list(player_data.keys())
                                load_color_list = []
                                for key, value in player_data.items():
                                    if value["color"] == [255, 0, 26]:
                                        load_color_list.append(COLOR_LIST[0])
                                    elif value["color"] == [255, 153, 1]:
                                        load_color_list.append(COLOR_LIST[1])
                                    elif value["color"] == [188, 23, 229]:
                                        load_color_list.append(COLOR_LIST[2])
                                    elif value["color"] == [102, 51, 255]:
                                        load_color_list.append(COLOR_LIST[3])
                                    elif value["color"] == [0, 255, 255]:
                                        load_color_list.append(COLOR_LIST[4])
                                    elif value["color"] == [165, 42, 42]:
                                        load_color_list.append(COLOR_LIST[5])
                                    elif value["color"] == [0, 0, 0]:
                                        load_color_list.append(COLOR_LIST[6])
                                    elif value["color"] == [255, 0, 255]:
                                        load_color_list.append(COLOR_LIST[7])

                                if doesFileExists("./timer_data.txt"):
                                    time_trial = True

                            play(True, load_player_names, load_color_list, time_trial)

                    if MENU_BUTTON_LIST[2].check_for_input(menu_mouse_pos):
                        pygame.quit()
                        sys.exit()

        elif game_state == "play options":
            SCREEN.blit(GAME_MODE_TEXT, GAME_MODE_TEXT_RECT)
            SCREEN.blit(NUM_PLAYERS_TEXT, NUM_PLAYERS_TEXT_RECT)
            SCREEN.blit(AI_TEXT, AI_TEXT_RECT)
            for butt in ARROW_BUTTON_LIST:
                butt.change_color(menu_mouse_pos)
                butt.update(SCREEN)

            for b in PLAY_OPTIONS_BUTTONS:
                b.change_color(menu_mouse_pos)
                b.update(SCREEN)
            game_mode_rect = GAME_MODES[game_mode_index].get_rect(center=(961, 548))
            SCREEN.blit(GAME_MODES[game_mode_index], game_mode_rect)

            num_players_rect = NUM_OF_PLAYERS[num_players_index].get_rect(center=(961, 703))
            SCREEN.blit(NUM_OF_PLAYERS[num_players_index], num_players_rect)

            ai_options_rect = NUM_OF_PLAYERS[num_players_index].get_rect(center=(961, 858))
            SCREEN.blit(AI_OPTION[ai_option_index], ai_options_rect)

            for i in range(current_num_players):
                if len(player_list) < current_num_players:
                    current_name = default_player_list.pop(0)
                    player_list.append(current_name)
                elif len(player_list) > current_num_players:
                    removed_name = player_list.pop(-1)
                    default_player_list = [removed_name] + default_player_list

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_PLAY_BUTTON.check_for_input(menu_mouse_pos):
                        game_state = "main menu"
                    if START_GAME_BUTTON.check_for_input(menu_mouse_pos):
                        player_list = []
                        for i in range(current_num_players + 1):
                            if i == 1:
                                player_list.append(P1_name)
                            elif i == 2:
                                player_list.append(P2_name)
                            elif i == 3:
                                player_list.append(P3_name)
                            elif i == 4:
                                player_list.append(P4_name)
                        print(player_list)
                        print(current_players_color_list)

                        if current_num_players < 4 and current_ai_options == "yes":
                            if current_num_players == 3:
                                player_list.append(default_ai_list[-1])
                            elif current_num_players == 2:
                                player_list.append(default_ai_list[1])
                                player_list.append(default_ai_list[-1])
                            elif current_num_players == 1:
                                player_list.append(default_ai_list[0])
                                player_list.append(default_ai_list[1])
                                player_list.append(default_ai_list[-1])

                        if current_game_mode == "time trial":
                            time_trial = True
                        play(False, player_list, current_players_color_list, time_trial)
                    if PALETTE_BUTTON.check_for_input(menu_mouse_pos):
                        game_state = "edit players"
                        print(player_list)
                    if ARROW_BUTTON_LIST[0].check_for_input(menu_mouse_pos):
                        if game_mode_index == 0:
                            game_mode_index = 1
                            current_game_mode = game_modes[game_mode_index]
                            print(current_game_mode)
                        else:
                            game_mode_index -= 1
                            current_game_mode = game_modes[game_mode_index]
                            print(current_game_mode)
                    if ARROW_BUTTON_LIST[1].check_for_input(menu_mouse_pos):
                        if game_mode_index == 1:
                            game_mode_index = 0
                            current_game_mode = game_modes[game_mode_index]
                            print(current_game_mode)
                        else:
                            game_mode_index += 1
                            current_game_mode = game_modes[game_mode_index]
                            print(current_game_mode)

                    if ARROW_BUTTON_LIST[2].check_for_input(menu_mouse_pos):
                        if num_players_index == 0:
                            num_players_index = 3
                            current_num_players = num_players[num_players_index]
                            print(current_num_players)
                        else:
                            num_players_index -= 1
                            current_num_players = num_players[num_players_index]
                            print(current_num_players)
                    if ARROW_BUTTON_LIST[3].check_for_input(menu_mouse_pos):
                        if num_players_index == 3:
                            num_players_index = 0
                            current_num_players = num_players[num_players_index]
                            print(current_num_players)
                        else:
                            num_players_index += 1
                            current_num_players = num_players[num_players_index]
                            print(current_num_players)

                    if ARROW_BUTTON_LIST[4].check_for_input(menu_mouse_pos):
                        if ai_option_index == 0:
                            ai_option_index = 1
                            current_ai_options = ai_option[ai_option_index]
                            print(current_ai_options)
                        else:
                            ai_option_index -= 1
                            current_ai_options = ai_option[ai_option_index]
                            print(current_ai_options)
                    if ARROW_BUTTON_LIST[5].check_for_input(menu_mouse_pos):
                        if ai_option_index == 1:
                            ai_option_index = 0
                            current_ai_options = ai_option[ai_option_index]
                            print(current_ai_options)
                        else:
                            ai_option_index += 1
                            current_ai_options = ai_option[ai_option_index]
                            print(current_ai_options)

        elif game_state == "edit players":
            SCREEN.blit(EDIT_PLAYERS_UI, EDIT_PLAYERS_UI_RECT)
            BACK_PLAY_BUTTON.change_color(menu_mouse_pos)
            BACK_PLAY_BUTTON.update(SCREEN)
            START_GAME_BUTTON.change_color(menu_mouse_pos)
            START_GAME_BUTTON.update(SCREEN)

            player_button_list = []
            edit_arrow_button_list = []
            for i in range(current_num_players):

                if i == 0:
                    player_1_button = Button(image=EDIT_NAME_PLATE, pos=(697, name_plate_y_pos),
                                             text_input="{}".format(P1_name), font=NUMBER_FONT, base_color=BLACK,
                                             hovering_color=(160, 32, 220))
                    player_button_list.append(player_1_button)

                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[0])
                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[1])
                    color_rect = P1_color_image.get_rect(center=(1214, 430))
                    SCREEN.blit(P1_color_image, color_rect)
                elif i == 1:
                    player_2_button = Button(image=EDIT_NAME_PLATE, pos=(697, name_plate_y_pos + 150),
                                             text_input="{}".format(P2_name), font=NUMBER_FONT, base_color=BLACK,
                                             hovering_color=(160, 32, 220))
                    player_button_list.append(player_2_button)

                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[2])
                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[3])
                    color_rect = P2_color_image.get_rect(center=(1214, 580))
                    SCREEN.blit(P2_color_image, color_rect)
                elif i == 2:
                    player_3_button = Button(image=EDIT_NAME_PLATE, pos=(697, name_plate_y_pos + 300),
                                             text_input="{}".format(P3_name), font=NUMBER_FONT, base_color=BLACK,
                                             hovering_color=(160, 32, 220))
                    player_button_list.append(player_3_button)

                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[4])
                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[5])
                    color_rect = P3_color_image.get_rect(center=(1214, 730))
                    SCREEN.blit(P3_color_image, color_rect)
                elif i == 3:
                    player_4_button = Button(image=EDIT_NAME_PLATE, pos=(697, name_plate_y_pos + 450),
                                             text_input="{}".format(P4_name), font=NUMBER_FONT, base_color=BLACK,
                                             hovering_color=(160, 32, 220))
                    player_button_list.append(player_4_button)

                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[6])
                    edit_arrow_button_list.append(EDIT_ARROWS_LIST[7])
                    color_rect = P4_color_image.get_rect(center=(1214, 880))
                    SCREEN.blit(P4_color_image, color_rect)

            for butt in player_button_list:
                butt.change_color(menu_mouse_pos)
                butt.update(SCREEN)

            for b in edit_arrow_button_list:
                b.change_color(menu_mouse_pos)
                b.update(SCREEN)

            if player_1_edit:
                pygame.draw.rect(SCREEN, (160, 32, 220), player_1_button, 5)
            if player_2_edit:
                pygame.draw.rect(SCREEN, (160, 32, 220), player_2_button, 5)
            if player_3_edit:
                pygame.draw.rect(SCREEN, (160, 32, 220), player_3_button, 5)
            if player_4_edit:
                pygame.draw.rect(SCREEN, (160, 32, 220), player_4_button, 5)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_PLAY_BUTTON.check_for_input(menu_mouse_pos):
                        game_state = "play options"

                    if EDIT_ARROWS_LIST[0].check_for_input(menu_mouse_pos) or EDIT_ARROWS_LIST[1].check_for_input(menu_mouse_pos):
                        color_list.append(P1_color)
                        P1_color = color_list.pop(0)
                        color_image_list.append(P1_color_image)
                        P1_color_image = color_image_list.pop(0)
                    if EDIT_ARROWS_LIST[2].check_for_input(menu_mouse_pos) or EDIT_ARROWS_LIST[3].check_for_input(menu_mouse_pos):
                        color_list.append(P2_color)
                        P2_color = color_list.pop(0)
                        color_image_list.append(P2_color_image)
                        P2_color_image = color_image_list.pop(0)
                    if EDIT_ARROWS_LIST[4].check_for_input(menu_mouse_pos) or EDIT_ARROWS_LIST[5].check_for_input(menu_mouse_pos):
                        color_list.append(P3_color)
                        P3_color = color_list.pop(0)
                        color_image_list.append(P3_color_image)
                        P3_color_image = color_image_list.pop(0)
                    if EDIT_ARROWS_LIST[6].check_for_input(menu_mouse_pos) or EDIT_ARROWS_LIST[7].check_for_input(menu_mouse_pos):
                        color_list.append(P4_color)
                        P4_color = color_list.pop(0)
                        color_image_list.append(P4_color_image)
                        P4_color_image = color_image_list.pop(0)

                    if player_1_button is not None:
                        if player_1_button.check_for_input(menu_mouse_pos):
                            player_1_edit = True
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = False
                            break
                        else:
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = False
                    if player_2_button is not None:
                        if player_2_button.check_for_input(menu_mouse_pos):
                            player_1_edit = False
                            player_2_edit = True
                            player_3_edit = False
                            player_4_edit = False
                            break
                        else:
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = False
                    if player_3_button is not None:
                        if player_3_button.check_for_input(menu_mouse_pos):
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = True
                            player_4_edit = False
                            break
                        else:
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = False
                    if player_4_button is not None:
                        if player_4_button.check_for_input(menu_mouse_pos):
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = True
                            break
                        else:
                            player_1_edit = False
                            player_2_edit = False
                            player_3_edit = False
                            player_4_edit = False

                    if START_GAME_BUTTON.check_for_input(menu_mouse_pos):
                        player_list = []
                        current_players_color_list = []
                        for i in range(current_num_players + 1):
                            if i == 1:
                                player_list.append(P1_name)
                                current_players_color_list.append(P1_color)
                            elif i == 2:
                                player_list.append(P2_name)
                                current_players_color_list.append(P2_color)
                            elif i == 3:
                                player_list.append(P3_name)
                                current_players_color_list.append(P3_color)
                            elif i == 4:
                                player_list.append(P4_name)
                                current_players_color_list.append(P4_color)
                        print(player_list)
                        print(current_players_color_list)

                        if current_num_players < 4 and current_ai_options == "yes":
                            if current_num_players == 3:
                                player_list.append(default_ai_list[-1])
                                current_players_color_list.append(color_list.pop(0))
                            elif current_num_players == 2:
                                player_list.append(default_ai_list[1])
                                player_list.append(default_ai_list[-1])
                                current_players_color_list.append(color_list.pop(0))
                                current_players_color_list.append(color_list.pop(0))
                            elif current_num_players == 1:
                                player_list.append(default_ai_list[0])
                                player_list.append(default_ai_list[1])
                                player_list.append(default_ai_list[-1])
                                current_players_color_list.append(color_list.pop(0))
                                current_players_color_list.append(color_list.pop(0))
                                current_players_color_list.append(color_list.pop(0))

                            if current_game_mode == "time trial":
                                time_trial = True
                        play(False, player_list, current_players_color_list, time_trial)

                if event.type == pygame.KEYDOWN:
                    if player_1_edit:
                        if event.key == pygame.K_BACKSPACE:
                            P1_name = P1_name[:-1]
                            print(P1_name)
                            print(player_list)
                            break
                        else:
                            P1_name += event.unicode
                            print(P1_name)
                            break
                    elif player_2_edit:
                        if event.key == pygame.K_BACKSPACE:
                            P2_name = P2_name[:-1]
                            print(P2_name)
                            break
                        else:
                            P2_name += event.unicode
                            print(P2_name)
                            break
                    elif player_3_edit:
                        if event.key == pygame.K_BACKSPACE:
                            P3_name = P3_name[:-1]
                            print(P3_name)
                            break
                        else:
                            P3_name += event.unicode
                            print(P3_name)
                            break
                    elif player_4_edit:
                        if event.key == pygame.K_BACKSPACE:
                            P4_name = P4_name[:-1]
                            print(P4_name)
                            break
                        else:
                            P4_name += event.unicode
                            print(P4_name)
                            break

        pygame.display.update()
        clock.tick(FPS)


def play(load_game=False, players_names=("YOU", "MESSED", "UP", "BAD"), color_list=COLOR_LIST, time_trial = False):
    """
    Pygame play function to start and run the Catan game.

    Parameters:
    load_game (bool, optional): Indicates if a saved game will be loaded. Defaults to False.
    players_names (tuple of str, optional): A tuple of the names of the players. Defaults to ("YOU", "MESSED", "UP", "BAD").
    color_list (list of tuple of int, optional): A list of RGB tuples representing the colors of the players. Defaults to COLOR_LIST.
    time_trial (bool, optional): Indicates if the game will be played with a time trial. Defaults to False.

    Returns:
    None

    Note:
    This function creates a new game instance and initializes all the necessary game components such as the board, players, and bank.
    It runs the game loop until the game is finished or exited, during which it updates the screen, handles user input and game logic,
    and displays messages to the players. If a saved game is loaded, the function restores the game state from the saved data.
    The function also provides error messages for various game scenarios and helpers for dev cards and discarding resources.
    """
    # Set run flag to True
    run = True

    # Create a timer object if time trial is enabled
    if time_trial:
        timer = Timer(SCREEN)

    # Create a new game object, passing in player names and color list
    new_game = Game(players_names, color_list)

    # If loading a saved game, load player, board, bank, and game data, and unpause timer if time trial is enabled
    if load_game:
        new_game.load_player_data()
        new_game.load_board_data()
        new_game.load_bank_data()
        new_game.load_game_data()
        if time_trial:
            timer.load()
            timer.unpause()
        # Set game state to "default" if loading a saved game
        game_state = "default"
    # If not loading a saved game, set game state to "initial house placements P1"
    else:
        game_state = "initial house placements P1"

    # Set counters for road and resource cards
    road_counter = 0
    resource_counter = 0

    # Set empty list for players who need to discard cards
    PLAYERS_TO_DISCARD = []

    # Set error messages for various scenarios
    RESOURCE_ERROR = "Not enough resources to place that!"
    ZONE_OF_CONTROL_ERROR = "Too close to other players to place that!"
    ALLOWANCE_ERROR = "You have run out of that placement type!"
    ROAD_ERROR = "You must place a road off the house you just placed!"
    ROAD_ERROR_2 = "You must place a road off an existing house or road!"
    HOUSE_ERROR = "You must place a road off an existing road!"
    CITY_ERROR = "Must upgrade an existing house to a city!"
    NO_ERROR = ""
    CURRENT_ERROR_MESSAGE = NO_ERROR

    # Game loop
    while run:
        # Limit the frame rate
        dt = clock.tick(FPS)

        # Set current player to the current_player in Game class
        current_player = new_game.get_current_player()

        # Draw everything
        new_game.draw_board(SCREEN)  # Draws the game board on the screen
        new_game.draw_players_resources(SCREEN)  # Draws the resources of each player on the screen
        new_game.update_state(SCREEN)  # Updates the state of the game
        new_game.draw_house(SCREEN)  # Draws the houses of each player on the screen
        new_game.draw_city(SCREEN)  # Draws the cities of each player on the screen
        new_game.draw_robber(SCREEN)  # Draws the robber on the screen
        new_game.draw_flags(SCREEN)  # Draws the flags on the screen
        new_game.draw_player_bank_ratios(SCREEN, current_player)  # Draws the bank ratios of each player on the screen
        new_game.ui_Messages(SCREEN, game_state, current_player)  # Draws the user interface messages on the screen

        if time_trial:
            timer.update(dt)  # If it is a time trial game, updates the timer with the time elapsed
        else:
            if new_game.check_game_over(current_player):  # Checks if the game is over for the current player
                game_state = "victory screen"  # If the game is over, sets the game state to "victory screen"

        mos_pos = pygame.mouse.get_pos()  # Gets the current mouse position on the screen

        """
        
        GAME STATES:
        
        """

        # initial HOUSE placements for player 1
        if game_state == "initial house placements P1":
            error_message = NUMBER_FONT.render(CURRENT_ERROR_MESSAGE, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            chosen_house_p1 = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for pos in new_game.house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            if new_game.isnt_to_close_to_other_houses(pos):
                                print(current_player.get_name(), "placed a house at", pos)
                                current_player.add_house(pos)
                                current_player.add_victory_point()
                                # remove the pos from the list
                                new_game.house_positions.remove(pos)
                                if new_game.get_AI_player() is not False:
                                    every_house_in_play.append(pos)
                                chosen_house_p1 = pos
                                CURRENT_ERROR_MESSAGE = NO_ERROR
                                game_state = "initial road placements P1"
                            else:
                                CURRENT_ERROR_MESSAGE = ZONE_OF_CONTROL_ERROR
        # initial ROAD placements for player 1
        elif game_state == "initial road placements P1":
            error_message = NUMBER_FONT.render(ROAD_ERROR, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    roads_next_to_house = []
                    for road in new_game.road_positions:
                        if road[0] == chosen_house_p1 or road[1] == chosen_house_p1:
                            roads_next_to_house.append(road)

                    for pos_2 in roads_next_to_house:
                        start_point = pos_2[0]
                        end_point = pos_2[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 20

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            # Add the road to the player's list of roads
                            CURRENT_ERROR_MESSAGE = NO_ERROR
                            current_player.add_road(pos_2)
                            new_game.road_positions.remove(pos_2)
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            if len(current_player.get_roads()) == 2:
                                game_state = "dice roll"
                            else:
                                new_game.end_turn()

                                game_state = "initial house placements P2+"
        # initial HOUSE placements for players 2+
        elif game_state == "initial house placements P2+":
            error_message = NUMBER_FONT.render(CURRENT_ERROR_MESSAGE, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            # AI agent control
            if "AI" in current_player.get_name():
                road_pos, house_pos = current_player.make_decision("initial house placements P2+",
                                                                   new_game.road_positions, new_game.house_positions)
                new_game.road_positions = road_pos
                new_game.house_positions = house_pos
                game_state = "initial road placements P2+"

            # user input control
            chosen_house_P2 = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for pos in new_game.house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            if new_game.isnt_to_close_to_other_houses(pos):
                                print(current_player.get_name(), "placed a house at", pos)
                                current_player.add_house(pos)
                                current_player.add_victory_point()
                                # remove the pos from the list
                                new_game.house_positions.remove(pos)
                                if new_game.get_AI_player() is not False:
                                    every_house_in_play.append(pos)
                                chosen_house_P2 = pos
                                CURRENT_ERROR_MESSAGE = NO_ERROR
                                game_state = "initial road placements P2+"
                            else:
                                CURRENT_ERROR_MESSAGE = ZONE_OF_CONTROL_ERROR
        # initial ROAD placements for players 2+
        elif game_state == "initial road placements P2+":
            error_message = NUMBER_FONT.render(ROAD_ERROR, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            # AI agent control
            if "AI" in current_player.get_name():
                road_pos, house_pos = current_player.make_decision("initial road placements P2+",
                                                                   new_game.road_positions, new_game.house_positions)
                new_game.road_positions = road_pos
                new_game.house_positions = house_pos
                if len(current_player.get_roads()) == 2 and current_player is not new_game.get_players()[-1]:

                    new_game.end_turn()
                    game_state = "initial house placements P2+"
                elif len(current_player.get_roads()) == 1:

                    game_state = "initial house placements P2+"
                else:

                    new_game.end_turn()
                    game_state = "initial house placements P1"

            # player input control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    roads_next_to_house = []
                    for road in new_game.road_positions:
                        if road[0] == chosen_house_P2 or road[1] == chosen_house_P2:
                            roads_next_to_house.append(road)

                    for pos_2 in roads_next_to_house:
                        start_point = pos_2[0]
                        end_point = pos_2[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 20

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            # Add the road to the player's list of roads
                            CURRENT_ERROR_MESSAGE = NO_ERROR
                            current_player.add_road(pos_2)
                            new_game.road_positions.remove(pos_2)
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            if len(current_player.get_roads()) == 2 and current_player is not new_game.get_players()[
                                -1]:
                                new_game.end_turn()
                                game_state = "initial house placements P2+"
                            elif len(current_player.get_roads()) == 1:
                                game_state = "initial house placements P2+"
                            else:
                                new_game.end_turn()
                                game_state = "initial house placements P1"

        # dice roll game state
        elif game_state == "dice roll":
            if "AI" in current_player.get_name():
                current_player.roll_dice()
                new_game.give_resources(current_player)
                print(current_player.get_name(), "rolled a", current_player.get_dice_number())
                if current_player.get_dice_number() == 7:
                    game_state = "discard"
                else:
                    game_state = "default"

            ROLL_DICE_BUTTON.change_color(mos_pos)
            ROLL_DICE_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ROLL_DICE_BUTTON.check_for_input(mos_pos):
                        current_player.roll_dice()
                        new_game.give_resources(current_player)
                        print(current_player.get_name(), "rolled a", current_player.get_dice_number())
                        if current_player.get_dice_number() == 7:
                            game_state = "discard"
                        else:
                            game_state = "default"
        # robber game state
        elif game_state == "robber":
            if "AI" in current_player.get_name():
                robber_pos = random.choice(list(new_game.possible_robber_pos.items()))
                print(current_player.get_name(), "placed the robber at", robber_pos[1])
                new_game.update_robber_pos(new_game.current_board[robber_pos[0]]["position"])
                new_game.update_robber_pos_list()
                new_game.remove_robber_pos()
                game_state = "default"

            for key, value in new_game.possible_robber_pos.copy().items():
                pygame.draw.circle(SCREEN, (160, 32, 240), value, 15, 5)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for key, pos in new_game.possible_robber_pos.copy().items():
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            print(current_player.get_name(), "placed the robber at", pos)
                            new_game.update_robber_pos(new_game.current_board[key]["position"])
                            new_game.robber_take_resource_from_rand_player(current_player)
                            new_game.update_robber_pos_list()
                            new_game.remove_robber_pos()
                            game_state = "default"
        # discard game state
        elif game_state == "discard":

            PLAYERS_TO_DISCARD = new_game.player_list_with_7_resources_or_more()

            if PLAYERS_TO_DISCARD:
                for p in PLAYERS_TO_DISCARD:
                    p.update_discard_amount()
                game_state = "discard player 1"
            else:
                game_state = "robber"
        # discard player states
        elif game_state == "discard player 1":
            discard_player = PLAYERS_TO_DISCARD[0]
            if "AI" in discard_player.get_name():
                discard_list = discard_player.make_list_of_resources_to_str()
                discard_amount = discard_player.discard_amount
                to_remove = random.sample(discard_list, discard_amount)
                discard_player.remove_resources_from_list(to_remove)
                new_game.bank.add_resources_from_list(to_remove)
                if len(PLAYERS_TO_DISCARD) >= 2:
                    game_state = "discard player 2"
                else:
                    game_state = "robber"


            current_player.draw_dice(SCREEN)
            message = NUMBER_FONT.render("Ready player {}!".format(discard_player.get_name()), True,
                                         discard_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            SCREEN.blit(message, message_rect)
            new_game.draw_trade_dev_buttons(SCREEN)

            SCREEN.blit(DISCARD_UI, DISCARD_UI_RECT)
            new_game.draw_numbers_in_discard(SCREEN, discard_player)

            discard_text = NUMBER_FONT.render("DISCARD {} CARDS!".format(discard_player.discard_amount), True, BLACK)
            discard_text_rect = discard_text.get_rect(center=(960, 590))
            SCREEN.blit(discard_text, discard_text_rect)
            for butt in DISCARD_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DISCARD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_amount == 0:
                            new_game.give_resource_from_discard_to_bank(discard_player)
                            if len(PLAYERS_TO_DISCARD) >= 2:
                                game_state = "discard player 2"
                            else:
                                game_state = "robber"

                    elif DISCARD_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.resources["forest"] > 0 and discard_player.discard_amount > 0:
                            discard_player.remove_resource("forest")
                            discard_player.add_resource_to_discard_pool("forest")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["pasture"] > 0:
                            discard_player.remove_resource("pasture")
                            discard_player.add_resource_to_discard_pool("pasture")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["fields"] > 0:
                            discard_player.remove_resource("fields")
                            discard_player.add_resource_to_discard_pool("fields")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_ORE_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["mountains"] > 0:
                            discard_player.remove_resource("mountains")
                            discard_player.add_resource_to_discard_pool("mountains")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_BRICK_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["hills"] > 0:
                            discard_player.remove_resource("hills")
                            discard_player.add_resource_to_discard_pool("hills")
                            discard_player.remove_discard_amount()

                    elif DISCARD_POOL_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["forest"] > 0:
                            discard_player.remove_resource_from_discard_pool("forest")
                            discard_player.add_resource("forest")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_SHEEP_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["pasture"] > 0:
                            discard_player.remove_resource_from_discard_pool("pasture")
                            discard_player.add_resource("pasture")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_WHEAT_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["fields"] > 0:
                            discard_player.remove_resource_from_discard_pool("fields")
                            discard_player.add_resource("fields")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_ORE_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["mountains"] > 0:
                            discard_player.remove_resource_from_discard_pool("mountains")
                            discard_player.add_resource("mountains")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_BRICK_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["hills"] > 0:
                            discard_player.remove_resource_from_discard_pool("hills")
                            discard_player.add_resource("hills")
                            discard_player.add_discard_amount()
        elif game_state == "discard player 2":
            discard_player = PLAYERS_TO_DISCARD[1]
            if "AI" in discard_player.get_name():
                discard_list = discard_player.make_list_of_resources_to_str()
                discard_amount = discard_player.discard_amount
                to_remove = random.sample(discard_list, discard_amount)
                discard_player.remove_resources_from_list(to_remove)
                new_game.bank.add_resources_from_list(to_remove)
                if len(PLAYERS_TO_DISCARD) >= 3:
                    game_state = "discard player 3"
                else:
                    game_state = "robber"

            current_player.draw_dice(SCREEN)
            message = NUMBER_FONT.render("Ready player {}!".format(discard_player.get_name()), True,
                                         discard_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            SCREEN.blit(message, message_rect)
            new_game.draw_trade_dev_buttons(SCREEN)

            SCREEN.blit(DISCARD_UI, DISCARD_UI_RECT)
            new_game.draw_numbers_in_discard(SCREEN, discard_player)

            discard_text = NUMBER_FONT.render("DISCARD {} CARDS!".format(discard_player.discard_amount), True, BLACK)
            discard_text_rect = discard_text.get_rect(center=(960, 590))
            SCREEN.blit(discard_text, discard_text_rect)
            for butt in DISCARD_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DISCARD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_amount == 0:
                            new_game.give_resource_from_discard_to_bank(discard_player)
                            if len(PLAYERS_TO_DISCARD) >= 3:
                                game_state = "discard player 3"
                            else:
                                game_state = "robber"

                    elif DISCARD_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.resources["forest"] > 0 and discard_player.discard_amount > 0:
                            discard_player.remove_resource("forest")
                            discard_player.add_resource_to_discard_pool("forest")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["pasture"] > 0:
                            discard_player.remove_resource("pasture")
                            discard_player.add_resource_to_discard_pool("pasture")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["fields"] > 0:
                            discard_player.remove_resource("fields")
                            discard_player.add_resource_to_discard_pool("fields")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_ORE_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["mountains"] > 0:
                            discard_player.remove_resource("mountains")
                            discard_player.add_resource_to_discard_pool("mountains")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_BRICK_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["hills"] > 0:
                            discard_player.remove_resource("hills")
                            discard_player.add_resource_to_discard_pool("hills")
                            discard_player.remove_discard_amount()

                    elif DISCARD_POOL_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["forest"] > 0:
                            discard_player.remove_resource_from_discard_pool("forest")
                            discard_player.add_resource("forest")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_SHEEP_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["pasture"] > 0:
                            discard_player.remove_resource_from_discard_pool("pasture")
                            discard_player.add_resource("pasture")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_WHEAT_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["fields"] > 0:
                            discard_player.remove_resource_from_discard_pool("fields")
                            discard_player.add_resource("fields")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_ORE_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["mountains"] > 0:
                            discard_player.remove_resource_from_discard_pool("mountains")
                            discard_player.add_resource("mountains")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_BRICK_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["hills"] > 0:
                            discard_player.remove_resource_from_discard_pool("hills")
                            discard_player.add_resource("hills")
                            discard_player.add_discard_amount()
        elif game_state == "discard player 3":
            discard_player = PLAYERS_TO_DISCARD[2]
            if "AI" in discard_player.get_name():
                discard_list = discard_player.make_list_of_resources_to_str()
                discard_amount = discard_player.discard_amount
                to_remove = random.sample(discard_list, discard_amount)
                discard_player.remove_resources_from_list(to_remove)
                new_game.bank.add_resources_from_list(to_remove)
                if len(PLAYERS_TO_DISCARD) >= 4:
                    game_state = "discard player 4"
                else:
                    game_state = "robber"

            current_player.draw_dice(SCREEN)
            message = NUMBER_FONT.render("Ready player {}!".format(discard_player.get_name()), True,
                                         discard_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            SCREEN.blit(message, message_rect)
            new_game.draw_trade_dev_buttons(SCREEN)

            SCREEN.blit(DISCARD_UI, DISCARD_UI_RECT)
            new_game.draw_numbers_in_discard(SCREEN, discard_player)

            discard_text = NUMBER_FONT.render("DISCARD {} CARDS!".format(discard_player.discard_amount), True, BLACK)
            discard_text_rect = discard_text.get_rect(center=(960, 590))
            SCREEN.blit(discard_text, discard_text_rect)
            for butt in DISCARD_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DISCARD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_amount == 0:
                            new_game.give_resource_from_discard_to_bank(discard_player)
                            if len(PLAYERS_TO_DISCARD) >= 4:
                                game_state = "discard player 4"
                            else:
                                game_state = "robber"

                    elif DISCARD_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.resources["forest"] > 0 and discard_player.discard_amount > 0:
                            discard_player.remove_resource("forest")
                            discard_player.add_resource_to_discard_pool("forest")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["pasture"] > 0:
                            discard_player.remove_resource("pasture")
                            discard_player.add_resource_to_discard_pool("pasture")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["fields"] > 0:
                            discard_player.remove_resource("fields")
                            discard_player.add_resource_to_discard_pool("fields")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_ORE_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["mountains"] > 0:
                            discard_player.remove_resource("mountains")
                            discard_player.add_resource_to_discard_pool("mountains")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_BRICK_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["hills"] > 0:
                            discard_player.remove_resource("hills")
                            discard_player.add_resource_to_discard_pool("hills")
                            discard_player.remove_discard_amount()

                    elif DISCARD_POOL_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["forest"] > 0:
                            discard_player.remove_resource_from_discard_pool("forest")
                            discard_player.add_resource("forest")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_SHEEP_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["pasture"] > 0:
                            discard_player.remove_resource_from_discard_pool("pasture")
                            discard_player.add_resource("pasture")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_WHEAT_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["fields"] > 0:
                            discard_player.remove_resource_from_discard_pool("fields")
                            discard_player.add_resource("fields")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_ORE_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["mountains"] > 0:
                            discard_player.remove_resource_from_discard_pool("mountains")
                            discard_player.add_resource("mountains")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_BRICK_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["hills"] > 0:
                            discard_player.remove_resource_from_discard_pool("hills")
                            discard_player.add_resource("hills")
                            discard_player.add_discard_amount()
        elif game_state == "discard player 4":
            discard_player = PLAYERS_TO_DISCARD[3]
            if "AI" in discard_player.get_name():
                discard_list = discard_player.make_list_of_resources_to_str()
                discard_amount = discard_player.discard_amount
                to_remove = random.sample(discard_list, discard_amount)
                discard_player.remove_resources_from_list(to_remove)
                new_game.bank.add_resources_from_list(to_remove)
                game_state = "robber"

            current_player.draw_dice(SCREEN)
            message = NUMBER_FONT.render("Ready player {}!".format(discard_player.get_name()), True,
                                         discard_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            SCREEN.blit(message, message_rect)
            new_game.draw_trade_dev_buttons(SCREEN)

            SCREEN.blit(DISCARD_UI, DISCARD_UI_RECT)
            new_game.draw_numbers_in_discard(SCREEN, discard_player)

            discard_text = NUMBER_FONT.render("DISCARD {} CARDS!".format(discard_player.discard_amount), True, BLACK)
            discard_text_rect = discard_text.get_rect(center=(960, 590))
            SCREEN.blit(discard_text, discard_text_rect)
            for butt in DISCARD_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if DISCARD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_amount == 0:
                            new_game.give_resource_from_discard_to_bank(discard_player)
                            game_state = "robber"

                    elif DISCARD_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.resources["forest"] > 0 and discard_player.discard_amount > 0:
                            discard_player.remove_resource("forest")
                            discard_player.add_resource_to_discard_pool("forest")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["pasture"] > 0:
                            discard_player.remove_resource("pasture")
                            discard_player.add_resource_to_discard_pool("pasture")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["fields"] > 0:
                            discard_player.remove_resource("fields")
                            discard_player.add_resource_to_discard_pool("fields")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_ORE_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["mountains"] > 0:
                            discard_player.remove_resource("mountains")
                            discard_player.add_resource_to_discard_pool("mountains")
                            discard_player.remove_discard_amount()
                    elif DISCARD_PLAYER_BRICK_BUTTON.check_for_input(mos_pos) and discard_player.discard_amount > 0:
                        if discard_player.resources["hills"] > 0:
                            discard_player.remove_resource("hills")
                            discard_player.add_resource_to_discard_pool("hills")
                            discard_player.remove_discard_amount()

                    elif DISCARD_POOL_WOOD_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["forest"] > 0:
                            discard_player.remove_resource_from_discard_pool("forest")
                            discard_player.add_resource("forest")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_SHEEP_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["pasture"] > 0:
                            discard_player.remove_resource_from_discard_pool("pasture")
                            discard_player.add_resource("pasture")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_WHEAT_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["fields"] > 0:
                            discard_player.remove_resource_from_discard_pool("fields")
                            discard_player.add_resource("fields")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_ORE_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["mountains"] > 0:
                            discard_player.remove_resource_from_discard_pool("mountains")
                            discard_player.add_resource("mountains")
                            discard_player.add_discard_amount()
                    elif DISCARD_POOL_BRICK_BUTTON.check_for_input(mos_pos):
                        if discard_player.discard_pool["hills"] > 0:
                            discard_player.remove_resource_from_discard_pool("hills")
                            discard_player.add_resource("hills")
                            discard_player.add_discard_amount()

        # default game state
        elif game_state == "default":
            if "AI" in current_player.get_name():
                if current_player.has_enough_resources('road') and not current_player.has_enough_resources('house'):
                    game_state = "place road"
                elif current_player.has_enough_resources('road') and current_player.has_enough_resources('house'):
                    game_state = "place house"
                else:
                    surplus_resources, needed_resources = current_player.trade_with_bank()
                    if surplus_resources and needed_resources:
                        for surplus in surplus_resources:
                            if len(needed_resources) >= 1:
                                needed = needed_resources.pop(-1)
                                if new_game.bank.get_bank_resource(needed) > 0:
                                    print(current_player.get_name(), "traded {} {} for 1 {}".format(current_player.get_trade_ratios()[surplus][0],
                                                                                                  surplus, needed))
                                    current_player.add_resource(needed)
                                    current_player.remove_resource_with_amount(surplus,
                                                                               current_player.get_trade_ratios()[surplus][0])
                                    new_game.bank.add_bank_resources_with_amount(surplus,
                                                                                 current_player.get_trade_ratios()[surplus][0])
                                    new_game.bank.remove_resources(needed)
                                    if time_trial and current_player == new_game.players[-1]:
                                        if timer.remaining_time == 0:
                                            game_state = "victory screen"
                                        else:
                                            new_game.end_turn()
                                            game_state = "dice roll"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"

                                else:
                                    if time_trial and current_player == new_game.players[-1]:
                                        if timer.remaining_time == 0:
                                            game_state = "victory screen"
                                        else:
                                            new_game.end_turn()
                                            game_state = "dice roll"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"

                            else:
                                if time_trial and current_player == new_game.players[-1]:
                                    if timer.remaining_time == 0:
                                        game_state = "victory screen"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"
                                else:
                                    new_game.end_turn()
                                    game_state = "dice roll"
                    else:
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"

            # loop through each button in the games UI
            for butt in UI_BUTTONS:
                # change color if hovered
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if END_TURN_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "ended their turn")
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"
                    if PLACE_HOUSE_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to place a HOUSE")
                        game_state = "place house"
                    if PLACE_ROAD_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to place a ROAD")
                        game_state = "place road"
                    if PLACE_CITY_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to place a CITY")
                        game_state = "place city"
                    if DEV_CARDS_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "opened Dev Cards")
                        game_state = "dev cards"
                    if SHEEP_BUTTON.check_for_input(mos_pos):
                        game_state = "bank sheep"
                    if WOOD_BUTTON.check_for_input(mos_pos):
                        game_state = "bank wood"
                    if WHEAT_BUTTON.check_for_input(mos_pos):
                        game_state = "bank wheat"
                    if ORE_BUTTON.check_for_input(mos_pos):
                        game_state = "bank ore"
                    if BRICK_BUTTON.check_for_input(mos_pos):
                        game_state = "bank brick"
                    if DEV_BUTTON.check_for_input(mos_pos):
                        game_state = "bank dev"
                    if PLAYER_TRADING_BUTTON.check_for_input(mos_pos):
                        game_state = "pick player for trade"
                    if PAUSE_BUTTON.check_for_input(mos_pos):
                        game_state = "pause menu"
                    if HELP_BUTTON.check_for_input(mos_pos):
                        game_state = "help menu"

        # implement place house state
        elif game_state == "place house":
            error_message = NUMBER_FONT.render(CURRENT_ERROR_MESSAGE, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            if "AI" in current_player.get_name():
                place_bool, road_pos, house_pos = current_player.make_decision("place house", new_game.road_positions,
                                                                               new_game.house_positions)
                if place_bool:

                    new_game.road_positions = road_pos
                    new_game.house_positions = house_pos
                    new_game.bank.add_bank_resources_from_placement('house')
                    if time_trial and current_player == new_game.players[-1]:
                        if timer.remaining_time == 0:
                            game_state = "victory screen"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"
                    else:
                        new_game.end_turn()
                        game_state = "dice roll"
                else:
                    game_state = "place road"

            for butt in PLACE_HOUSE_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if END_TURN_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "ended their turn")
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                CURRENT_ERROR_MESSAGE = NO_ERROR
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            CURRENT_ERROR_MESSAGE = NO_ERROR
                            game_state = "dice roll"
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        CURRENT_ERROR_MESSAGE = NO_ERROR
                        game_state = "default"

                    # checks if the mouse clicked on any of the house positions within a 20 pixel buffer
                    for pos in new_game.house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            if current_player.house_allowance():
                                if current_player.is_valid_house_placement(pos):
                                    if current_player.has_enough_resources("house"):
                                        if new_game.isnt_to_close_to_other_houses(pos):
                                            print(current_player.get_name(), "placed a house at", pos)
                                            current_player.add_house(pos)
                                            if new_game.get_AI_player() is not False:
                                                every_house_in_play.append(pos)
                                            current_player.add_victory_point()
                                            current_player.remove_resources_for_placement('house')
                                            new_game.bank.add_bank_resources_from_placement('house')

                                            # remove the pos from the list
                                            new_game.house_positions.remove(pos)
                                            CURRENT_ERROR_MESSAGE = NO_ERROR
                                        else:
                                            CURRENT_ERROR_MESSAGE = ZONE_OF_CONTROL_ERROR
                                    else:
                                        CURRENT_ERROR_MESSAGE = RESOURCE_ERROR
                                else:
                                    CURRENT_ERROR_MESSAGE = HOUSE_ERROR
                            else:
                                CURRENT_ERROR_MESSAGE = ALLOWANCE_ERROR

        # implement place road state
        elif game_state == "place road":
            error_message = NUMBER_FONT.render(CURRENT_ERROR_MESSAGE, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            if "AI" in current_player.get_name():
                place_bool, road_pos, house_pos = current_player.make_decision("place road", new_game.road_positions,
                                                                               new_game.house_positions)
                if place_bool:

                    new_game.road_positions = road_pos
                    new_game.house_positions = house_pos
                    new_game.update_longest_road_player()
                    new_game.bank.add_bank_resources_from_placement('road')
                    if time_trial and current_player == new_game.players[-1]:
                        if timer.remaining_time == 0:
                            game_state = "victory screen"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"
                    else:
                        new_game.end_turn()
                        game_state = "dice roll"
                else:
                    surplus_resources, needed_resources = current_player.trade_with_bank()
                    if surplus_resources and needed_resources:
                        for surplus in surplus_resources:
                            if len(needed_resources) >= 1:
                                needed = needed_resources.pop(-1)
                                if new_game.bank.get_bank_resource(needed) > 0:
                                    print(current_player.get_name(),
                                          "traded {} {} for 1 {}".format(current_player.get_trade_ratios()[surplus][0],
                                                                         surplus, needed))
                                    current_player.add_resource(needed)
                                    current_player.remove_resource_with_amount(surplus,
                                                                               current_player.get_trade_ratios()[
                                                                                   surplus][0])
                                    new_game.bank.add_bank_resources_with_amount(surplus,
                                                                                 current_player.get_trade_ratios()[
                                                                                     surplus][0])
                                    new_game.bank.remove_resources(needed)
                                    if time_trial and current_player == new_game.players[-1]:
                                        if timer.remaining_time == 0:
                                            game_state = "victory screen"
                                        else:
                                            new_game.end_turn()
                                            game_state = "dice roll"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"

                                else:
                                    if time_trial and current_player == new_game.players[-1]:
                                        if timer.remaining_time == 0:
                                            game_state = "victory screen"
                                        else:
                                            new_game.end_turn()
                                            game_state = "dice roll"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"
                            else:
                                if time_trial and current_player == new_game.players[-1]:
                                    if timer.remaining_time == 0:
                                        game_state = "victory screen"
                                    else:
                                        new_game.end_turn()
                                        game_state = "dice roll"
                                else:
                                    new_game.end_turn()
                                    game_state = "dice roll"
                    else:
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"

            for butt in PLACE_ROAD_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        CURRENT_ERROR_MESSAGE = NO_ERROR
                        game_state = 'default'
                    if END_TURN_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "ended their turn")
                        CURRENT_ERROR_MESSAGE = NO_ERROR
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"
                    # Check if the click is within the clickable area for any of the lines
                    for pos in new_game.road_positions:
                        start_point = pos[0]
                        end_point = pos[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 20

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            if current_player.road_allowance():
                                if current_player.is_valid_road_placement(pos):
                                    if current_player.has_enough_resources('road'):
                                        # Add the road to the player's list of roads
                                        print(current_player.get_name(),
                                              "placed a road from {} to {}".format(start_point, end_point))
                                        current_player.add_road(pos)
                                        new_game.update_longest_road_player()
                                        current_player.remove_resources_for_placement('road')
                                        new_game.bank.add_bank_resources_from_placement('road')
                                        new_game.road_positions.remove(pos)
                                        CURRENT_ERROR_MESSAGE = NO_ERROR
                                    else:
                                        CURRENT_ERROR_MESSAGE = RESOURCE_ERROR
                                else:
                                    CURRENT_ERROR_MESSAGE = ROAD_ERROR_2
                            else:
                                CURRENT_ERROR_MESSAGE = ALLOWANCE_ERROR
        # place city state
        elif game_state == "place city":
            error_message = NUMBER_FONT.render(CITY_ERROR, True, RED)
            error_rect = error_message.get_rect(center=(960, 980))
            SCREEN.blit(error_message, error_rect)
            error_message_2 = NUMBER_FONT.render(CURRENT_ERROR_MESSAGE, True, RED)
            error_rect_2 = error_message_2.get_rect(center=(960, 1020))
            SCREEN.blit(error_message_2, error_rect_2)
            for butt in PLACE_HOUSE_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if END_TURN_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "ended their turn")
                        CURRENT_ERROR_MESSAGE = NO_ERROR
                        if time_trial and current_player == new_game.players[-1]:
                            if timer.remaining_time == 0:
                                game_state = "victory screen"
                            else:
                                new_game.end_turn()
                                game_state = "dice roll"
                        else:
                            new_game.end_turn()
                            game_state = "dice roll"
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        CURRENT_ERROR_MESSAGE = NO_ERROR
                        game_state = "default"

                    # checks if the mouse clicked on any of the house positions within a 20 pixel buffer
                    for pos in current_player.get_house():
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            if current_player.city_allowance():
                                if current_player.is_valid_house_placement(pos):
                                    if current_player.has_enough_resources("city"):
                                        print(current_player.get_name(), "placed a city at", pos)
                                        current_player.add_city(pos)
                                        current_player.remove_house(pos)
                                        current_player.add_victory_point()
                                        current_player.remove_resources_for_placement('city')
                                        new_game.bank.add_bank_resources_from_placement('city')
                                        CURRENT_ERROR_MESSAGE = NO_ERROR
                                    else:
                                        CURRENT_ERROR_MESSAGE = RESOURCE_ERROR
                                else:
                                    CURRENT_ERROR_MESSAGE = CITY_ERROR
                            else:
                                CURRENT_ERROR_MESSAGE = ALLOWANCE_ERROR

        # dev cards game states
        elif game_state == "dev cards":

            for butt in DEV_CARDS_BUTTONS_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        game_state = "default"
                    if KNIGHT_BUTTON.check_for_input(mos_pos):
                        game_state = "knight"
                    if VICTORY_POINT_BUTTON.check_for_input(mos_pos):
                        game_state = "victory"
                    if ROAD_BUILDING_BUTTON.check_for_input(mos_pos):
                        game_state = "road"
                    if MONOPOLY_BUTTON.check_for_input(mos_pos):
                        game_state = "monopoly"
                    if YEAR_OF_PLENTY_BUTTON.check_for_input(mos_pos):
                        game_state = "year"
        # dev knight
        elif game_state == "knight":
            if current_player.get_dev_card_total_by_type("knight"):
                for butt in [USE_BUTTON, BACK_DEV_TRADE_BUTTON]:
                    butt.change_color(mos_pos)
                    butt.update(SCREEN)
            else:
                BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
                BACK_DEV_TRADE_BUTTON.update(SCREEN)
                SCREEN.blit(GREY_USE_DEV, GREY_USE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "dev cards"
                    if USE_BUTTON.check_for_input(mos_pos) and current_player.get_dev_card_total_by_type("knight") > 0:
                        current_player.remove_development_card("knight")
                        current_player.add_knight()
                        new_game.update_largest_army_player()
                        game_state = "robber"
        # dev victory
        elif game_state == "victory":

            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)
            SCREEN.blit(GREY_USE_DEV, GREY_USE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "dev cards"
        # dev road
        elif game_state == "road":
            if current_player.get_dev_card_total_by_type("road"):
                for butt in [USE_BUTTON, BACK_DEV_TRADE_BUTTON]:
                    butt.change_color(mos_pos)
                    butt.update(SCREEN)
            else:
                BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
                BACK_DEV_TRADE_BUTTON.update(SCREEN)
                SCREEN.blit(GREY_USE_DEV, GREY_USE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "dev cards"
                    if USE_BUTTON.check_for_input(mos_pos) and current_player.get_dev_card_total_by_type("road") > 0:
                        current_player.remove_development_card("road")
                        game_state = "road effect"
        # handles placing of 2 roads after road building card is used.
        elif game_state == "road effect":
            if not current_player.road_allowance():
                print("Player out of roads (15)")
                game_state = "default"


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    # Check if the click is within the clickable area for any of the lines

                    for pos in new_game.road_positions:
                        start_point = pos[0]
                        end_point = pos[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 20

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2 \
                                and current_player.is_valid_road_placement(pos):
                            # Add the road to the player's list of roads
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            current_player.add_road(pos)
                            new_game.update_longest_road_player()
                            new_game.road_positions.remove(pos)
                            road_counter += 1
                            if road_counter == 2:
                                road_counter = 0
                                game_state = "default"
        # dev monopoly
        elif game_state == "monopoly":
            if current_player.get_dev_card_total_by_type("monopoly"):
                for butt in [USE_BUTTON, BACK_DEV_TRADE_BUTTON]:
                    butt.change_color(mos_pos)
                    butt.update(SCREEN)
            else:
                BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
                BACK_DEV_TRADE_BUTTON.update(SCREEN)
                SCREEN.blit(GREY_USE_DEV, GREY_USE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "dev cards"
                    if USE_BUTTON.check_for_input(mos_pos) and current_player.get_dev_card_total_by_type(
                            "monopoly") > 0:
                        current_player.remove_development_card("monopoly")
                        game_state = "monopoly effect"
        # monopoly effect
        elif game_state == "monopoly effect":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        for p in new_game.get_players():
                            if p is not current_player and p.get_resources()["forest"] > 0:
                                p.remove_resource("forest")
                                current_player.add_resource("forest")
                        game_state = "default"
                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        for p in new_game.get_players():
                            if p is not current_player and p.get_resources()["pasture"] > 0:
                                p.remove_resource("pasture")
                                current_player.add_resource("pasture")
                        game_state = "default"
                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        for p in new_game.get_players():
                            if p is not current_player and p.get_resources()["fields"] > 0:
                                p.remove_resource("fields")
                                current_player.add_resource("fields")
                        game_state = "default"
                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        for p in new_game.get_players():
                            if p is not current_player and p.get_resources()["mountains"] > 0:
                                p.remove_resource("mountains")
                                current_player.add_resource("mountains")
                        game_state = "default"
                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        for p in new_game.get_players():
                            if p is not current_player and p.get_resources()["hills"] > 0:
                                p.remove_resource("hills")
                                current_player.add_resource("hills")
                        game_state = "default"
        # dev year
        elif game_state == "year":
            if current_player.get_dev_card_total_by_type("year"):
                for butt in [USE_BUTTON, BACK_DEV_TRADE_BUTTON]:
                    butt.change_color(mos_pos)
                    butt.update(SCREEN)
            else:
                BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
                BACK_DEV_TRADE_BUTTON.update(SCREEN)
                SCREEN.blit(GREY_USE_DEV, GREY_USE_RECT)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "dev cards"
                    if USE_BUTTON.check_for_input(mos_pos) and current_player.get_dev_card_total_by_type("year") > 0:
                        current_player.remove_development_card("year")
                        game_state = "year effect"
        # year effect state
        elif game_state == "year effect":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                # handles state switching
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if new_game.bank.get_bank_resource("forest") > 0:
                            new_game.bank.remove_resources("forest")
                            current_player.add_resource("forest")
                            resource_counter += 1
                        if resource_counter == 2:
                            resource_counter = 0
                            game_state = "default"

                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if new_game.bank.get_bank_resource("pasture") > 0:
                            new_game.bank.remove_resources("pasture")
                            current_player.add_resource("pasture")
                            resource_counter += 1
                        if resource_counter == 2:
                            resource_counter = 0
                            game_state = "default"
                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if new_game.bank.get_bank_resource("fields") > 0:
                            new_game.bank.remove_resources("fields")
                            current_player.add_resource("fields")
                            resource_counter += 1
                        if resource_counter == 2:
                            resource_counter = 0
                            game_state = "default"
                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if new_game.bank.get_bank_resource("mountains") > 0:
                            new_game.bank.remove_resources("mountains")
                            current_player.add_resource("mountains")
                            resource_counter += 1
                        if resource_counter == 2:
                            resource_counter = 0
                            game_state = "default"
                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if new_game.bank.get_bank_resource("hills") > 0:
                            new_game.bank.remove_resources("hills")
                            current_player.add_resource("hills")
                            resource_counter += 1
                        if resource_counter == 2:
                            resource_counter = 0
                            game_state = "default"

        elif game_state == "pause menu":
            if time_trial:
                timer.pause()
            for butt in [SAVE_BUTTON, RESUME_BUTTON, MAIN_MENU_BUTTON]:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if RESUME_BUTTON.check_for_input(mos_pos):
                        game_state = "default"
                        if time_trial:
                            timer.unpause()
                    if MAIN_MENU_BUTTON.check_for_input(mos_pos):
                        main_menu()
                    if SAVE_BUTTON.check_for_input(mos_pos):
                        if time_trial:
                            timer.save()
                        else:
                            if doesFileExists("timer_data.txt"):
                                os.remove("timer_data.txt")
                        players_data = new_game.generate_players_save_data()
                        board_data = new_game.board.generate_grid_save()
                        bank_data = new_game.bank.generate_bank_save()
                        game_data = new_game.generate_game_save()
                        with open('player_data.txt', 'w') as player_file:
                            json.dump(players_data, player_file)
                        with open('board_data.txt', 'w') as board_file:
                            json.dump(board_data, board_file)
                        with open('bank_data.txt', 'w') as bank_file:
                            json.dump(bank_data, bank_file)
                        with open('game_data.txt', 'w') as game_file:
                            json.dump(game_data, game_file)

        elif game_state == "help menu":
            if time_trial:
                timer.pause()
            BACK_BUTTON.change_color(mos_pos)
            BACK_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON.check_for_input(mos_pos):
                        if time_trial:
                            timer.unpause()
                        game_state = "default"

        # bank trading game states
        elif game_state == "bank sheep":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"

                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["forest"] >= current_player.get_trade_ratios()["forest"][0] \
                                and new_game.bank.get_bank_resource("pasture") >= 1:
                            current_player.add_resource("pasture")
                            current_player.remove_resource_with_amount("forest",
                                                                       current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.add_bank_resources_with_amount("forest",
                                                                         current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.remove_resources("pasture")

                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["fields"] >= current_player.get_trade_ratios()["fields"][0] \
                                and new_game.bank.get_bank_resource("pasture") >= 1:
                            current_player.add_resource("pasture")
                            current_player.remove_resource_with_amount("fields",
                                                                       current_player.get_trade_ratios()["fields"][0])
                            new_game.bank.add_bank_resources_with_amount("fields",
                                                                         current_player.get_trade_ratios()["fields"][0])
                            new_game.bank.remove_resources("pasture")

                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["mountains"] >= \
                                current_player.get_trade_ratios()["mountains"][0] \
                                and new_game.bank.get_bank_resource("pasture") >= 1:
                            current_player.add_resource("pasture")
                            current_player.remove_resource_with_amount("mountains",
                                                                       current_player.get_trade_ratios()["mountains"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("mountains",
                                                                         current_player.get_trade_ratios()["mountains"][
                                                                             0])
                            new_game.bank.remove_resources("pasture")

                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["hills"] >= current_player.get_trade_ratios()["hills"][0] \
                                and new_game.bank.get_bank_resource("pasture") >= 1:
                            current_player.add_resource("pasture")
                            current_player.remove_resource_with_amount("hills",
                                                                       current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.add_bank_resources_with_amount("hills",
                                                                         current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.remove_resources("pasture")
        elif game_state == "bank wood":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"

                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["pasture"] >= current_player.get_trade_ratios()["pasture"][0] \
                                and new_game.bank.get_bank_resource("forest") >= 1:
                            current_player.add_resource("forest")
                            current_player.remove_resource_with_amount("pasture",
                                                                       current_player.get_trade_ratios()["pasture"][0])
                            new_game.bank.add_bank_resources_with_amount("pasture",
                                                                         current_player.get_trade_ratios()["pasture"][
                                                                             0])
                            new_game.bank.remove_resources("forest")

                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["fields"] >= current_player.get_trade_ratios()["fields"][0] \
                                and new_game.bank.get_bank_resource("forest") >= 1:
                            current_player.add_resource("forest")
                            current_player.remove_resource_with_amount("fields",
                                                                       current_player.get_trade_ratios()["fields"][0])
                            new_game.bank.add_bank_resources_with_amount("fields",
                                                                         current_player.get_trade_ratios()["fields"][0])
                            new_game.bank.remove_resources("forest")

                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["mountains"] >= \
                                current_player.get_trade_ratios()["mountains"][0] \
                                and new_game.bank.get_bank_resource("forest") >= 1:
                            current_player.add_resource("forest")
                            current_player.remove_resource_with_amount("mountains",
                                                                       current_player.get_trade_ratios()["mountains"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("mountains",
                                                                         current_player.get_trade_ratios()["mountains"][
                                                                             0])
                            new_game.bank.remove_resources("forest")

                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["hills"] >= current_player.get_trade_ratios()["hills"][0] \
                                and new_game.bank.get_bank_resource("forest") >= 1:
                            current_player.add_resource("forest")
                            current_player.remove_resource_with_amount("hills",
                                                                       current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.add_bank_resources_with_amount("hills",
                                                                         current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.remove_resources("forest")
        elif game_state == "bank wheat":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"

                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["pasture"] >= current_player.get_trade_ratios()["pasture"][0] \
                                and new_game.bank.get_bank_resource("fields") >= 1:
                            current_player.add_resource("fields")
                            current_player.remove_resource_with_amount("pasture",
                                                                       current_player.get_trade_ratios()["pasture"][0])
                            new_game.bank.add_bank_resources_with_amount("pasture",
                                                                         current_player.get_trade_ratios()["pasture"][
                                                                             0])
                            new_game.bank.remove_resources("fields")

                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["forest"] >= current_player.get_trade_ratios()["forest"][0] \
                                and new_game.bank.get_bank_resource("fields") >= 1:
                            current_player.add_resource("fields")
                            current_player.remove_resource_with_amount("forest",
                                                                       current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.add_bank_resources_with_amount("forest",
                                                                         current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.remove_resources("fields")

                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["mountains"] >= \
                                current_player.get_trade_ratios()["mountains"][0] \
                                and new_game.bank.get_bank_resource("fields") >= 1:
                            current_player.add_resource("fields")
                            current_player.remove_resource_with_amount("mountains",
                                                                       current_player.get_trade_ratios()["mountains"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("mountains",
                                                                         current_player.get_trade_ratios()["mountains"][
                                                                             0])
                            new_game.bank.remove_resources("fields")

                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["hills"] >= current_player.get_trade_ratios()["hills"][0] \
                                and new_game.bank.get_bank_resource("fields") >= 1:
                            current_player.add_resource("fields")
                            current_player.remove_resource_with_amount("hills",
                                                                       current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.add_bank_resources_with_amount("hills",
                                                                         current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.remove_resources("fields")
        elif game_state == "bank ore":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"

                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["pasture"] >= current_player.get_trade_ratios()["pasture"][0] \
                                and new_game.bank.get_bank_resource("mountains") >= 1:
                            current_player.add_resource("mountains")
                            current_player.remove_resource_with_amount("pasture",
                                                                       current_player.get_trade_ratios()["pasture"][0])
                            new_game.bank.add_bank_resources_with_amount("pasture",
                                                                         current_player.get_trade_ratios()["pasture"][
                                                                             0])
                            new_game.bank.remove_resources("mountains")

                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["forest"] >= current_player.get_trade_ratios()["forest"][0] \
                                and new_game.bank.get_bank_resource("mountains") >= 1:
                            current_player.add_resource("mountains")
                            current_player.remove_resource_with_amount("forest",
                                                                       current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.add_bank_resources_with_amount("forest",
                                                                         current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.remove_resources("mountains")

                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["fields"] >= \
                                current_player.get_trade_ratios()["fields"][0] \
                                and new_game.bank.get_bank_resource("mountains") >= 1:
                            current_player.add_resource("mountains")
                            current_player.remove_resource_with_amount("fields",
                                                                       current_player.get_trade_ratios()["fields"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("fields",
                                                                         current_player.get_trade_ratios()["fields"][
                                                                             0])
                            new_game.bank.remove_resources("mountains")

                    if BRICK_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["hills"] >= current_player.get_trade_ratios()["hills"][0] \
                                and new_game.bank.get_bank_resource("mountains") >= 1:
                            current_player.add_resource("mountains")
                            current_player.remove_resource_with_amount("hills",
                                                                       current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.add_bank_resources_with_amount("hills",
                                                                         current_player.get_trade_ratios()["hills"][0])
                            new_game.bank.remove_resources("mountains")
        elif game_state == "bank brick":
            for butt in MONOPOLY_EFFECT_BUTTON_LIST:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"

                    if SHEEP_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["pasture"] >= current_player.get_trade_ratios()["pasture"][0] \
                                and new_game.bank.get_bank_resource("hills") >= 1:
                            current_player.add_resource("hills")
                            current_player.remove_resource_with_amount("pasture",
                                                                       current_player.get_trade_ratios()["pasture"][0])
                            new_game.bank.add_bank_resources_with_amount("pasture",
                                                                         current_player.get_trade_ratios()["pasture"][
                                                                             0])
                            new_game.bank.remove_resources("hills")

                    if WOOD_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["forest"] >= current_player.get_trade_ratios()["forest"][0] \
                                and new_game.bank.get_bank_resource("hills") >= 1:
                            current_player.add_resource("hills")
                            current_player.remove_resource_with_amount("forest",
                                                                       current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.add_bank_resources_with_amount("forest",
                                                                         current_player.get_trade_ratios()["forest"][0])
                            new_game.bank.remove_resources("hills")

                    if WHEAT_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["fields"] >= \
                                current_player.get_trade_ratios()["fields"][0] \
                                and new_game.bank.get_bank_resource("hills") >= 1:
                            current_player.add_resource("hills")
                            current_player.remove_resource_with_amount("fields",
                                                                       current_player.get_trade_ratios()["fields"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("fields",
                                                                         current_player.get_trade_ratios()["fields"][
                                                                             0])
                            new_game.bank.remove_resources("hills")

                    if ORE_BUTTON_MONOPOLY.check_for_input(mos_pos):
                        if current_player.get_resources()["mountains"] >= \
                                current_player.get_trade_ratios()["mountains"][0] \
                                and new_game.bank.get_bank_resource("hills") >= 1:
                            current_player.add_resource("hills")
                            current_player.remove_resource_with_amount("mountains",
                                                                       current_player.get_trade_ratios()["mountains"][
                                                                           0])
                            new_game.bank.add_bank_resources_with_amount("mountains",
                                                                         current_player.get_trade_ratios()["mountains"][
                                                                             0])
                            new_game.bank.remove_resources("hills")
        elif game_state == "bank dev":
            BACK_BUTTON_BUY_DEV.change_color(mos_pos)
            BACK_BUTTON_BUY_DEV.update(SCREEN)
            BUY_BUTTON_BUY_DEV.change_color(mos_pos)
            BUY_BUTTON_BUY_DEV.update(SCREEN)
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_BUY_DEV.check_for_input(mos_pos):
                        game_state = "default"
                    if BUY_BUTTON_BUY_DEV.check_for_input(mos_pos) and current_player.has_enough_resources("dev card") \
                            and len(new_game.bank.dev_cards) > 0:
                        card = new_game.bank.remove_dev_card()
                        new_game.bank.add_bank_resources_from_placement("dev card")
                        current_player.remove_resources_for_placement("dev card")
                        current_player.add_development_card(card)
                        if card == "victory":
                            current_player.add_victory_point()

        # player trading game states
        elif game_state == "pick player for trade":
            button_list = new_game.make_buttons_for_player_trading(current_player)
            for butt in button_list:
                butt.change_color(mos_pos)
                butt.update(SCREEN)
            BACK_DEV_TRADE_BUTTON.change_color(mos_pos)
            BACK_DEV_TRADE_BUTTON.update(SCREEN)

            new_game.update_trade_player_list(current_player)
            player_list = new_game.trade_player_list

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_DEV_TRADE_BUTTON.check_for_input(mos_pos):
                        game_state = "default"
                    if button_list[0].check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to trade with", player_list[0].get_name())
                        game_state = "trade player 1"
                    if len(button_list) > 1 and button_list[1].check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to trade with", player_list[1].get_name())
                        game_state = "trade player 2"
                    if len(button_list) > 2 and button_list[2].check_for_input(mos_pos):
                        print(current_player.get_name(), "wants to trade with", player_list[2].get_name())
                        game_state = "trade player 3"
        elif game_state == "trade player 1":
            trade_player = new_game.trade_player_list[0]
            for butt in TRADE_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_TRADE.check_for_input(mos_pos):
                        new_game.give_pool_resources_to_players(current_player, trade_player)
                        new_game.reset_trade_pools()
                        game_state = "pick player for trade"
                    elif TRADE_BUTTON.check_for_input(mos_pos):
                        if "AI" in trade_player.get_name():
                            if trade_player.player_trade_50_50:
                                new_game.swap_trade_pools()
                                new_game.give_pool_resources_to_players(current_player, trade_player)
                                new_game.reset_trade_pools()
                                game_state = "default"
                            else:
                                new_game.give_pool_resources_to_players(current_player, trade_player)
                                new_game.reset_trade_pools()
                                game_state = "default"
                        else:
                            new_game.swap_trade_pools()
                            new_game.give_pool_resources_to_players(current_player, trade_player)
                            new_game.reset_trade_pools()
                            game_state = "default"

                    # current player
                    if LEFT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["forest"] > 0:
                            new_game.add_resource_x_trader("forest")
                            current_player.remove_resource("forest")
                    elif LEFT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["pasture"] > 0:
                            new_game.add_resource_x_trader("pasture")
                            current_player.remove_resource("pasture")
                    elif LEFT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["fields"] > 0:
                            new_game.add_resource_x_trader("fields")
                            current_player.remove_resource("fields")
                    elif LEFT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["mountains"] > 0:
                            new_game.add_resource_x_trader("mountains")
                            current_player.remove_resource("mountains")
                    elif LEFT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["hills"] > 0:
                            new_game.add_resource_x_trader("hills")
                            current_player.remove_resource("hills")
                    # trade player
                    elif RIGHT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["forest"] > 0:
                            new_game.add_resource_y_trader("forest")
                            trade_player.remove_resource("forest")
                    elif RIGHT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["pasture"] > 0:
                            new_game.add_resource_y_trader("pasture")
                            trade_player.remove_resource("pasture")
                    elif RIGHT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["fields"] > 0:
                            new_game.add_resource_y_trader("fields")
                            trade_player.remove_resource("fields")
                    elif RIGHT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["mountains"] > 0:
                            new_game.add_resource_y_trader("mountains")
                            trade_player.remove_resource("mountains")
                    elif RIGHT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["hills"] > 0:
                            new_game.add_resource_y_trader("hills")
                            trade_player.remove_resource("hills")

                    elif LEFT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["forest"] > 0:
                            current_player.add_resource("forest")
                            new_game.remove_resource_x_trader("forest")
                    elif LEFT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["pasture"] > 0:
                            current_player.add_resource("pasture")
                            new_game.remove_resource_x_trader("pasture")
                    elif LEFT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["fields"] > 0:
                            current_player.add_resource("fields")
                            new_game.remove_resource_x_trader("fields")
                    elif LEFT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["mountains"] > 0:
                            current_player.add_resource("mountains")
                            new_game.remove_resource_x_trader("mountains")
                    elif LEFT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["hills"] > 0:
                            current_player.add_resource("hills")
                            new_game.remove_resource_x_trader("hills")

                    elif RIGHT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["forest"] > 0:
                            trade_player.add_resource("forest")
                            new_game.remove_resource_y_trader("forest")
                    elif RIGHT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["pasture"] > 0:
                            trade_player.add_resource("pasture")
                            new_game.remove_resource_y_trader("pasture")
                    elif RIGHT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["fields"] > 0:
                            trade_player.add_resource("fields")
                            new_game.remove_resource_y_trader("fields")
                    elif RIGHT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["mountains"] > 0:
                            trade_player.add_resource("mountains")
                            new_game.remove_resource_y_trader("mountains")
                    elif RIGHT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["hills"] > 0:
                            trade_player.add_resource("hills")
                            new_game.remove_resource_y_trader("hills")
        elif game_state == "trade player 2":
            trade_player = new_game.trade_player_list[1]
            for butt in TRADE_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_TRADE.check_for_input(mos_pos):
                        new_game.give_pool_resources_to_players(current_player, trade_player)
                        new_game.reset_trade_pools()
                        game_state = "pick player for trade"
                    elif TRADE_BUTTON.check_for_input(mos_pos):
                        new_game.swap_trade_pools()
                        new_game.give_pool_resources_to_players(current_player, trade_player)
                        new_game.reset_trade_pools()
                        game_state = "default"
                    # current player
                    if LEFT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["forest"] > 0:
                            new_game.add_resource_x_trader("forest")
                            current_player.remove_resource("forest")
                    elif LEFT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["pasture"] > 0:
                            new_game.add_resource_x_trader("pasture")
                            current_player.remove_resource("pasture")
                    elif LEFT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["fields"] > 0:
                            new_game.add_resource_x_trader("fields")
                            current_player.remove_resource("fields")
                    elif LEFT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["mountains"] > 0:
                            new_game.add_resource_x_trader("mountains")
                            current_player.remove_resource("mountains")
                    elif LEFT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["hills"] > 0:
                            new_game.add_resource_x_trader("hills")
                            current_player.remove_resource("hills")
                    # trade player
                    elif RIGHT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["forest"] > 0:
                            new_game.add_resource_y_trader("forest")
                            trade_player.remove_resource("forest")
                    elif RIGHT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["pasture"] > 0:
                            new_game.add_resource_y_trader("pasture")
                            trade_player.remove_resource("pasture")
                    elif RIGHT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["fields"] > 0:
                            new_game.add_resource_y_trader("fields")
                            trade_player.remove_resource("fields")
                    elif RIGHT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["mountains"] > 0:
                            new_game.add_resource_y_trader("mountains")
                            trade_player.remove_resource("mountains")
                    elif RIGHT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["hills"] > 0:
                            new_game.add_resource_y_trader("hills")
                            trade_player.remove_resource("hills")

                    elif LEFT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["forest"] > 0:
                            current_player.add_resource("forest")
                            new_game.remove_resource_x_trader("forest")
                    elif LEFT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["pasture"] > 0:
                            current_player.add_resource("pasture")
                            new_game.remove_resource_x_trader("pasture")
                    elif LEFT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["fields"] > 0:
                            current_player.add_resource("fields")
                            new_game.remove_resource_x_trader("fields")
                    elif LEFT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["mountains"] > 0:
                            current_player.add_resource("mountains")
                            new_game.remove_resource_x_trader("mountains")
                    elif LEFT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["hills"] > 0:
                            current_player.add_resource("hills")
                            new_game.remove_resource_x_trader("hills")

                    elif RIGHT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["forest"] > 0:
                            trade_player.add_resource("forest")
                            new_game.remove_resource_y_trader("forest")
                    elif RIGHT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["pasture"] > 0:
                            trade_player.add_resource("pasture")
                            new_game.remove_resource_y_trader("pasture")
                    elif RIGHT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["fields"] > 0:
                            trade_player.add_resource("fields")
                            new_game.remove_resource_y_trader("fields")
                    elif RIGHT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["mountains"] > 0:
                            trade_player.add_resource("mountains")
                            new_game.remove_resource_y_trader("mountains")
                    elif RIGHT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["hills"] > 0:
                            trade_player.add_resource("hills")
                            new_game.remove_resource_y_trader("hills")
        elif game_state == "trade player 3":
            trade_player = new_game.trade_player_list[2]
            for butt in TRADE_BUTTONS:
                butt.change_color(mos_pos)
                butt.update(SCREEN)

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if BACK_BUTTON_TRADE.check_for_input(mos_pos):
                        new_game.give_pool_resources_to_players(current_player, trade_player)
                        new_game.reset_trade_pools()
                        game_state = "pick player for trade"
                    elif TRADE_BUTTON.check_for_input(mos_pos):
                        new_game.swap_trade_pools()
                        new_game.give_pool_resources_to_players(current_player, trade_player)
                        new_game.reset_trade_pools()
                        game_state = "default"
                    # current player
                    if LEFT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["forest"] > 0:
                            new_game.add_resource_x_trader("forest")
                            current_player.remove_resource("forest")
                    elif LEFT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["pasture"] > 0:
                            new_game.add_resource_x_trader("pasture")
                            current_player.remove_resource("pasture")
                    elif LEFT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["fields"] > 0:
                            new_game.add_resource_x_trader("fields")
                            current_player.remove_resource("fields")
                    elif LEFT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["mountains"] > 0:
                            new_game.add_resource_x_trader("mountains")
                            current_player.remove_resource("mountains")
                    elif LEFT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if current_player.resources["hills"] > 0:
                            new_game.add_resource_x_trader("hills")
                            current_player.remove_resource("hills")
                    # trade player
                    elif RIGHT_PLAYER_WOOD_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["forest"] > 0:
                            new_game.add_resource_y_trader("forest")
                            trade_player.remove_resource("forest")
                    elif RIGHT_PLAYER_SHEEP_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["pasture"] > 0:
                            new_game.add_resource_y_trader("pasture")
                            trade_player.remove_resource("pasture")
                    elif RIGHT_PLAYER_WHEAT_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["fields"] > 0:
                            new_game.add_resource_y_trader("fields")
                            trade_player.remove_resource("fields")
                    elif RIGHT_PLAYER_ORE_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["mountains"] > 0:
                            new_game.add_resource_y_trader("mountains")
                            trade_player.remove_resource("mountains")
                    elif RIGHT_PLAYER_BRICK_BUTTON.check_for_input(mos_pos):
                        if trade_player.resources["hills"] > 0:
                            new_game.add_resource_y_trader("hills")
                            trade_player.remove_resource("hills")

                    elif LEFT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["forest"] > 0:
                            current_player.add_resource("forest")
                            new_game.remove_resource_x_trader("forest")
                    elif LEFT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["pasture"] > 0:
                            current_player.add_resource("pasture")
                            new_game.remove_resource_x_trader("pasture")
                    elif LEFT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["fields"] > 0:
                            current_player.add_resource("fields")
                            new_game.remove_resource_x_trader("fields")
                    elif LEFT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["mountains"] > 0:
                            current_player.add_resource("mountains")
                            new_game.remove_resource_x_trader("mountains")
                    elif LEFT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_x_pool["hills"] > 0:
                            current_player.add_resource("hills")
                            new_game.remove_resource_x_trader("hills")

                    elif RIGHT_TRADE_WOOD_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["forest"] > 0:
                            trade_player.add_resource("forest")
                            new_game.remove_resource_y_trader("forest")
                    elif RIGHT_TRADE_SHEEP_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["pasture"] > 0:
                            trade_player.add_resource("pasture")
                            new_game.remove_resource_y_trader("pasture")
                    elif RIGHT_TRADE_WHEAT_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["fields"] > 0:
                            trade_player.add_resource("fields")
                            new_game.remove_resource_y_trader("fields")
                    elif RIGHT_TRADE_ORE_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["mountains"] > 0:
                            trade_player.add_resource("mountains")
                            new_game.remove_resource_y_trader("mountains")
                    elif RIGHT_TRADE_BRICK_BUTTON.check_for_input(mos_pos):
                        if new_game.trader_y_pool["hills"] > 0:
                            trade_player.add_resource("hills")
                            new_game.remove_resource_y_trader("hills")
        # victory screen game state
        elif game_state == "victory screen":
            SCREEN.fill(BEIGE)
            SCREEN.blit(VICTORY_UI, VICTORY_UI_RECT)
            SCREEN.blit(VICTORY_IMAGE, VICTORY_IMAGE_RECT)

            MAIN_MENU_VICTORY_BUTTON.change_color(mos_pos)
            MAIN_MENU_VICTORY_BUTTON.update(SCREEN)
            QUIT_VICTORY_BUTTON.change_color(mos_pos)
            QUIT_VICTORY_BUTTON.update(SCREEN)

            sorted_player_score = new_game.generate_sorted_player_score()
            y_pos = 462

            for name, score in sorted_player_score.items():
                for p in new_game.players:
                    if p.get_name() == name:
                        name_text = NUMBER_FONT.render("{}".format(name), True, p.color)
                        score_text = NUMBER_FONT.render("{}".format(score), True, p.color)
                        name_text_rect = name_text.get_rect(center=(687, y_pos))
                        score_text_rect = score_text.get_rect(center=(1213, y_pos))
                        SCREEN.blit(name_text, name_text_rect)
                        SCREEN.blit(score_text, score_text_rect)
                        y_pos += 100
            y_pos = 462

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if MAIN_MENU_VICTORY_BUTTON.check_for_input(mos_pos):
                        main_menu()
                    if QUIT_VICTORY_BUTTON.check_for_input(mos_pos):
                        pygame.quit()
                        sys.exit()

        # Update the screen
        pygame.display.update()


# run game
main_menu()
