import unittest
from catan.game import Game

class testGameClass(unittest.TestCase):
    testPlayers = ["John Smith", "David Jones"]
    testColors = ["blue", "red"]

    game = Game(testPlayers, testColors)

    def testGameParam(self):
        """ We can compare the above initialised values with the name list that has been generated. """
        self.assertEqual(self.game.generate_player_name_list(), self.testPlayers)

        """ Going one-by-one through the list of players provided above, an equally indexed colour from the provided list is given. """
        self.assertEqual(self.game.players[0].get_color(), "blue")
        self.assertEqual(self.game.players[1].get_color(), "red")

    def testGameOver(self):
        """ At first, without any victory points, the game is not over. When we provide either player with the required victory
        points, the game will return being over. """
        self.assertEqual(self.game.check_game_over(self.game.players[0]), False)
        self.game.players[0].victory_points = 10
        self.assertEqual(self.game.check_game_over(self.game.players[0]), True)

        self.assertEqual(self.game.check_game_over(self.game.players[1]), False)
        self.game.players[1].victory_points = 10
        self.assertEqual(self.game.check_game_over(self.game.players[1]), True)
