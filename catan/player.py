import pygame, \
    random
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
        self.cities = []
        self.roads = []
        self.knights_played = 0
        self.dice_roll = [1, 1]
        self.trade_ratios = {'forest': (4, 1), 'hills': (4, 1), 'pasture': (4, 1), 'fields': (4, 1), 'mountains': (4, 1)}

    def get_name(self):
        return self.name

    def get_color(self):
        return self.color

    def add_knight(self):
        self.knights_played += 1

    def get_knights_played(self):
        return self.knights_played

    def get_trade_ratios(self):
        return self.trade_ratios

    def update_trade_ratios(self, resource_type, ratio):
        self.trade_ratios[resource_type] = ratio

    def update_all_trade_ratios(self, ratio):
        for key, value in self.trade_ratios.items():
            if value == (4, 1):
                self.trade_ratios[key] = (3, 1)

    def draw_trade_ratio_maritime(self, screen):
        y_pos = 650
        ratios = self.trade_ratios
        for resource_type, ratio in ratios.items():
            if resource_type == 'forest':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(742, y_pos))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'pasture':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(851, y_pos))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'fields':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(960, y_pos))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'mountains':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(1069, y_pos))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'hills':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(1178, y_pos))
                screen.blit(ratio_image, ratio_rect)

    def has_won(self):
        if self.victory_points >= VIC_POINT_THRESHOLD:
            return True

    def add_resource(self, resource_type):
        if resource_type == 'desert':
            return
        self.resources[resource_type] += 1

    def remove_resource(self, resource_type):
        if resource_type == 'desert':
            return
        self.resources[resource_type] -= 1

    def remove_resource_with_amount(self, resource_type, amount):
        self.resources[resource_type] -= amount
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
            self.resources['fields'] -= 2
            self.resources['mountains'] -= 3
        elif placement_type == "dev card":
            self.resources['fields'] -= 1
            self.resources['mountains'] -= 1
            self.resources['pasture'] -= 1

    def remove_resources_for_discard(self):
        pass  # this will allow the player to pick which resources to discard when a player rolls a 7 and
        pass  # the player has more than 7 cards

    def get_resources(self):
        return self.resources

    def remove_development_card(self, card_type):
        self.development_cards.remove(card_type)

    def add_development_card(self, card_type):
        self.development_cards.append(card_type)

    def get_development_cards(self):
        return self.development_cards

    def get_dev_card_total_by_type(self, card_type):
        return self.development_cards.count(card_type)

    def add_victory_point(self):
        self.victory_points += 1

    def remove_victory_point(self):
        self.victory_points -= 1

    def get_victory_points(self):
        return self.victory_points

    def add_house(self, position):
        self.houses.append(position)

    def remove_house(self, position):
        self.houses.remove(position)

    def get_house(self):
        return self.houses

    def add_city(self, position):
        self.cities.append(position)

    def get_cities(self):
        return self.cities

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
        elif placement_type == "dev card":
            if self.resources['fields'] >= 1 and self.resources['mountains'] >= 1 and self.resources["pasture"] >= 1:
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

    def get_dice_roll(self):
        return self.dice_roll

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

    def draw_cities(self, screen, city_image):
        for city in self.cities:
            city_rect = city_image.get_rect(center=city)
            screen.blit(city_image, city_rect)

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
        knight = BANK_NUMBER_FONT.render("{}".format(self.knights_played), True, BLACK)
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

    def draw_resource_in_maritime(self, screen, selected_resource):
        y_pos = 450
        if selected_resource == "wood":
            # draw wood number
            wood = NUMBER_FONT.render("{}".format(self.resources['forest']), True, BLACK)
            wood_rect = wood.get_rect(center=(1217, y_pos))
            screen.blit(wood, wood_rect)

        if selected_resource == "sheep":
            # draw sheep number
            sheep = NUMBER_FONT.render("{}".format(self.resources['pasture']), True, BLACK)
            sheep_rect = sheep.get_rect(center=(1217, y_pos))
            screen.blit(sheep, sheep_rect)

        if selected_resource == "wheat":
            # draw wheat number
            wheat = NUMBER_FONT.render("{}".format(self.resources['fields']), True, BLACK)
            wheat_rect = wheat.get_rect(center=(1217, y_pos))
            screen.blit(wheat, wheat_rect)

        if selected_resource == "ore":
            # draw ore number
            ore = NUMBER_FONT.render("{}".format(self.resources['mountains']), True, BLACK)
            ore_rect = ore.get_rect(center=(1217, y_pos))
            screen.blit(ore, ore_rect)
        if selected_resource == "brick":
            # draw brick number
            brick = NUMBER_FONT.render("{}".format(self.resources['hills']), True, BLACK)
            brick_rect = brick.get_rect(center=(1217, y_pos))
            screen.blit(brick, brick_rect)

    def draw_player_name(self, screen, y_pos):
        player_name = PLAYER_NAME_FONT.render("{}".format(self.name), True, self.color)
        player_name_rect = player_name.get_rect(center=(1315, y_pos))
        screen.blit(player_name, player_name_rect)

    def draw_dev_card_numbers(self, screen):
        knight = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('knight')), True, BLACK)
        knight_rect = knight.get_rect(center=(170, 707))
        screen.blit(knight, knight_rect)

        victory = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('victory')), True, BLACK)
        victory_rect = victory.get_rect(center=(355, 707))
        screen.blit(victory, victory_rect)

        road = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('road')), True, BLACK)
        road_rect = road.get_rect(center=(540, 707))
        screen.blit(road, road_rect)

        mono = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('monopoly')), True, BLACK)
        mono_rect = mono.get_rect(center=(170, 857))
        screen.blit(mono, mono_rect)

        year = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('year')), True, BLACK)
        year_rect = year.get_rect(center=(355, 857))
        screen.blit(year, year_rect)

        blank = NUMBER_FONT.render("{}x".format(len(self.development_cards)), True, BLACK)
        blank_rect = blank.get_rect(center=(540, 857))
        screen.blit(blank, blank_rect)

    def draw_dev_card_num_in_bank_trade(self, screen):
        knight = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('knight')), True, BLACK)
        knight_rect = knight.get_rect(center=(742, 600))
        screen.blit(knight, knight_rect)

        victory = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('victory')), True, BLACK)
        victory_rect = victory.get_rect(center=(851, 600))
        screen.blit(victory, victory_rect)

        road = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('road')), True, BLACK)
        road_rect = road.get_rect(center=(960, 600))
        screen.blit(road, road_rect)

        mono = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('monopoly')), True, BLACK)
        mono_rect = mono.get_rect(center=(1069, 600))
        screen.blit(mono, mono_rect)

        year = NUMBER_FONT.render("{}x".format(self.get_dev_card_total_by_type('year')), True, BLACK)
        year_rect = year.get_rect(center=(1178, 600))
        screen.blit(year, year_rect)

