import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, CYAN, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, PLAY_BUTTON, \
    OPTIONS_BUTTON, QUIT_BUTTON, BUFFER, HOUSE_POSITIONS, MOUSE_BUFFER
from catan.board import Board
from catan.player import Player

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

        for butt in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            butt.change_color(menu_mouse_pos)
            butt.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.check_for_input(menu_mouse_pos):
                    play()
                if OPTIONS_BUTTON.check_for_input(menu_mouse_pos):
                    options()
                if QUIT_BUTTON.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()
        pygame.display.update()
        clock.tick(FPS)


players = 2


def play():
    run = True
    game_start = True
    new_board = Board()
    all_players = []

    # Loop through the number of players and create new players
    for player in range(players):
        player_name = "P{}".format(player + 1)
        player_color = BLACK if player % 2 == 0 else CYAN
        new_player = Player(player_name, player_color)
        all_players.append(new_player)

    # Game loop
    while run:
        new_board.draw_board(SCREEN)

        # Loop through all players and draw their houses on the board
        for player in all_players:
            player.draw_houses(SCREEN)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                mouse_pos = pygame.mouse.get_pos()

                if game_start:
                    for pos in HOUSE_POSITIONS:
                        if (pos[0] - MOUSE_BUFFER <= mouse_pos[0] <= pos[0] + MOUSE_BUFFER) and (
                                pos[1] - MOUSE_BUFFER <= mouse_pos[1] <= pos[1] + BUFFER):
                            # Get the current player and add a house to their list
                            current_player = all_players[0]
                            current_player.add_house(pos)
                            print("Clicked on board position:", pos)

                            # Remove the current player from the list and add them to the end
                            all_players.append(all_players.pop(0))

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
main_menu()
