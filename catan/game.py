import pygame
from catan import HOUSE_POSITIONS, MOUSE_BUFFER, board, player, COLOR_LIST, UI_BUTTONS, PLACE_HOUSE_BUTTON, \
    END_TURN_BUTTON, PLACE_ROAD_BUTTON, NUMBER_FONT, BLACK


class Game:
    def __init__(self, player_names):
        self.board = board.Board()  # create a new game board
        self.players = [player.Player(name, COLOR_LIST[player_names.index(name)]) for name in
                        player_names]  # create a new player list
        self.current_player_index = 0  # initialize the current player index
        self.game_over = False  # initialize the game over flag

    def update_state(self, screen):
        # update the game board
        for current_player in self.players:
            current_player.draw_roads(screen)


        self.check_game_over()  # check if the game is over

    def draw_house(self, screen):
        for current_player in self.players:
            current_player.draw_houses(screen)

    def get_players(self):
        return self.players

    def check_game_over(self):
        # check if any player has reached 10 victory points
        for current_player in self.players:
            if current_player.victory_points >= 10:
                self.game_over = True

    def get_current_player(self):
        return self.players[self.current_player_index]

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def draw_board(self, screen):
        self.board.draw_board(screen)

    def draw_players_resources(self, screen):
        for current_player in self.players:
            if current_player.get_name() == "P1":
                current_player.draw_player_name(screen, 832)
                current_player.draw_resources(screen, 832)
            elif current_player.get_name() == "P2":
                current_player.draw_player_name(screen, 902)
                current_player.draw_resources(screen, 902)
            elif current_player.get_name() == "P3":
                current_player.draw_player_name(screen, 972)
                current_player.draw_resources(screen, 972)
            elif current_player.get_name() == "P4":
                current_player.draw_player_name(screen, 1042)
                current_player.draw_resources(screen, 1042)