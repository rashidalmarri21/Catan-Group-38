import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, MENU_BUTTON_LIST, \
    END_TURN_BUTTON, GAME_BUTTONS
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
NUM_PLAYERS = 2
player_names = []
for i in range(NUM_PLAYERS):
    player_names.append("P{}".format(i + 1))


def play():
    run = True
    new_game = Game(player_names)

    # Game loop
    while run:
        # draw board
        new_game.draw_board(SCREEN)
        # get mouse position
        mos_pos = pygame.mouse.get_pos()
        # assign current_player
        current_player = new_game.get_current_player()

        # loop through each button in the games UI
        for butt in GAME_BUTTONS:
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

        # Place Houses

        new_game.update_state(SCREEN)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
main_menu()
