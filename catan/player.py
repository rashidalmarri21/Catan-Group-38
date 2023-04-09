import pygame, random
import math
from catan.constants import HOUSE_POSITIONS, CYAN, VIC_POINT_THRESHOLD, BUFFER, ROAD_POSITIONS, NUMBER_FONT, BLACK, BANK_NUMBER_FONT,\
    PLAYER_NAME_FONT



class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

        self.victory_points = 0
        self.resources = {'forest': 10, 'hills': 10, 'pasture': 10, 'fields': 10, 'mountains': 10}
        self.development_cards = []
        self.houses = []
        self.houses_rect = []
        self.roads = []
        self.robbers = 0
        self.dice_roll = [1, 1]
        self.trade_ratios = {'forest': (4, 1), 'hills': (4, 1), 'pasture': (4, 1), 'fields': (4, 1), 'mountains': (4, 1)}

    def get_name(self):
        return self.name

    def get_trade_ratios(self):
        return self.trade_ratios

    def update_trade_ratios(self, resource_type, ratio):
        self.trade_ratios[resource_type] = ratio

    def has_won(self):
        if self.victory_points >= VIC_POINT_THRESHOLD:
            return True

    def add_robber(self):
        self.robbers += 1

    def add_resource(self, resource_type):
        if resource_type == 'desert':
            return
        self.resources[resource_type] += 1

    def remove_resources_for_placement(self, placement_type):
        if placement_type == "road":
            self.resources['forest'] -= 1
            self.resources['hills'] -= 1
        elif placement_type == "house":
            self.resources['forest'] -= 1
            self.resources['fields'] -= 1
            self.resources['pasture'] -= 1
            self.resources['hills'] -= 1
        elif placement_type == "city":
            self.resources['fields'] -= 3
            self.resources['mountains'] -= 2

    def remove_resources_for_discard(self):
        pass  # this will allow the player to pick which resources to discard when a player rolls a 7 and
        pass  # the player has more than 7 cards

    def get_resources(self):
        return self.resources

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

    def is_valid_house_placement(self, house_pos):
        p_roads = self.get_roads()
        for start, end in p_roads:
            if start == house_pos or end == house_pos:
                return True

    def has_enough_resources(self, placement_type):
        if placement_type == "road":
            if self.resources['forest'] >= 1 and self.resources['hills'] >= 1:
                return True
            else:
                return False
        elif placement_type == "house":
            if self.resources['forest'] >= 1 and self.resources['fields'] >= 1 and self.resources['pasture'] >= 1 and \
                    self.resources['hills'] >= 1:
                return True
            else:
                return False
        elif placement_type == "city":
            if self.resources['fields'] >= 3 and self.resources['mountains'] >= 2:
                return True
            else:
                return False

    def add_road(self, position):
        self.roads.append(position)

    def get_roads(self):
        return self.roads

    def is_valid_road_placement(self, road_pos):
        buffer_distance = 73
        print(self.name, "wants to place a road at", road_pos)

        # Calculate center points of player's current roads
        road_center_points = []
        for start, end in self.roads:
            x = (start[0] + end[0]) / 2
            y = (start[1] + end[1]) / 2
            road_center_points.append((x, y))

        # Check if given road position is within buffer distance of any road center point
        for center_point in road_center_points:
            if math.sqrt((road_pos[0][0] - center_point[0]) ** 2 + (
                    road_pos[0][1] - center_point[1]) ** 2) <= buffer_distance or \
                    math.sqrt((road_pos[1][0] - center_point[0]) ** 2 + (
                            road_pos[1][1] - center_point[1]) ** 2) <= buffer_distance:
                print("True")
                return True

        print("False")
        return False

    def roll_dice(self):
        nums = [random.randint(1, 6), random.randint(1, 6)]
        self.dice_roll = nums

    def get_dice_number(self):
        return sum(self.dice_roll)

    def draw_dice(self, screen):
        dice_1 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[0]))
        dice_2 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[1]))
        dice_1_rect = dice_1.get_rect(center=(508, 47))
        dice_2_rect = dice_2.get_rect(center=(593, 47))
        screen.blit(dice_1, dice_1_rect)
        screen.blit(dice_2, dice_2_rect)

    def draw_houses(self, screen, house_image):
        for house in self.houses:
            house_rect = house_image.get_rect(center=house)
            screen.blit(house_image, house_rect)

    def draw_roads(self, screen):
        for road in self.roads:
            pygame.draw.line(screen, self.color, road[0], road[1], 10)

    def draw_resources(self, screen, y_pos):
        # draw wood number
        wood = BANK_NUMBER_FONT.render("{}".format(self.resources['forest']), True, BLACK)
        wood_rect = wood.get_rect(center=(1395, y_pos))
        screen.blit(wood, wood_rect)

        # draw sheep number
        sheep = BANK_NUMBER_FONT.render("{}".format(self.resources['pasture']), True, BLACK)
        sheep_rect = sheep.get_rect(center=(1455, y_pos))
        screen.blit(sheep, sheep_rect)

        # draw wheat number
        wheat = BANK_NUMBER_FONT.render("{}".format(self.resources['fields']), True, BLACK)
        wheat_rect = wheat.get_rect(center=(1515, y_pos))
        screen.blit(wheat, wheat_rect)

        # draw ore number
        ore = BANK_NUMBER_FONT.render("{}".format(self.resources['mountains']), True, BLACK)
        ore_rect = ore.get_rect(center=(1575, y_pos))
        screen.blit(ore, ore_rect)

        # draw brick number
        brick = BANK_NUMBER_FONT.render("{}".format(self.resources['hills']), True, BLACK)
        brick_rect = brick.get_rect(center=(1635, y_pos))
        screen.blit(brick, brick_rect)

        # draw dev_card number
        dev_card = BANK_NUMBER_FONT.render("{}".format(len(self.development_cards)), True, BLACK)
        dev_card_rect = dev_card.get_rect(center=(1695, y_pos))
        screen.blit(dev_card, dev_card_rect)

        # draw knight number
        knight = BANK_NUMBER_FONT.render("{}".format(self.robbers), True, BLACK)
        knight_rect = knight.get_rect(center=(1755, y_pos))
        screen.blit(knight, knight_rect)

        # draw road number
        road = BANK_NUMBER_FONT.render("{}".format(len(self.roads)), True, BLACK)
        road_rect = road.get_rect(center=(1815, y_pos))
        screen.blit(road, road_rect)

        # draw vic_points number
        vic_points = BANK_NUMBER_FONT.render("{}".format(self.victory_points), True, BLACK)
        vic_points_rect = vic_points.get_rect(center=(1875, y_pos))
        screen.blit(vic_points, vic_points_rect)

    def draw_player_name(self, screen, y_pos):
        player_name = PLAYER_NAME_FONT.render("{}".format(self.name), True, self.color)
        player_name_rect = player_name.get_rect(center=(1315, y_pos))
        screen.blit(player_name, player_name_rect)
