import sys
import pygame
from catan import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, board, MENU_BG, button, MENU_BUTTON, FONT, \
    TITLE_FONT
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

        menu_text = TITLE_FONT.render("The SETTLERS of CATAN", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(960, 150))

        play_button = button.Button(image=MENU_BUTTON, pos=(960, 500), text_input="PLAY", font=FONT, base_color=BLACK,
                                    hovering_color=WHITE)
        options_button = button.Button(image=MENU_BUTTON, pos=(960, 650), text_input="OPTIONS", font=FONT,
                                       base_color=BLACK,
                                       hovering_color=WHITE)
        quit_button = button.Button(image=MENU_BUTTON, pos=(960, 800), text_input="QUIT", font=FONT, base_color=BLACK,
                                    hovering_color=WHITE)

        SCREEN.blit(menu_text, menu_rect)

        for butt in [play_button, options_button, quit_button]:
            butt.change_color(menu_mouse_pos)
            butt.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.check_for_input(menu_mouse_pos):
                    play()
                if options_button.check_for_input(menu_mouse_pos):
                    options()
                if quit_button.check_for_input(menu_mouse_pos):
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
