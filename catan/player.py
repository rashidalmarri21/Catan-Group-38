import pygame, \
    random
import math
from catan.constants import HOUSE_POSITIONS, CYAN, VIC_POINT_THRESHOLD, BUFFER, ROAD_POSITIONS, NUMBER_FONT, BLACK, BANK_NUMBER_FONT,\
    PLAYER_NAME_FONT



class Player:
    """
    A class that represents a player in the game.

    Attributes:
    - name (str): The name of the player.
    - color (str): The color of the player.
    - victory_points (int): The number of victory points the player has.
    - resources (dict): A dictionary of the player's resources, with keys 'forest', 'hills', 'pasture', 'fields', and 'mountains'.
    - development_cards (list): A list of the player's development cards.
    - houses (list): A list of the player's houses.
    - cities (list): A list of the player's cities.
    - roads (list): A list of the player's roads.
    - knights_played (int): The number of knights the player has played.
    - dice_roll (list): The dice roll result in the current turn.
    - trade_ratios (dict): A dictionary of the player's trade ratios, with keys 'forest', 'hills', 'pasture', 'fields', and 'mountains'.
    - discard_pool (dict): A dictionary of the player's discarded resources, with keys 'forest', 'hills', 'pasture', 'fields', and 'mountains'.
    - discard_amount (int): The number of resources in the discard pool.
    """
    def __init__(self, name, color):
        """
        Initialize the player object.

        Parameters:
        - name (str): The name of the player.
        - color (str): The color of the player.
        """
        self.name = name
        self.color = color

        self.victory_points = 0
        self.resources = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.development_cards = []
        self.houses = []
        self.cities = []
        self.roads = []
        self.knights_played = 0
        self.dice_roll = [1, 1]
        self.trade_ratios = {'forest': (4, 1), 'hills': (4, 1), 'pasture': (4, 1), 'fields': (4, 1), 'mountains': (4, 1)}
        self.discard_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.discard_amount = 0

    def get_name(self):
        """
       Get the name of the player.

       Returns:
       - str: The name of the player.
       """
        return self.name

    def get_color(self):
        """
       Get the color of the player.

       Returns:
       - str: The color of the player.
       """
        return self.color

    def add_knight(self):
        """
        Increment the number of knights played by the player.
        """
        self.knights_played += 1

    def get_knights_played(self):
        """
       Get the number of knights played by the player.

       Returns:
       - int: The number of knights played by the player.
       """
        return self.knights_played

    def get_trade_ratios(self):
        """
       Get the trade ratios of the player.

       Returns:
       - dict: A dictionary of the player's trade ratios, with keys 'forest', 'hills', 'pasture', 'fields', and 'mountains'.
       """
        return self.trade_ratios

    def update_trade_ratios(self, resource_type, ratio):
        """
        Update the trade ratio of a specific resource type.

        Parameters:
        - resource_type (str): The type of the resource to be updated.
        - ratio (tuple): The new trade ratio.
        """
        self.trade_ratios[resource_type] = ratio

    def update_all_trade_ratios(self, ratio):
        """
        Update all trade ratios of the player.

        Parameters:
        - ratio (tuple): The new trade ratio.
        """
        for key, value in self.trade_ratios.items():
            if value == (4, 1):
                self.trade_ratios[key] = ratio

    def house_allowance(self):
        """
        Check if the player can build a house.

        Returns:
        - bool: True if the player can build a house, False otherwise.
        """
        if len(self.houses) >= 5:
            return False
        else:
            return True

    def road_allowance(self):
        """
       Check if the player can build a road.

       Returns:
       - bool: True if the player can build a road, False otherwise.
       """
        if len(self.roads) >= 15:
            return False
        else:
            return True

    def city_allowance(self):
        """
       Check if the player can build a city.

       Returns:
       - bool: True if the player can build a city, False otherwise.
       """
        if len(self.cities) >= 4:
            return False
        else:
            return True


    def draw_trade_ratio_maritime(self, screen):
        """
        Draws the trade ratios for maritime trading on the screen.

        Args:
        - screen: the pygame screen object to draw on.
        """
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
        """
        Checks if the player has won the game.

        Returns:
        - True if the player has reached the victory point threshold, False otherwise.
        """
        if self.victory_points >= VIC_POINT_THRESHOLD:
            return True

    def add_resource(self, resource_type):
        """
        Adds one resource of the given type to the player's resource inventory.

        Args:
        - resource_type: the type of resource to add.
        """
        if resource_type == 'desert':
            return
        self.resources[resource_type] += 1

    def remove_resource(self, resource_type):
        """
        Removes one resource of the given type from the player's resource inventory.

        Args:
        - resource_type: the type of resource to remove.
        """
        if resource_type == 'desert':
            return
        self.resources[resource_type] -= 1

    def remove_resource_with_amount(self, resource_type, amount):
        """
        Removes a specified amount of the given resource type from the player's inventory.

        Args:
        - resource_type: the type of resource to remove.
        - amount: the amount of the resource to remove.
        """
        self.resources[resource_type] -= amount
    def remove_resources_for_placement(self, placement_type):
        """
        Removes the necessary resources from the player's inventory for the given type of placement.

        Args:
        - placement_type: the type of placement (road, house, city, dev card).
        """
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

    def remove_resource_from_discard_pool(self, resource_type):
        """
        Removes one resource of the given type from the player's discard pool.

        Args:
        - resource_type: the type of resource to remove.
        """
        self.discard_pool[resource_type] -= 1

    def add_resource_to_discard_pool(self, resource_type):
        """
        Adds one resource of the given type to the player's discard pool.

        Args:
        - resource_type: the type of resource to add.
        """
        self.discard_pool[resource_type] += 1

    def reset_discard_pool(self):
        """
        Resets the player's discard pool to zero for all resource types.
        """

        self.discard_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}


    def get_resources(self):
        """
        Returns a dictionary of the player's current resource inventory.

       Returns:
       - A dictionary with the keys as the resource types and the values as the number of resources for each type.
       """
        return self.resources

    def remove_development_card(self, card_type):
        """
        Removes a development card of a given type to the player's hand.

        Args:
        card_type (str): The type of the development card to add.

        """
        self.development_cards.remove(card_type)

    def add_development_card(self, card_type):
        """
        Adds a development card of a given type to the player's hand.

        Args:
        card_type (str): The type of the development card to add.

        """
        self.development_cards.append(card_type)

    def get_development_cards(self):
        """
        Returns a list of the player's development cards.

        """
        return self.development_cards

    def get_dev_card_total_by_type(self, card_type):
        """
        Returns the total number of development cards of a given type in the player's hand.

        Args:
        card_type (str): The type of development card to count.

        """
        return self.development_cards.count(card_type)

    def add_victory_point(self):
        """
        Increases the player's victory points by 1.

        """
        self.victory_points += 1

    def remove_victory_point(self):
        """
        Decreases the player's victory points by 1.

        """
        self.victory_points -= 1

    def get_victory_points(self):
        """
        Returns the number of victory points the player currently has.

        """
        return self.victory_points

    def add_house(self, position):
        """
        Adds a house to the player's collection of houses.

        Args:
        position (tuple): The coordinates of the house's position.

        """
        self.houses.append(position)

    def remove_house(self, position):
        """
        Removes a house from the player's collection of houses.

        Args:
        position (tuple): The coordinates of the house's position.

        """
        self.houses.remove(position)

    def get_house(self):
        """
        Returns a list of the player's houses.

        """
        return self.houses

    def add_city(self, position):
        """
        Adds a city to the player's collection of cities.

        Parameters:
        position (tuple): The coordinates of the city's position.

        """
        self.cities.append(position)

    def get_cities(self):
        """
        Returns a list of the player's cities.

        """
        return self.cities

    def sum_resource(self):
        """
        Sums the player's resources.

        Returns:
        int: The total number of resources the player has.

        """
        summed_resources = sum(self.resources.values())
        return summed_resources

    def update_discard_amount(self):
        """
        Updates the player's discard amount based on their current resources.

        """
        summed = self.sum_resource()
        self.discard_amount = summed // 2

    def remove_discard_amount(self):
        """
        Decreases the player's discard amount by 1.

        """
        self.discard_amount -= 1

    def add_discard_amount(self):
        """
        Increases the player's discard amount by 1.

        """
        self.discard_amount += 1

    def is_valid_house_placement(self, house_pos):
        """
        Determines if a given house placement is valid based on the player's existing roads.

        Parameters:
        house_pos (tuple): The coordinates of the house's position.

        Returns:
        bool: True if the placement is valid, False otherwise.

        """
        p_roads = self.get_roads()
        for start, end in p_roads:
            if start == house_pos or end == house_pos:
                return True

    def has_enough_resources(self, placement_type):
        """
        Determines if the player has enough resources to make a given type of placement.

        Parameters:
        placement_type (str): The type of placement to check for.

        Returns:
        bool: True if the player has enough resources, False otherwise.

        """
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
            if self.resources['fields'] >= 2 and self.resources['mountains'] >= 3:
                return True
            else:
                return False
        elif placement_type == "dev card":
            if self.resources['fields'] >= 1 and self.resources['mountains'] >= 1 and self.resources["pasture"] >= 1:
                return True
            else:
                return False

    def add_road(self, position):
        """
        Adds a road to the player's collection of roads.

        Parameters:
        position (tuple): The coordinates of the road's position.

        """
        self.roads.append(position)

    def get_roads(self):
        """
        Returns a list of the player's roads.

        """
        return self.roads

    def is_valid_road_placement(self, road_pos):
        """
        Determines if a given road placement is valid based on the player's existing roads.

        Args:
        road_pos (tuple): The coordinates of the road's position.

        Returns:
        bool: True if the placement is valid, False otherwise.

        """
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
        """
        Simulates dice roll and stores the resulting values in the instance variable dice_roll.
        """
        nums = [random.randint(1, 6), random.randint(1, 6)]
        self.dice_roll = nums

    def get_dice_number(self):
        """
        Returns the sum of the two dice rolled in the previous roll_dice() method call.
        """

        return sum(self.dice_roll)

    def get_dice_roll(self):
        """
        Returns the list of two integers representing the two dice rolled in the previous roll_dice() method call.
        """
        return self.dice_roll

    def draw_dice(self, screen):
        """
        Draw the two dice rolls onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        """

        dice_1 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[0]))
        dice_2 = pygame.image.load("assets/UI/dice/{}.png".format(self.dice_roll[1]))
        dice_1_rect = dice_1.get_rect(center=(508, 47))
        dice_2_rect = dice_2.get_rect(center=(593, 47))
        screen.blit(dice_1, dice_1_rect)
        screen.blit(dice_2, dice_2_rect)

    def draw_houses(self, screen, house_image):
        """
        Draw the player's houses onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        - house_image: the Pygame image object to use for each house.
        """
        if house_image is not None:
            for house in self.houses:
                house_rect = house_image.get_rect(center=house)
                screen.blit(house_image, house_rect)

    def draw_cities(self, screen, city_image):
        """
        Draw the player's cities onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        - city_image: the Pygame image object to use for each city.
        """

        for city in self.cities:
            city_rect = city_image.get_rect(center=city)
            screen.blit(city_image, city_rect)

    def draw_roads(self, screen):
        """
        Draw the player's roads onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        """
        for road in self.roads:
            pygame.draw.line(screen, self.color, road[0], road[1], 10)

    def draw_resources(self, screen, y_pos):
        """
        Draw the player's resource counts onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        - y_pos: the y-coordinate of the resource count display on the screen.
        """
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
        """
        Draw the player's selected resource count onto the screen in the maritime trade section.

        Args:
        - screen: the Pygame display surface object to draw on.
        - selected_resource: the selected resource to display the count for.
        """
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
        """
        Draw the player's name onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        - y_pos: the y-coordinate of the player name display on the screen.
        """
        player_name = PLAYER_NAME_FONT.render("{}".format(self.name), True, self.color)
        player_name_rect = player_name.get_rect(center=(1300, y_pos))
        screen.blit(player_name, player_name_rect)

    def draw_dev_card_numbers(self, screen):
        """
        Draw the player's development card counts onto the screen.

        Args:
        - screen: the Pygame display surface object to draw on.
        """
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
        """
        Draws the number of each type of development card that the player has in their possession
        in the bank trade screen.

        Args:
        - screen: pygame.Surface
            The surface on which to draw the development card counts.
        """
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

