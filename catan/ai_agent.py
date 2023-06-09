import pygame, random, math, time
from catan import HOUSE_POSITIONS, ROAD_POSITIONS
from catan.player import Player

every_house_in_play = []


class AIAgent(Player):
    """
    Class representing an AI agent for playing a game.

    Args:
        name (str): Name of the AI agent.
        color (str): Color of the AI agent.

    Attributes:
        chosen_house (tuple): Coordinates of the house chosen by the AI agent.

    Inherits:
        Player: A parent class representing a player in the game.

    """
    def __init__(self, name, color):
        """
        Initialize the AI agent with a name, color, and set the chosen house to None.

        Args:
            name (str): Name of the AI agent.
            color (str): Color of the AI agent.

        """
        super().__init__(name, color)
        self.chosen_house = None

    def make_decision(self, game_state, road_positions, house_positions):
        """
        Make a decision based on the current game state.

        Args:
            game_state (str): Current game state, which determines the AI agent's decision-making logic.
            road_positions (list): List of road positions available for placement.
            house_positions (list): List of house positions available for placement.

        Returns:
            tuple: Tuple containing updated road positions and house positions after the AI agent's decision.

        """
        if game_state == "initial house placements P2+":
            valid_house_pos = []
            for pos in house_positions:
                if self.isnt_too_close_to_other_player_houses(pos):
                    valid_house_pos.append(pos)

            self.chosen_house = random.choice(valid_house_pos)

            print(self.name, "placed a house at", self.chosen_house)
            self.add_house(self.chosen_house)
            every_house_in_play.append(self.chosen_house)
            self.add_victory_point()
            # remove the pos from the list
            house_positions.remove(self.chosen_house)
            return road_positions, house_positions

        elif game_state == "initial road placements P2+":
            roads_next_to_house = []
            for road in road_positions:
                if road[0] == self.chosen_house or road[1] == self.chosen_house:
                    roads_next_to_house.append(road)

            chosen_road = random.choice(roads_next_to_house)
            self.add_road(chosen_road)
            road_positions.remove(chosen_road)

            print(self.name,
                  "placed a road from {} to {}".format(chosen_road[0], chosen_road[1]))
            return road_positions, house_positions

        elif game_state == "default":
            if self.has_enough_resources("road"):
                return True
            else:
                return False

        elif game_state == "place road":
            if self.has_enough_resources("road") and self.road_allowance():
                possible_roads = []
                for road in road_positions:
                    if self.is_valid_road_placement(road):
                        possible_roads.append(road)

                if len(possible_roads) != 0:
                    chosen_road = random.choice(possible_roads)
                    print(self.name,
                          "placed a road from {} to {}".format(chosen_road[0], chosen_road[1]))
                    self.add_road(chosen_road)
                    self.remove_resources_for_placement('road')
                    road_positions.remove(chosen_road)
                    return True, road_positions, house_positions
                else:
                    print("Out of valid roads.")
                    return False, road_positions, house_positions
            else:
                print("not enough resources or allowance limit")
                return False, road_positions, house_positions
        elif game_state == "place house":
            if self.has_enough_resources("house") and self.house_allowance():
                valid_positions = []
                for pos in house_positions:
                    if self.is_valid_house_placement(pos) and self.isnt_too_close_to_other_player_houses(pos):
                        valid_positions.append(pos)
                if len(valid_positions) != 0:
                    chosen_house = random.choice(valid_positions)

                    print(self.get_name(), "placed a house at", chosen_house)
                    self.add_house(chosen_house)
                    every_house_in_play.append(chosen_house)
                    self.add_victory_point()
                    self.remove_resources_for_placement('house')
                    house_positions.remove(chosen_house)
                    return True, road_positions, house_positions
                else:
                    print("Out of valid houses")
                    return False, road_positions, house_positions
            else:
                print("not enough resources or allowance limit")
                return False, road_positions, house_positions

    def trade_with_bank(self):
        """
        Trade with the bank for resources.

        Returns:
            tuple: Tuple containing lists of tradeable resources and needed resources.

        """

        tradeable_resources = []
        needed_resources = []
        for resource, value in self.resources.items():
            if value >= 5:
                tradeable_resources.append(resource)
            elif value <= 0 and resource != "mountains":
                needed_resources.append(resource)

        return tradeable_resources, needed_resources

    def make_list_of_resources_to_str(self):
        """
        Convert the AI agent's resources into a list of strings.

        Returns:
            list: List of resource strings.

        """
        string_list = []
        for key, value in self.resources.items():
            for i in range(value):
                string_list.append(key)
        return string_list

    def remove_resources_from_list(self, resource_list):
        """
        Remove resources from the AI agent's resources based on a given list of resources.

        Args:
            resource_list (list): List of resources to be removed.

        """
        for resource in resource_list:
            self.remove_resource(resource)

    def player_trade_50_50(self):
        """
        Perform a 50/50 trade with another player.

        Returns:
            bool: True if the trade is successful, False otherwise.

        """
        nums = [1, 2]
        x = random.choice(nums)
        if x == 1:
            return True
        else:
            return False

    def isnt_too_close_to_other_player_houses(self, pos):
        """
        Check if the given house position is not too close to other player's houses.

        Args:
            pos (tuple): Coordinates of the house position to be checked.

        Returns:
            bool: True if the house position is not too close to other player's houses, False otherwise.

        """
        for house in every_house_in_play:
            distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
            if distance < 130:
                return False
        return True
