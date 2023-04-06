
import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, UI_BUTTONS, PLACE_HOUSE_BUTTON, HOUSE_POSITIONS, PLACE_HOUSE_BUTTONS, BACK_BUTTON,PLACE_ROAD_BUTTONS, \
    PLACE_ROAD_BUTTON, ROAD_POSITIONS
from catan.game import Game

# Set up the screen

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
pygame.init()
pygame.font.init()

SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Settlers Of Catan")

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
NUM_PLAYERS = 4




def play():
    run = True
    house_positions = HOUSE_POSITIONS.copy()
    road_positions = ROAD_POSITIONS.copy()
    player_names = []
    for i in range(NUM_PLAYERS):
        player_names.append("P{}".format(i + 1))
    new_game = Game(player_names)
    game_state = "default"



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
        if game_state == "initial placements":
            pass
        """
        
        """
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
                        break
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
                        game_state = "default"
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        game_state = "default"

                    # checks if the mouse clicked on any of the house positions within a 20 pixel buffer
                    for pos in house_positions:
                        if pos[0] - 20 <= mos_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mos_pos[1] <= pos[1] + 20:
                            # if player has enough resources for house and house is valid_house_placement:
                            # need to implement 2 functions that:
                            # 1. check if the player has enough resources (player class)
                            # 2. makes sure the house is at least 2 intersections away any existing houses. (game class)
                            # 3. makes sure there is a road connected. (can also be in valid_house_placement) (game class)
                            print(current_player.get_name(), "placed a house at", pos)
                            current_player.add_house(pos)
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
                        game_state = 'default'
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
                            print(current_player.get_name(), "placed a road from {} to {}".format(start_point, end_point))

        # updates the board state
        new_game.update_state(SCREEN)
        new_game.draw_house(SCREEN)
        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
play()
