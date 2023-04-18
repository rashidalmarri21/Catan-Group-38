import pygame, random, math, time
from catan import HOUSE_POSITIONS, ROAD_POSITIONS
from catan.player import Player

every_house_in_play = []
class AIAgent(Player):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.chosen_house = None


    def make_decision(self, game_state, road_positions, house_positions):
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
                    return road_positions, house_positions
                else:
                    print("Out of valid roads.")
                    return road_positions, house_positions
            else:
                return road_positions, house_positions
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
                    return road_positions, house_positions
                else:
                    print("Out of valid houses")
                    return road_positions, house_positions
            else:
                return road_positions, house_positions


    def isnt_too_close_to_other_player_houses(self, pos):
        """

        :rtype: object
        """
        for house in every_house_in_play:
            distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
            if distance < 130:
                return False
        return True
