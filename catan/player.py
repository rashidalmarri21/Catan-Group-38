import pygame
import math
from catan.constants import HOUSE_POSITIONS, CYAN, VIC_POINT_THRESHOLD


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.victory_points = 0
        self.resources = {'wood': 0, 'brick': 0, 'sheep': 0, 'wheat': 0, 'ore': 0}
        self.development_cards = []
        self.houses = []
        self.roads = []
    def get_name(self):
        return self.name

    def has_won(self):
        if self.victory_points >= VIC_POINT_THRESHOLD:
            return True

    def add_resource(self, resource_type):
        self.resources[resource_type] += 1

    def remove_resources(self, resource_type):
        self.resources[resource_type] -= 1

    def get_resources(self):
        return self.resources

    def add_development_card(self, card):
        self.development_cards.append(card)

    def remove_development_card(self, card):
        self.development_cards.remove(card)

    def get_development_cards(self):
        return self.development_cards

    def add_victory_point(self):
        self.victory_points += 1

    def remove_victory_point(self):
        self.victory_points -= 1

    def get_victory_points(self):
        return self.victory_points

    def add_house(self, position):
        self.houses.append(position)

    def get_house(self):
        return self.houses
    def add_road(self, position):
        self.roads.append(position)

    def get_road(self):
        return self.roads
    def draw_houses(self, screen):
        for house in self.houses:
            pygame.draw.circle(screen, self.color, house, 20)
