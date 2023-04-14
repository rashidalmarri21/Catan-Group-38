import pygame, random, math, time
from catan import HOUSE_POSITIONS, ROAD_POSITIONS, EVERY_HOUSE_IN_PLAY
from catan.player import Player


class AIAgent(Player):
    def __init__(self, name, color):
        super().__init__(name, color)
        self.chosen_house = None
        self.last_road_placed = None

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

        elif game_state == "default":
            if self.has_enough_resources("road"):
                return True
            else:
                return False

        elif game_state == "place road":
            if self.has_enough_resources("road"):
                possible_roads = []
                possible_roads_weighted_to_last_road = []
                for road in ROAD_POSITIONS:
                    if self.is_valid_road_placement(road):
                        possible_roads.append(road)
                        if self.last_road_placed is not None:
                            if road[0] == self.last_road_placed[0] or road[0] == self.last_road_placed[1]\
                                    or road[1] == self.last_road_placed[0] or road[1] == self.last_road_placed[1]:
                                possible_roads_weighted_to_last_road.append(road)
                if len(possible_roads) != 0 and len(possible_roads_weighted_to_last_road) == 0:
                    chosen_road = random.choice(possible_roads)
                    print(self.name,
                          "placed a road from {} to {}".format(chosen_road[0], chosen_road[1]))
                    self.add_road(chosen_road)
                    self.remove_resources_for_placement('road')
                    self.last_road_placed = chosen_road
                    ROAD_POSITIONS.remove(chosen_road)
                    return
                elif len(possible_roads) != 0 and len(possible_roads_weighted_to_last_road) != 0:
                    chosen_road_random = random.choice(possible_roads)
                    chosen_road_weighted = random.choice(possible_roads_weighted_to_last_road)
                    chosen_road = random.choice([chosen_road_random, chosen_road_weighted])

                    print(self.name,
                          "placed a road from {} to {}".format(chosen_road[0], chosen_road[1]))
                    self.add_road(chosen_road)
                    self.remove_resources_for_placement('road')
                    self.last_road_placed = chosen_road
                    ROAD_POSITIONS.remove(chosen_road)
                    return
                else:
                    print("Out of valid roads.")
                    return
        elif game_state == "place house":
            if self.has_enough_resources("house"):
                valid_positions = []
                for pos in HOUSE_POSITIONS:
                    if self.is_valid_house_placement(pos) and self.isnt_too_close_to_other_player_houses(pos):
                        valid_positions.append(pos)
                if len(valid_positions) != 0:
                    chosen_house = random.choice(valid_positions)

                    print(self.get_name(), "placed a house at", chosen_house)
                    self.add_house(chosen_house)
                    EVERY_HOUSE_IN_PLAY.append(chosen_house)
                    self.add_victory_point()
                    self.remove_resources_for_placement('house')
                else:
                    print("Out of valid houses")
            else:
                return


    def isnt_too_close_to_other_player_houses(self, pos):
        """

        :rtype: object
        """
        for house in EVERY_HOUSE_IN_PLAY:
            distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
            if distance < 130:
                return False
        return True
