import pygame
from catan import BLACK, BANK_NUMBER_FONT

class Bank:
    def __init__(self):
        self.bank_resources ={'forest': 19, 'hills': 19, 'pasture': 19, 'fields': 19, 'mountains': 19}
        self.dev_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

    def get_bank_resources(self):
        return self.bank_resources

    def get_bank_resource(self, resource_type):
        if resource_type == 'desert':
            return -1
        return self.bank_resources[resource_type]

    def get_dev_cards(self):
        return self.dev_cards

    def add_bank_resources(self, resource_type):
        self.bank_resources[resource_type] += 1

    def add_bank_resources_from_placement(self, placement_type):
        if placement_type == "road":
            self.bank_resources['forest'] += 1
            self.bank_resources['hills'] += 1
        elif placement_type == "house":
            self.bank_resources['forest'] += 1
            self.bank_resources['fields'] += 1
            self.bank_resources['pasture'] += 1
            self.bank_resources['hills'] += 1
        elif placement_type == "city":
            self.bank_resources['fields'] += 3
            self.bank_resources['mountains'] += 2

    def remove_resources(self, resource_type):
        if resource_type == 'desert':
            return
        self.bank_resources[resource_type] -= 1

    def draw_bank_resources(self, screen):
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



