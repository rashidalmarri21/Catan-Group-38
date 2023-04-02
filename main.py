import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, MENU_BG, MENU_TITLE_TEXT, MENU_TITLE_RECT, PLAY_BUTTON, \
    OPTIONS_BUTTON, QUIT_BUTTON
from catan.board import Board

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


def play():
    run = True
    new_board = Board()

    # Game loop
    while run:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                break

        new_board.draw_board(SCREEN)

        # Update the screen
        pygame.display.update()

        # Limit the frame rate
        clock.tick(FPS)


def options():
    pass


# run game
main_menu()
