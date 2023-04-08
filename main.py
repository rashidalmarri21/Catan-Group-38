import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, UI_BUTTONS, PLACE_HOUSE_BUTTON, HOUSE_POSITIONS, PLACE_HOUSE_BUTTONS, BACK_BUTTON, \
    PLACE_ROAD_BUTTONS, \
    PLACE_ROAD_BUTTON, ROAD_POSITIONS, ICON_32x, ROLL_DICE_BUTTON
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
player_names = ["Bob", "Dillon", "Mike", "Sara"]


def play():
    run = True
    house_positions = HOUSE_POSITIONS.copy()
    road_positions = ROAD_POSITIONS.copy()

    new_game = Game(player_names)
    game_state = "initial house placements P1"


    # Game loop
    while run:
        current_player = new_game.get_current_player()
        # draw board
        new_game.draw_board(SCREEN)
        new_game.draw_players_resources(SCREEN)
        new_game.ui_Messages(SCREEN, game_state, current_player)

        # get mouse position
        mos_pos = pygame.mouse.get_pos()
        # assign current_player

        # this state is for initial placements.
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
                            chosen_house_p1 = pos
                            game_state = "initial road placements P1"

        if game_state == "initial road placements P1":

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

        if game_state == "initial house placements P2+":
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
                            chosen_house_P2 = pos
                            game_state = "initial road placements P2+"

        if game_state == "initial road placements P2+":
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
                            if len(current_player.get_roads()) == 2 and current_player is not new_game.get_players()[3]:
                                new_game.end_turn()
                                game_state = "initial house placements P2+"
                            elif len(current_player.get_roads()) == 1:
                                game_state = "initial house placements P2+"
                            else:
                                new_game.end_turn()
                                game_state = "initial house placements P1"

        if game_state == "dice roll":
            ROLL_DICE_BUTTON.change_color(mos_pos)
            ROLL_DICE_BUTTON.update(SCREEN)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ROLL_DICE_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "rolled the dice")
                        current_player.roll_dice()
                        new_game.give_resources(current_player)
                        game_state = "default"

        if game_state == "default":
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
                            current_player.remove_resources_for_placement('house')
                            current_player.add_victory_point()
                            # remove the pos from the list
                            house_positions.remove(pos)
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
                        if (mos_pos[0] - center[0]) ** 2 + (mos_pos[1] - center[1]) ** 2 <= buffer_radius ** 2:
                            # Add the road to the player's list of roads
                            current_player.add_road(pos)
                            road_positions.remove(pos)
                            print(current_player.get_name(),
                                  "placed a road from {} to {}".format(start_point, end_point))

        # updates the board state
        new_game.update_state(SCREEN)
        new_game.draw_house(SCREEN)
        current_player.draw_dice(SCREEN)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
play()
