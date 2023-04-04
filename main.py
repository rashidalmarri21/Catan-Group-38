import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, UI_BUTTONS, PLACE_HOUSE_BUTTON, HOUSE_POSITIONS, PLACE_HOUSE_BUTTONS, BACK_BUTTON
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


def check_house_positions(mouse_pos, house_positions, current_player):
    for pos in house_positions:
        if pos[0] - 20 <= mouse_pos[0] <= pos[0] + 20 and pos[1] - 20 <= mouse_pos[1] <= pos[1] + 20:
            print(current_player.get_name(), "placed a house at", pos)
            current_player.add_house(pos)


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
player_names = []
for i in range(NUM_PLAYERS):
    player_names.append("P{}".format(i + 1))


def play():
    run = True
    house_positions = HOUSE_POSITIONS.copy()
    new_game = Game(player_names)
    game_state = "ui"

    # Game loop
    while run:

        # draw board
        new_game.draw_board(SCREEN)
        # get mouse position
        mos_pos = pygame.mouse.get_pos()
        # assign current_player
        current_player = new_game.get_current_player()

        # this state is for initial placements.
        if game_state == "initial placements":
            pass

        if game_state == "ui":
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
                        print(current_player.get_name(), "wants to place a house")
                        game_state = "place house"

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
                        game_state = "ui"
                    if BACK_BUTTON.check_for_input(mos_pos):
                        print(current_player.get_name(), "went back")
                        game_state = "ui"

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
                            # remove the pos from the list
                            house_positions.remove(pos)
        # updates the board state
        new_game.update_state(SCREEN)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
main_menu()
