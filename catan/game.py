import pygame, math
from catan import HOUSE_POSITIONS, MOUSE_BUFFER, board, player, COLOR_LIST, UI_BUTTONS, PLACE_HOUSE_BUTTON, \
    END_TURN_BUTTON, PLACE_ROAD_BUTTON, NUMBER_FONT, BLACK, bank, HOUSE_TILE_CHECK, BANK_NUMBER_FONT, \
    QUESTION_MARK_DICE, \
    DEV_CARDS_BUTTON, PLAYER_TRADING_BUTTON, DEV_CARDS_IMAGE, PLAYER_TRADING_IMAGE


class Game:
    def __init__(self, player_names):
        self.board = board.Board()  # create a new game board
        self.players = [player.Player(name, COLOR_LIST[player_names.index(name)]) for name in
                        player_names]  # create a new player list
        self.current_player_index = 0  # initialize the current player index
        self.game_over = False  # initialize the game over flag
        self.bank = bank.Bank()

    def update_state(self, screen):
        # update the game board
        self.bank.draw_bank_resources(screen)
        for current_player in self.players:
            current_player.draw_roads(screen)

        self.check_game_over()  # check if the game is over

    def draw_house(self, screen):
        house_image = None
        for current_player in self.players:
            if current_player == self.players[0]:
                house_image = pygame.image.load("assets/UI/house/P1.png")
            elif current_player == self.players[1]:
                house_image = pygame.image.load("assets/UI/house/P2.png")
            elif current_player == self.players[2]:
                house_image = pygame.image.load("assets/UI/house/P3.png")
            elif current_player == self.players[3]:
                house_image = pygame.image.load("assets/UI/house/P4.png")
            current_player.draw_houses(screen, house_image)

    def isnt_to_close_to_other_houses(self, pos):
        for p in self.players:
            for house in p.get_house():
                distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
                if distance < 130:
                    return False
        return True

    def get_players(self):
        return self.players

    def check_game_over(self):
        # check if any player has reached 10 victory points
        for current_player in self.players:
            if current_player.victory_points >= 10:
                self.game_over = True

    def get_current_player(self):
        return self.players[self.current_player_index]

    def end_turn(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def give_resources(self, current_player):
        dice_number = current_player.get_dice_number()
        tile_grid = self.board.get_grid()
        tiles_with_num = {}
        for position, values in self.board.grid.items():
            if values["number"] is not None and values["number"] == dice_number:
                tiles_with_num[position] = values["resource_type"]

        house_pos_with_number = []
        for xy, resource_type in tiles_with_num.items():
            for pos_2, vertices in HOUSE_TILE_CHECK.items():
                if xy == pos_2:
                    house_pos_with_number.append({"pos": xy, "vertices": vertices})

        players_to_receive = []
        for payer in self.players:
            for house in payer.get_house():
                for house_pos in house_pos_with_number:
                    if house in house_pos["vertices"]:
                        players_to_receive.append((payer, house_pos["pos"]))

        for p in self.players:
            for pp, tile in players_to_receive:
                if pp == p:
                    print("adding resources to", p.get_name())
                    test = tile_grid[tile]["resource_type"][0]
                    if self.bank.get_bank_resource(test) > 0:
                        p.add_resource(test)
                        self.bank.remove_resources(test)

    def draw_board(self, screen):
        self.board.draw_board(screen)

    def draw_players_resources(self, screen):
        for current_player in self.players:
            if current_player == self.players[0]:
                current_player.draw_player_name(screen, 74)
                current_player.draw_resources(screen, 74)
            elif current_player == self.players[1]:
                current_player.draw_player_name(screen, 114)
                current_player.draw_resources(screen, 114)
            elif current_player == self.players[2]:
                current_player.draw_player_name(screen, 154)
                current_player.draw_resources(screen, 154)
            elif current_player == self.players[3]:
                current_player.draw_player_name(screen, 194)
                current_player.draw_resources(screen, 194)

    def draw_player_bank_ratios(self, screen, current_player):
        ratios = current_player.get_trade_ratios()
        for resource_type, ratio in ratios.items():
            if resource_type == 'forest':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(51, 115))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'pasture':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(161, 115))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'fields':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(272, 115))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'mountains':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(381, 115))
                screen.blit(ratio_image, ratio_rect)
            elif resource_type == 'hills':
                ratio_image = NUMBER_FONT.render("{}:1".format(ratio[0]), True, BLACK)
                ratio_rect = ratio_image.get_rect(center=(491, 115))
                screen.blit(ratio_image, ratio_rect)
        dev_image = BANK_NUMBER_FONT.render("BUY CARD", True, BLACK)
        dev_rect = dev_image.get_rect(center=(602, 115))
        screen.blit(dev_image, dev_rect)

    def ui_Messages(self, screen, game_state, current_player):
        if game_state == 'default':
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 100))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == "initial house placements P1" or game_state == "initial road placements P1":
            self.draw_trade_dev_buttons(screen)
            message_1 = NUMBER_FONT.render("Place Initial Settlements!".format(current_player.get_name()), True,
                                           current_player.get_color())
            message_1_rect = message_1.get_rect(center=(960, 100))
            message_2 = NUMBER_FONT.render("{}! Place 1 settlement and 1 road!".format(current_player.get_name()), True,
                                           current_player.get_color())
            message_2_rect = message_2.get_rect(center=(960, 140))
            screen.blit(message_1, message_1_rect)
            screen.blit(message_2, message_2_rect)

            dice_rect_1 = QUESTION_MARK_DICE.get_rect(center=(508, 47))
            dice_rect_2 = QUESTION_MARK_DICE.get_rect(center=(593, 47))
            screen.blit(QUESTION_MARK_DICE, dice_rect_1)
            screen.blit(QUESTION_MARK_DICE, dice_rect_2)

        elif game_state == "initial house placements P2+" or game_state == "initial road placements P2+":
            self.draw_trade_dev_buttons(screen)
            message_1 = NUMBER_FONT.render("Place Initial Settlements!".format(current_player.get_name()), True,
                                           current_player.get_color())
            message_1_rect = message_1.get_rect(center=(960, 100))
            message_2 = NUMBER_FONT.render("{}! Place 2 settlements and 2 roads!".format(current_player.get_name()),
                                           True, current_player.get_color())
            message_2_rect = message_2.get_rect(center=(960, 140))
            screen.blit(message_1, message_1_rect)
            screen.blit(message_2, message_2_rect)

            dice_rect_1 = QUESTION_MARK_DICE.get_rect(center=(508, 47))
            dice_rect_2 = QUESTION_MARK_DICE.get_rect(center=(593, 47))
            screen.blit(QUESTION_MARK_DICE, dice_rect_1)
            screen.blit(QUESTION_MARK_DICE, dice_rect_2)

        elif game_state == 'place house':
            self.draw_trade_dev_buttons(screen)
            message = pygame.image.load("assets/UI/building_costs/house_cost.png")
            message_rect = message.get_rect(center=(960, 100))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == 'place road':
            self.draw_trade_dev_buttons(screen)
            message = pygame.image.load("assets/UI/building_costs/road_cost.png")
            message_rect = message.get_rect(center=(960, 100))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == 'dice roll':
            self.draw_trade_dev_buttons(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 100))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)
            dice_rect_1 = QUESTION_MARK_DICE.get_rect(center=(508, 47))
            dice_rect_2 = QUESTION_MARK_DICE.get_rect(center=(593, 47))
            screen.blit(QUESTION_MARK_DICE, dice_rect_1)
            screen.blit(QUESTION_MARK_DICE, dice_rect_2)

    def draw_trade_dev_buttons(self, screen):
        # Draw the player trading button with a border
        player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
        player_trading_rect.inflate_ip(20, 20)
        pygame.draw.rect(screen, BLACK, player_trading_rect)
        screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        # Draw the dev cards button with a border
        dev_cards_rect = pygame.Rect(DEV_CARDS_BUTTON)
        dev_cards_rect.inflate_ip(20, 20)
        pygame.draw.rect(screen, BLACK, dev_cards_rect)
        screen.blit(DEV_CARDS_IMAGE, DEV_CARDS_BUTTON)


