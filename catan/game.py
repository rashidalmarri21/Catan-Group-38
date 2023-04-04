import pygame
from catan import HOUSE_POSITIONS, MOUSE_BUFFER, board, player, COLOR_LIST


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
            current_player.draw_houses(screen)
        self.check_game_over()  # check if the game is over

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
