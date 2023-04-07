import pygame, random
import math
from catan.constants import HOUSE_POSITIONS, CYAN, VIC_POINT_THRESHOLD, BUFFER, ROAD_POSITIONS, NUMBER_FONT, BLACK


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.victory_points = 0
        self.resources = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.development_cards = []
        self.houses = []
        self.houses_rect = []
        self.roads = []
        self.robbers = 0
        self.dice_roll = [1, 1]

    def get_name(self):
        return self.name

    def has_won(self):
        if self.victory_points >= VIC_POINT_THRESHOLD:
            return True

    def add_robber(self):
        self.robbers += 1

    def add_resource(self, resource_type):
        if resource_type == 'desert':
            return
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

    def get_roads(self):
        return self.roads

    def roll_dice(self):
        nums = [random.randint(1, 6), random.randint(1, 6)]
        self.dice_roll = nums

    def get_dice_number(self):
        return sum(self.dice_roll)
    def draw_dice(self, screen):
        dice_1 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[0]))
        dice_2 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[1]))
        dice_1_rect = dice_1.get_rect(center=(90, 400))
        dice_2_rect = dice_2.get_rect(center=(160, 400))
        screen.blit(dice_1, dice_1_rect)
        screen.blit(dice_2, dice_2_rect)


    def draw_houses(self, screen):
        house_image = pygame.image.load("assets/UI/house/{}.png".format(self.name))
        for house in self.houses:
            house_rect = house_image.get_rect(center=house)
            screen.blit(house_image, house_rect)

    def draw_roads(self, screen):
        for road in self.roads:
            pygame.draw.line(screen, self.color, road[0], road[1], 10)

    def draw_resources(self, screen, y_pos):
        # draw wood number
        wood = NUMBER_FONT.render("{}".format(self.resources['forest']), True, BLACK)
        wood_rect = wood.get_rect(center=(1427, y_pos))
        screen.blit(wood, wood_rect)

        # draw sheep number
        sheep = NUMBER_FONT.render("{}".format(self.resources['pasture']), True, BLACK)
        sheep_rect = sheep.get_rect(center=(1484, y_pos))
        screen.blit(sheep, sheep_rect)

        # draw wheat number
        wheat = NUMBER_FONT.render("{}".format(self.resources['fields']), True, BLACK)
        wheat_rect = wheat.get_rect(center=(1546, y_pos))
        screen.blit(wheat, wheat_rect)

        # draw ore number
        ore = NUMBER_FONT.render("{}".format(self.resources['mountains']), True, BLACK)
        ore_rect = ore.get_rect(center=(1604, y_pos))
        screen.blit(ore, ore_rect)

        # draw brick number
        brick = NUMBER_FONT.render("{}".format(self.resources['hills']), True, BLACK)
        brick_rect = brick.get_rect(center=(1659, y_pos))
        screen.blit(brick, brick_rect)

        # draw dev_card number
        dev_card = NUMBER_FONT.render("{}".format(len(self.development_cards)), True, BLACK)
        dev_card_rect = dev_card.get_rect(center=(1717, y_pos))
        screen.blit(dev_card, dev_card_rect)

        # draw robber number
        robber = NUMBER_FONT.render("{}".format(self.robbers), True, BLACK)
        robber_rect = robber.get_rect(center=(1774, y_pos))
        screen.blit(robber, robber_rect)

        # draw road number
        road = NUMBER_FONT.render("{}".format(len(self.roads)), True, BLACK)
        road_rect = road.get_rect(center=(1832, y_pos))
        screen.blit(road, road_rect)

        # draw vic_points number
        vic_points = NUMBER_FONT.render("{}".format(self.victory_points), True, BLACK)
        vic_points_rect = vic_points.get_rect(center=(1889, y_pos))
        screen.blit(vic_points, vic_points_rect)

    def draw_player_name(self, screen, y_pos):
        player_name = NUMBER_FONT.render("{}".format(self.name), True, self.color)
        player_name_rect = player_name.get_rect(center=(1372, y_pos))
        screen.blit(player_name, player_name_rect)
