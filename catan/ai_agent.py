import pygame, random, math, time
from catan import HOUSE_POSITIONS, ROAD_POSITIONS, EVERY_HOUSE_IN_PLAY
from catan.player import Player


class AIAgent(Player):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.chosen_house = None

    def make_decision(self, game_state):
        if game_state == "initial house placements P2+":
            valid_house_pos = []
            for pos in HOUSE_POSITIONS:
                if self.isnt_too_close_to_other_player_houses(pos):
                    valid_house_pos.append(pos)

            self.chosen_house = random.choice(valid_house_pos)

            print(self.name, "placed a house at", self.chosen_house)
            self.add_house(self.chosen_house)
            EVERY_HOUSE_IN_PLAY.append(self.chosen_house)
            self.add_victory_point()
            # remove the pos from the list
            HOUSE_POSITIONS.remove(self.chosen_house)

        elif game_state == "initial road placements P2+":
            roads_next_to_house = []
            for road in ROAD_POSITIONS:
                if road[0] == self.chosen_house or road[1] == self.chosen_house:
                    roads_next_to_house.append(road)

            chosen_road = random.choice(roads_next_to_house)
            self.add_road(chosen_road)
            ROAD_POSITIONS.remove(chosen_road)

            print(self.name,
                  "placed a road from {} to {}".format(chosen_road[0], chosen_road[1]))





    def isnt_too_close_to_other_player_houses(self, pos):
        """

        :rtype: object
        """
        for house in EVERY_HOUSE_IN_PLAY:
            distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
            if distance < 130:
                return False
        return True
