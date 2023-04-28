import unittest
from catan.ai_agent import AIAgent
from catan.player import Player

class testAI(unittest.TestCase):

    """ 
        The AI player gets initialised using the same parameters as a regular player, including name
        and color; to determine weather the current player is an AI, the name of such player is checked
        for the word "AI".
    """

    """ The AI name MUST have the word "AI" inside. """
    testAIName = "AI name"
    testAIColor = "blue"
    testIsAI = False

    testAI = AIAgent(testAIName, testAIColor)

    def testAIInit(self):
        """ We can assume what would happen when checking weather the AI player is in use, primarily 
        found in the main class. """
        if "AI" in self.testAIName:
            testIsAI = True

        self.assertEqual(testIsAI, True)

        """ At this point, no chosen house should be selected. """
        self.assertEqual(self.testAI.chosen_house, None)


    """
        The make_decision() method takes 3 parameters, including game_state, road_positions and
        house_positions - the first being a string, the latter two being lists.
    """
    
    def testMakeDecisions(self):
        """ There are 5 game_state processed by the make_decision() method. """
        self.testAI.game_state = "initial house placements P2+"

        self.testAI.road_positions = [((821.4359353944899, 220.0), (751.4359353944899, 260.0))]
        self.testAI.house_positions = [(821.4359353944899, 220.0)]

        self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions)

        """ After calling the make_decision() method with the first game_state and placing a house at the given
        position, the Player class' get_house() method should return the chosen position. """
        self.assertEqual(self.testAI.get_house(), [(821.4359353944899, 220.0)])

        """ The second game_state, similar to the first, is with regard to road placement. """ 
        self.testAI.game_state = "initial road placements P2+"
        self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions)

        self.assertEqual(self.testAI.get_roads(), [((821.4359353944899, 220.0), (751.4359353944899, 260.0))])


        """ The third game_state, aka. "default", simply returns the output of if the player has enough resources
        to place a road. """
        """ After the initial road/house placement, we do not have enough resource to build a road. """
        self.testAI.game_state = "default"
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), False)

        """ If we add enough resources however, this should return true. """
        self.testAI.add_resource("forest"), self.testAI.add_resource("hills")
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), True)

        """ We already have enough resources for the next game_state (aka. "place road), but not enough valid positions. """
        self.testAI.game_state = "place road"
        valid_roads = (False, [], [])
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), valid_roads)

        """ Let's try adding more valid road positions. """
        self.testAI.road_positions = [((751.4359353944899, 260.0), (752.1539030917347, 340.0))]
        valid_roads = (True, [], [])
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), valid_roads)

        """ The last game_state is called "place house". """
        self.testAI.game_state = "place house"
        valid_houses = (False, [], [])
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), valid_houses)

        """ At this point, we don't actually have enough resource to build a house. """
        self.testAI.add_resource("fields"), self.testAI.add_resource("pasture"), self.testAI.add_resource("forest"), self.testAI.add_resource("hills")
        """ Despite having enough resources, we don't have any valid houses positions, and the decision will
        fail similar to before. """
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), valid_houses)


        """ The isnt_too_close_to_other_player_houses() method can be used to determine, in advance, weather
        the specified house position will be considered valid. """
        """ The position of the initial house placement would be considered "too close" and therfore return
        False. """
        self.assertEqual(self.testAI.isnt_too_close_to_other_player_houses((821.4359353944899, 220.0)), False)
        """ Let's try another position. """
        self.assertEqual(self.testAI.isnt_too_close_to_other_player_houses((752.1539030917347, 340.0)), True)
        """ Given this position is valid, we can use this position to place a new house. """
        self.testAI.house_positions = [(752.1539030917347, 340.0)]
        valid_houses = (True, [], [])
        self.assertEqual(self.testAI.make_decision(self.testAI.game_state, self.testAI.road_positions, self.testAI.house_positions), valid_houses)

    def testTradeWithBank(self):
        """ The trade_with_bank() determines tradeable_resources from any resource the player has with the
        amount 5 or larger. """
        """ needed_resources are determined by any resource with a value equal or less than 0, while not
        including the "mountains" resource. """
        """ Before we give the AI player any resources, the method would return the name of all resources
        excluding the mountains resource. """
        expected_return = ([], ['forest', 'hills', 'pasture', 'fields'])
        self.assertEqual(self.testAI.trade_with_bank(), expected_return) 

        """ This should mean, after adding 5 forest resources, the expected return should change to the 
        newly specified value. """
        """ The "forest" resources has gone from needed_resources, to tradeable_resources. """
        self.testAI.add_resource("forest"), self.testAI.add_resource("forest"), self.testAI.add_resource("forest"), self.testAI.add_resource("forest"), self.testAI.add_resource("forest") 

        expected_return = (['forest'], ['hills', 'pasture', 'fields'])

        self.assertEqual(self.testAI.trade_with_bank(), expected_return) 

        """ At this point, we have added the 'forest' resource 5 times, which should be the return from
        the make_list_of_resources_to_str() method. """
        expected_return = ['forest', 'forest', 'forest', 'forest', 'forest']
        self.assertEqual(self.testAI.make_list_of_resources_to_str(), expected_return)

        """ The remove_resources_from_lists() method takes a list of resources, and goes by each value
        inside the list, removing them from the player's resources. 
        Given the 5x forest resources, we will provide the method with a list of two forest resources
        which should leave the player with 3x forest resources. """
        expected_return = ['forest', 'forest', 'forest']
        remove_list = ['forest', 'forest']
        self.testAI.remove_resources_from_list(remove_list)
        self.assertEqual(self.testAI.make_list_of_resources_to_str(), expected_return)
