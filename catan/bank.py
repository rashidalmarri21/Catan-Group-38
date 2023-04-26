import pygame, random
from catan import BLACK, BANK_NUMBER_FONT, DEV_CARDS

class Bank:
    """
       A class representing the game bank that manages the resources and development cards.

       Attributes:
           bank_resources (dict): A dictionary that stores the amount of each resource the bank has.
           dev_cards (list): A list of development cards the bank has.

       Methods:
           get_bank_resources(): Returns the bank resources dictionary.
           get_bank_resource(resource_type): Returns the amount of a specific resource type in the bank.
           get_dev_cards(): Returns the development cards list.
           remove_dev_card(): Removes and returns the first development card in the list.
           shuffled_dev_cards(card_list): Shuffles the input list of development cards and returns it.
           add_bank_resources(resource_type): Adds one unit of the specified resource type to the bank.
           add_bank_resources_with_amount(resource_type, amount): Adds the specified amount of the specified resource type to the bank.
           add_bank_resources_from_placement(placement_type): Adds the resources earned from a specific placement type to the bank.
           add_resources_from_list(resource_list): Adds the resources from the input list to the bank.
           remove_resources(resource_type): Removes one unit of the specified resource type from the bank.
           draw_bank_resources(screen): Draws the current amount of resources and development cards in the bank on the screen.
           generate_bank_save(): Returns a dictionary containing the bank's state for saving purposes.
       """
    def __init__(self):
        """
        Initializes the Bank instance with a dictionary of starting resources and a shuffled list of development cards.
        """
        self.bank_resources = {'forest': 19, 'hills': 19, 'pasture': 19, 'fields': 19, 'mountains': 19}
        self.dev_cards = self.shuffled_dev_cards(DEV_CARDS)

    def get_bank_resources(self):
        """
        Returns:
        dict: A copy of the bank_resources dictionary representing the current state of the bank.
        """
        return self.bank_resources

    def get_bank_resource(self, resource_type):
        """
        Args:
        resource_type (str): The type of resource to retrieve.

        Returns:
        int: The number of the specified resource type available in the bank, or -1 if the resource type is 'desert'.
        """
        if resource_type == 'desert':
            return -1
        return self.bank_resources[resource_type]

    def get_dev_cards(self):
        """
       Returns:
       list: A copy of the dev_cards list representing the current state of the development cards available in the bank.
       """
        return self.dev_cards

    def remove_dev_card(self):
        """
        Removes the topmost development card from the dev_cards list and returns it.

        Returns:
        str: The type of the removed development card.
        """
        card = self.dev_cards.pop(0)
        return card

    def shuffled_dev_cards(self, card_list):
        """
        Shuffles a list of development cards and returns the shuffled list.

        Args:
        card_list (list): A list of development cards.

        Returns:
        list: A shuffled list of development cards.
        """
        random.shuffle(card_list)
        return card_list

    def add_bank_resources(self, resource_type):
        """
        Increases the amount of a particular resource type in the bank by 1.

        Args:
            resource_type (str): The type of resource to add to the bank.
        """
        self.bank_resources[resource_type] += 1

    def add_bank_resources_with_amount(self, resource_type, amount):
        """
        Increases the amount of a particular resource type in the bank by a specified amount.

        Args:
            resource_type (str): The type of resource to add to the bank.
            amount (int): The amount to add to the bank.
        """
        self.bank_resources[resource_type] += amount

    def add_bank_resources_from_placement(self, placement_type):
        """
        Adds resources to the bank based on the type of game piece that was placed.

        Args:
            placement_type (str): The type of game piece that was placed (one of 'road', 'house', 'city', or 'dev card').
        """
        if placement_type == "road":
            self.bank_resources['forest'] += 1
            self.bank_resources['hills'] += 1
        elif placement_type == "house":
            self.bank_resources['forest'] += 1
            self.bank_resources['fields'] += 1
            self.bank_resources['pasture'] += 1
            self.bank_resources['hills'] += 1
        elif placement_type == "city":
            self.bank_resources['fields'] += 2
            self.bank_resources['mountains'] += 3
        elif placement_type == "dev card":
            self.bank_resources["pasture"] += 1
            self.bank_resources["fields"] += 1
            self.bank_resources["mountains"] += 1

    def add_resources_from_list(self, resource_list):
        """
        Adds a list of resource types to the bank.

        Args:
            resource_list (list): A list of resource types to add to the bank.
        """
        for resource in resource_list:
            self.add_bank_resources(resource)

    def remove_resources(self, resource_type):
        """
        Decreases the amount of a particular resource type in the bank by 1.

        Args:
            resource_type (str): The type of resource to remove from the bank.
        """
        if resource_type == 'desert':
            return
        self.bank_resources[resource_type] -= 1

    def draw_bank_resources(self, screen):
        """
        Draws the current resource counts in the bank onto the screen.

        Args:
            screen (pygame.Surface): The surface onto which the resource counts should be drawn.
        """
        y_pos = 73
        # draw wood number
        wood = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['forest']), True, BLACK)
        wood_rect = wood.get_rect(center=(124, y_pos))
        screen.blit(wood, wood_rect)

        # draw sheep number
        sheep = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['pasture']), True, BLACK)
        sheep_rect = sheep.get_rect(center=(186, y_pos))
        screen.blit(sheep, sheep_rect)

        # draw wheat number
        wheat = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['fields']), True, BLACK)
        wheat_rect = wheat.get_rect(center=(246, y_pos))
        screen.blit(wheat, wheat_rect)

        # draw ore number
        ore = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['mountains']), True, BLACK)
        ore_rect = ore.get_rect(center=(306, y_pos))
        screen.blit(ore, ore_rect)

        # draw brick number
        brick = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['hills']), True, BLACK)
        brick_rect = brick.get_rect(center=(366, y_pos))
        screen.blit(brick, brick_rect)

        # draw dev_card number
        dev_card = BANK_NUMBER_FONT.render("{}".format(len(self.dev_cards)), True, BLACK)
        dev_card_rect = dev_card.get_rect(center=(426, y_pos))
        screen.blit(dev_card, dev_card_rect)



    def generate_bank_save(self):
        """
        Generates a dictionary representing the current state of the bank,
        including the number of each type of resource and the remaining
        development cards.

        Returns:
            dict: A dictionary containing the number of each type of resource
            and the remaining development cards.
        """
        save_bank = {"dev cards": self.get_dev_cards()}
        for key, value in self.bank_resources.items():
            save_bank[key] = value
        return save_bank