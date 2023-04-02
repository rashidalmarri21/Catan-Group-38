import pygame
import math
from catan.constants import HOUSE_POSITIONS, CYAN, BLACK
from catan.board import Board


class Player:
    def __init__(self, color):
        self.color = color
        self.houses = {}
        self.roads = {}
        self.valid_house_positions = HOUSE_POSITIONS

    def place_house(self, position):
        self.houses[position] = True

    def place_road(self, position):
        self.roads[position] = True

    def draw(self, surface):
        house_color = self.color
        road_color = (128, 128, 128)

        for house in self.houses:
            pygame.draw.circle(surface, house_color, house, 10)

        for road in self.roads:
            pygame.draw.line(surface, road_color, road[0], road[1], 5)

    def is_valid_house_placement(self, new_position):
        if new_position in self.valid_house_positions and new_position not in self.houses:
            return True
        return False

    def draw_valid_house_positions(self, surface, mouse_position):
        for position in self.valid_house_positions:
            if self.is_valid_house_placement(position):
                if position[0] - 10 <= mouse_position[0] <= position[0] + 10 and position[1] - 10 <= mouse_position[
                    1] <= position[1] + 10:
                    color = CYAN
                else:
                    color = BLACK
                pygame.draw.circle(surface, color, position, 10, 2)
