import pygame
from catan import BLACK, BANK_NUMBER_FONT

class Bank:
    def __init__(self):
        self.bank_resources ={'wood': 19, 'brick': 19, 'sheep': 19, 'wheat': 19, 'ore': 19}
        self.dev_cards = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]

    def get_bank_resources(self):
        return self.bank_resources

    def get_dev_cards(self):
        return self.dev_cards

    def add_bank_resources(self, resource_type):
        self.bank_resources[resource_type] += 1

    def return_if_monument(self, dev_card):
        if dev_card == "Monument":
            self.dev_cards.append(dev_card)

    def draw_bank_resources(self, screen):
        y_pos = 73
        # draw wood number
        wood = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['wood']), True, BLACK)
        wood_rect = wood.get_rect(center=(124, y_pos))
        screen.blit(wood, wood_rect)

        # draw sheep number
        sheep = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['sheep']), True, BLACK)
        sheep_rect = sheep.get_rect(center=(186, y_pos))
        screen.blit(sheep, sheep_rect)

        # draw wheat number
        wheat = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['wheat']), True, BLACK)
        wheat_rect = wheat.get_rect(center=(246, y_pos))
        screen.blit(wheat, wheat_rect)

        # draw ore number
        ore = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['ore']), True, BLACK)
        ore_rect = ore.get_rect(center=(306, y_pos))
        screen.blit(ore, ore_rect)

        # draw brick number
        brick = BANK_NUMBER_FONT.render("{}".format(self.bank_resources['brick']), True, BLACK)
        brick_rect = brick.get_rect(center=(366, y_pos))
        screen.blit(brick, brick_rect)

        # draw dev_card number
        dev_card = BANK_NUMBER_FONT.render("{}".format(len(self.dev_cards)), True, BLACK)
        dev_card_rect = dev_card.get_rect(center=(426, y_pos))
        screen.blit(dev_card, dev_card_rect)



