import random
import sys
import pygame, time
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, UI_BUTTONS, PLACE_HOUSE_BUTTON, HOUSE_POSITIONS, PLACE_HOUSE_BUTTONS, BACK_BUTTON, \
    PLACE_ROAD_BUTTONS, PLACE_ROAD_BUTTON, ROAD_POSITIONS, ICON_32x, ROLL_DICE_BUTTON, DEV_CARDS_BUTTON, \
    BACK_DEV_TRADE_BUTTON, \
    DEV_CARDS_BUTTONS_LIST, KNIGHT_BUTTON, ROAD_BUILDING_BUTTON, MONOPOLY_BUTTON, YEAR_OF_PLENTY_BUTTON, \
    VICTORY_POINT_BUTTON, \
    USE_BUTTON, GREY_USE_RECT, GREY_USE_DEV, MONOPOLY_EFFECT_BUTTON_LIST, SHEEP_BUTTON_MONOPOLY, WHEAT_BUTTON_MONOPOLY, \
    WOOD_BUTTON_MONOPOLY, ORE_BUTTON_MONOPOLY, BRICK_BUTTON_MONOPOLY, PLACE_CITY_BUTTON, SHEEP_BUTTON, WHEAT_BUTTON, \
    WOOD_BUTTON, ORE_BUTTON, BRICK_BUTTON, DEV_BUTTON, BUY_BUTTON_BUY_DEV, BACK_BUTTON_BUY_DEV, EVERY_HOUSE_IN_PLAY
from catan.game import Game
from catan.player import Player

# Set up the screen

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Settlers Of Catan")
pygame.display.set_icon(ICON_32x)
# Set up the clock
clock = pygame.time.Clock()
FPS = 60


def main_menu():
    pygame.display.set_caption("Menu")

    while True:
        SCREEN.blit(MENU_BG.convert(), (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()

        SCREEN.blit(MENU_TITLE_TEXT, MENU_TITLE_RECT)

        for butt in MENU_BUTTON_LIST:
            butt.change_color(menu_mouse_pos)
            butt.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if MENU_BUTTON_LIST[0].check_for_input(menu_mouse_pos):
                    play()
                if MENU_BUTTON_LIST[1].check_for_input(menu_mouse_pos):
                    options()
                if MENU_BUTTON_LIST[2].check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(FPS)


# THIS WILL GET EXTRACTED FROM THE MAIN MENU FUNCTION BUT FOR TESTING PURPOSES IT IS MANUALLY ENTERED HERE
NUM_PLAYERS = 2
player_names = ["Bob", "AIDillon", "AIMike", "AISara"]


def play():
    run = True
    # static road and house position lists.
    house_positions = HOUSE_POSITIONS.copy()
    road_positions = ROAD_POSITIONS.copy()

    # create players
    new_game = Game(player_names)

    # initialise game_state
    game_state = "initial house placements P1"

    # dev card helpers. Road Building and Year of Plenty
    road_counter = 0
    resource_counter = 0

    # Game loop
    while run:
        current_player = new_game.get_current_player()
        # draw everything
        new_game.draw_board(SCREEN)
        new_game.draw_players_resources(SCREEN)
        new_game.update_state(SCREEN)
        new_game.draw_house(SCREEN)
        new_game.draw_city(SCREEN)
        new_game.draw_robber(SCREEN)
        new_game.draw_flags(SCREEN)
        new_game.ui_Messages(SCREEN, game_state, current_player)

        # get mouse position
        mos_pos = pygame.mouse.get_pos()

        """
        
        GAME STATES:
        
        """

        # initial HOUSE placements for player 1
        if game_state == "initial house placements P1":
            chosen_house_p1 = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for pos in house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20 \
                                and new_game.isnt_to_close_to_other_houses(pos):
                            print(current_player.get_name(), "placed a house at", pos)
                            current_player.add_house(pos)
                            current_player.add_victory_point()
                            # remove the pos from the list
                            house_positions.remove(pos)
                            HOUSE_POSITIONS.remove(pos)
                            EVERY_HOUSE_IN_PLAY.append(pos)
                            chosen_house_p1 = pos
                            game_state = "initial road placements P1"
        # initial ROAD placements for player 1
        elif game_state == "initial road placements P1":

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    roads_next_to_house = []
                    for road in ROAD_POSITIONS:
                        if road[0] == chosen_house_p1 or road[1] == chosen_house_p1:
                            roads_next_to_house.append(road)

                    for pos_2 in roads_next_to_house:
                        start_point = pos_2[0]
                        end_point = pos_2[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 15

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            # Add the road to the player's list of roads
                            current_player.add_road(pos_2)
                            ROAD_POSITIONS.remove(pos_2)
                            road_positions.remove(pos_2)
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            if len(current_player.get_roads()) == 2:
                                game_state = "dice roll"
                            else:
                                new_game.end_turn()
                                game_state = "initial house placements P2+"
        # initial HOUSE placements for players 2+
        elif game_state == "initial house placements P2+":
            # AI agent control
            if "AI" in current_player.get_name():
                current_player.make_decision("initial house placements P2+")
                game_state = "initial road placements P2+"

            # user input control
            chosen_house_P2 = None
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    for pos in house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20 \
                                and new_game.isnt_to_close_to_other_houses(pos):
                            print(current_player.get_name(), "placed a house at", pos)
                            current_player.add_house(pos)
                            current_player.add_victory_point()
                            # remove the pos from the list
                            house_positions.remove(pos)
                            HOUSE_POSITIONS.remove(pos)
                            EVERY_HOUSE_IN_PLAY.append(pos)
                            chosen_house_P2 = pos
                            game_state = "initial road placements P2+"
        # initial ROAD placements for players 2+
        elif game_state == "initial road placements P2+":
            # AI agent control
            if "AI" in current_player.get_name():
                current_player.make_decision("initial road placements P2+")
                if len(current_player.get_roads()) == 2 and current_player is not new_game.get_players()[-1]:
                    time.sleep(1)
                    new_game.end_turn()
                    game_state = "initial house placements P2+"
                elif len(current_player.get_roads()) == 1:
                    time.sleep(1)
                    game_state = "initial house placements P2+"
                else:
                    time.sleep(1)
                    new_game.end_turn()
                    game_state = "initial house placements P1"

            # player input control
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    roads_next_to_house = []
                    for road in ROAD_POSITIONS:
                        if road[0] == chosen_house_P2 or road[1] == chosen_house_P2:
                            roads_next_to_house.append(road)

                    for pos_2 in roads_next_to_house:
                        start_point = pos_2[0]
                        end_point = pos_2[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 15

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            # Add the road to the player's list of roads
                            current_player.add_road(pos_2)
                            ROAD_POSITIONS.remove(pos_2)
                            road_positions.remove(pos_2)
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
                    game_state = "robber"
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
                            game_state = "robber"
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
                            new_game.update_robber_pos_list()
                            new_game.remove_robber_pos()
                            game_state = "default"

        # default game state
        elif game_state == "default":
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
                        new_game.end_turn()
                        game_state = 'dice roll'
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

        # implement place house state
        elif game_state == "place house":
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
                        new_game.end_turn()
                        game_state = 'dice roll'
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        game_state = "default"

                    # checks if the mouse clicked on any of the house positions within a 20 pixel buffer
                    for pos in house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20 \
                                and current_player.is_valid_house_placement(pos) \
                                and current_player.has_enough_resources("house") \
                                and new_game.isnt_to_close_to_other_houses(pos):
                            print(current_player.get_name(), "placed a house at", pos)
                            current_player.add_house(pos)
                            EVERY_HOUSE_IN_PLAY.append(pos)
                            current_player.add_victory_point()
                            current_player.remove_resources_for_placement('house')
                            new_game.bank.add_bank_resources_from_placement('house')

                            # remove the pos from the list
                            house_positions.remove(pos)
                        else:
                            print("False")
        # implement place road state
        elif game_state == "place road":
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
                        game_state = 'default'
                    if END_TURN_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "ended their turn")
                        new_game.end_turn()
                        game_state = 'dice roll'
                    # Check if the click is within the clickable area for any of the lines
                    for pos in road_positions:
                        start_point = pos[0]
                        end_point = pos[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 15

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2 \
                                and current_player.is_valid_road_placement(pos) \
                                and current_player.has_enough_resources('road'):
                            # Add the road to the player's list of roads
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            current_player.add_road(pos)
                            new_game.update_longest_road_player()
                            current_player.remove_resources_for_placement('road')
                            new_game.bank.add_bank_resources_from_placement('road')
                            road_positions.remove(pos)
                            ROAD_POSITIONS.remove(pos)
        # place city state
        elif game_state == "place city":
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
                        new_game.end_turn()
                        game_state = 'dice roll'
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        game_state = "default"

                    # checks if the mouse clicked on any of the house positions within a 20 pixel buffer
                    for pos in current_player.get_house():
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20 \
                                and current_player.is_valid_house_placement(pos) \
                                and current_player.has_enough_resources("city"):
                            print(current_player.get_name(), "placed a city at", pos)
                            current_player.add_city(pos)
                            current_player.remove_house(pos)
                            current_player.add_victory_point()
                            current_player.remove_resources_for_placement('city')
                            new_game.bank.add_bank_resources_from_placement('city')

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if the click is within the clickable area for any of the lines

                    for pos in road_positions:
                        start_point = pos[0]
                        end_point = pos[1]

                        # Calculate the center of the line
                        center = ((start_point[0] + end_point[0]) // 2, (start_point[1] + end_point[1]) // 2)

                        # Define the radius of the buffer zone
                        buffer_radius = 15

                        # Check if the mouse position is within the buffer zone
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2 \
                                and current_player.is_valid_road_placement(pos):
                            # Add the road to the player's list of roads
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))
                            current_player.add_road(pos)
                            new_game.update_longest_road_player()
                            road_positions.remove(pos)
                            ROAD_POSITIONS.remove(pos)
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

        # bank game states
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
                    if BUY_BUTTON_BUY_DEV.check_for_input(mos_pos) and current_player.has_enough_resources("dev card")\
                            and len(new_game.bank.dev_cards) > 0:
                        card = new_game.bank.remove_dev_card()
                        current_player.remove_resources_for_placement("dev card")
                        current_player.add_development_card(card)
                        if card == "victory":
                            current_player.add_victory_point()






        new_game.draw_player_bank_ratios(SCREEN, current_player)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
play()
