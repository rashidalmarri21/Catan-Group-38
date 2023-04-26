import unittest
from catan.player import Player

"""
    The player class is given two parameters, including a name and a color; these parameters
    are used to initialise each active player inside the game, setting up important information
    including victory points, amount of resources, dice rolls, etc.
"""

class testPlayerClass(unittest.TestCase):

    """
        Initialize the player class with a provided name and color, these should be defined 
        as strings (they will fail otherwise).

        The first test will ensure the values provided by methods get_name() and get_color() 
        are strings, and that they equal the values provided.
    """

    testName = "John Smith"
    testColor = "blue"
    player = Player(testName, testColor)

    def testPlayerParam(self):
        self.assertIsInstance(self.player.get_name(), str)
        self.assertEqual(self.player.get_name(), self.player.name, self.testName)

        self.assertIsInstance(self.player.get_color(), str)
        self.assertEqual(self.player.get_color(), self.player.color, self.testColor)

    """
        The constant VIC_POINT_THRESHOLD defines the minimum value required to "win" the game.
        The value of the constant is 10, defined in file catan/constants.py.
    """

    def testPlayerHasWon(self):
        self.player.victory_points = 9;
        self.assertEqual(self.player.get_victory_points(), 9)
        self.player.add_victory_point()
        self.assertTrue(self.player.has_won())
        
        self.player.remove_victory_point()
        self.assertFalse(self.player.has_won())

    """
        The method add_knight() should increment the amount of knights_played, which can be
        returned using the appropriately named method get_knights_played().
    """

    def testKnights(self):
        self.player.add_knight()
        self.assertEqual(self.player.get_knights_played(), 1)

    """
        Trade ratios have values that will be provided during initialisation. There are various
        methods which involve trade ratios, including returning all trade ratios, updating a
        specific resource type's ratio, upgrading all default trade ratios, etc.
    """

    def testUpdatingTradeRatios(self):
        """ Check that the initialised values are correct before changing anything. """
        self.assertEqual(self.player.get_trade_ratios(), {'forest': (4, 1), 'hills': (4, 1), 'pasture': (4, 1), 'fields': (4, 1), 'mountains': (4, 1)})
       
        """ Attempt to update one trade ratio, and make sure the returned value is correct. """
        self.player.update_trade_ratios('forest', (5,2))
        self.assertEqual(self.player.get_trade_ratios(), {'forest': (5, 2), 'hills': (4, 1), 'pasture': (4, 1), 'fields': (4, 1), 'mountains': (4, 1)})

        """ Update all trade ratios, this should only change resources using the default 
        ratio (4, 1) to the value provided. """
        self.player.update_all_trade_ratios((10,5))
        self.assertEqual(self.player.get_trade_ratios(), {'forest': (5, 2), 'hills': (10, 5), 'pasture': (10, 5), 'fields': (10, 5), 'mountains': (10, 5)})


    """
        There are 3 important types of infrastructure (houses, roads and cities) with limiting 
        amounts of each that are possible (5, 15 and 4 respectively), each requires a certain
        combination and amount of resource. 
    """

    def testResources(self):
        """ The player is given 10 of each type of resource at the beginning. """
        self.assertEqual(self.player.get_resources(), {'forest': 10, 'hills': 10, 'pasture': 10, 'fields': 10, 'mountains': 10})


        """ At this point, we should have permission to create roads, houses and cities, with enough of each resource to build each type of infrastructure. """
        self.assertEqual(self.player.road_allowance(), True)
        self.assertEqual(self.player.has_enough_resources("road"), True)

        self.assertEqual(self.player.house_allowance(), True)
        self.assertEqual(self.player.has_enough_resources("house"), True)

        self.assertEqual(self.player.city_allowance(), True)
        self.assertEqual(self.player.has_enough_resources("city"), True)
       
        """ Remove an amount of resource that would dissallow building such infrastructure. """
        self.player.remove_resource_with_amount("mountains", 10)
        self.assertEqual(self.player.has_enough_resources("city"), False)

        """  If we leave at least 1 field resource (removing 9 from 10), we should still be able to create a house. """
        self.player.remove_resource_with_amount("fields", 9)
        self.assertEqual(self.player.has_enough_resources("house"), True)

        self.player.remove_resource_with_amount("pasture", 10)
        self.assertEqual(self.player.has_enough_resources("house"), False)

        self.player.remove_resource_with_amount("forest", 10)
        self.assertEqual(self.player.has_enough_resources("road"), False)

        """ We can simulate what would happen when placing a specific resource. """
        self.player.add_resource("forest")
        self.assertEqual(self.player.resources["forest"], 1)
        self.assertEqual(self.player.resources["hills"], 10)
        self.assertEqual(self.player.has_enough_resources("road"), True)

        """ We should go from having a single forest resource to zero, and having 10 hill resources to only 1. """
        self.player.remove_resources_for_placement("road")
        self.assertEqual(self.player.resources["forest"], 0)
        self.assertEqual(self.player.resources["hills"], 9)
        self.assertEqual(self.player.has_enough_resources("road"), False)

    """ 
        Add one of each development card type, check the full list of development cards and ensure 
        the reported amounts of each are valid.
    """

    def testDevCards(self):
        self.player.add_development_card("knight"), self.player.add_development_card("knight")
        self.player.add_development_card("victory")
        self.player.add_development_card("road")
        self.player.add_development_card("monopoly")
        self.player.add_development_card("year"), self.player.add_development_card("year"), self.player.add_development_card("year")
        self.assertEqual(self.player.get_development_cards(), ["knight", "knight", "victory", "road", "monopoly", "year", "year", "year"])
        self.assertEqual(self.player.get_dev_card_total_by_type("knight"), 2)
        self.assertEqual(self.player.get_dev_card_total_by_type("victory"), 1)
        self.assertEqual(self.player.get_dev_card_total_by_type("road"), 1)
        self.assertEqual(self.player.get_dev_card_total_by_type("monopoly"), 1)
        self.assertEqual(self.player.get_dev_card_total_by_type("year"), 3)

    def testDice(self):
        """ The unrolled die both have values of "1", and equal the total of "2" """
        self.assertEqual(self.player.get_dice_roll(), [1,1])

        """ We first manually apply an impossible value; the normal range of values provided by 
        get_dice_number() are between 2 and 12. """
        """ The default value is technically valid, so it would be possible to randomly achieve
        such roll. """
        self.player.dice_roll = [7,8]
        self.assertNotEqual(self.player.get_dice_roll(), [1,1])
        self.assertEqual(self.player.get_dice_number(), 15)

        """ If we roll the dice using the proper method, only values between 1 and 6 for each die are
        possible, this will never be able to equal the impossible value of 15, which had only been
        acheived through manually overriding the values. """
        self.player.roll_dice()
        self.assertNotEqual(self.player.get_dice_number(), 15)
