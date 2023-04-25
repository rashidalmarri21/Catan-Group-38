import json

import pygame, math, random

import catan.ai_agent
from catan.ai_agent import every_house_in_play
from catan.ai_agent import AIAgent
from catan import HOUSE_POSITIONS, MOUSE_BUFFER, board, player, COLOR_LIST, UI_BUTTONS, PLACE_HOUSE_BUTTON, \
    END_TURN_BUTTON, PLACE_ROAD_BUTTON, NUMBER_FONT, BLACK, bank, HOUSE_TILE_CHECK, BANK_NUMBER_FONT, \
    QUESTION_MARK_DICE, \
    DEV_CARDS_BUTTON, PLAYER_TRADING_BUTTON, DEV_CARDS_IMAGE, PLAYER_TRADING_IMAGE, DEV_CARDS_UI_IMAGE, \
    DEV_CARDS_UI_RECT, \
    KNIGHT_INFO_DEV, KNIGHT_INFO_DEV_RECT, DEV_CARDS_KNIGHT_UI_RECT, DEV_CARDS_KNIGHT_UI_IMAGE, GREY_USE_DEV, \
    GREY_USE_RECT, \
    BLANK_INFO_DEV, BLANK_INFO_DEV_RECT, DEV_CARDS_ROAD_BUILDING_UI_IMAGE, DEV_CARDS_ROAD_BUILDING_UI_RECT, \
    DEV_CARDS_YEAR_UI_IMAGE, \
    DEV_CARDS_YEAR_UI_RECT, DEV_CARDS_MONOPOLY_UI_IMAGE, DEV_CARDS_MONOPOLY_UI_RECT, DEV_CARDS_VICTORY_UI_IMAGE, \
    DEV_CARDS_VICTORY_UI_RECT, \
    VICTORY_INFO_DEV, VICTORY_INFO_RECT, ROAD_BUILDING_INFO_DEV, ROAD_BUILDING_INFO_DEV_RECT, MONOPOLY_INFO_DEV, \
    MONOPOLY_INFO_DEV_RECT, \
    YEAR_INFO_DEV, YEAR_INFO_DEV_RECT, ROBBER, MONOPOLY_EFFECT_IMAGE, MONOPOLY_EFFECT_RECT, YEAR_EFFECT_IMAGE, \
    YEAR_EFFECT_RECT, \
    FLAG_POSITIONS, FLAG_LIST, FLAG_HOUSE_CHECK, WOOD_FLAG, WHEAT_FLAG, ORE_FLAG, BRICK_FLAG, SHEEP_FLAG, ANY_FLAG, \
    SHEEP_IMAGE, WHEAT_IMAGE, WOOD_IMAGE, ORE_IMAGE, BRICK_IMAGE, MARITIME_TRADE, BUY_DEV_TRADE, KNIGHT_BUY_DEV, \
    ROAD_BUILDING_BUY_DEV, MONOPOLY_BUY_DEV, VICTORY_BUY_DEV, YEAR_BUY_DEV, PLAYER_ROBBER_IMAGE, ROBBER_EFFECT, \
    ROBBER_EFFECT_RECT, \
    RED, BLUE, ORANGE, PURPLE, WHITE, button, NAME_PLATE, PLAYER_TRADING_UI, PLAYER_TRADE_UI, PLAYER_TRADE_UI_RECT, \
    PAUSE_MENU_UI, PAUSE_MENU_RECT, ROAD_POSITIONS, CYAN, BROWN, PINK, GAME_HELP_IMAGE, GAME_HELP_IMAGE_RECT


class Game:
    def __init__(self, player_names, color_list):
        self.board = board.Board()  # create a new game board
        self.players = []
        for name in player_names:
            if "AI" in name:
                self.players.append(AIAgent(name, color_list[player_names.index(name)]))  # create an AI agent
            else:
                self.players.append(
                    player.Player(name, color_list[player_names.index(name)]))  # create a regular player
        self.current_player_index = 0  # initialize the current player index
        self.game_over = False  # initialize the game over flag
        self.bank = bank.Bank()
        # calculate robbers starting position
        self.robber_pos = ()
        self.longest_road_player = None
        self.largest_army_player = None
        self.trade_player_list = None
        self.trader_x_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.trader_y_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.house_positions = HOUSE_POSITIONS.copy()
        self.road_positions = ROAD_POSITIONS.copy()

        self.current_board = self.board.get_grid()
        for pos, tile in self.current_board.items():
            if tile["resource_type"] is not None:
                if tile['resource_type'][0] == 'desert':
                    self.robber_pos = tile["position"]
        self.possible_robber_pos = {}
        self.update_robber_pos_list()
        self.flag_list = FLAG_LIST
        random.shuffle(self.flag_list)

    def get_AI_player(self):
        AI_players = []
        for p in self.players:
            if "AI" in p.get_name():
                AI_players.append(p)
        if len(AI_players) == 0:
            return False
        else:
            return AI_players

    def generate_game_save(self):
        flag_list_to_str = []
        for flag in FLAG_LIST:
            if flag == WOOD_FLAG:
                flag_list_to_str.append("WOOD")
            elif flag == WHEAT_FLAG:
                flag_list_to_str.append("WHEAT")
            elif flag == ORE_FLAG:
                flag_list_to_str.append("ORE")
            elif flag == BRICK_FLAG:
                flag_list_to_str.append("BRICK")
            elif flag == SHEEP_FLAG:
                flag_list_to_str.append("SHEEP")
            elif flag == ANY_FLAG:
                flag_list_to_str.append("ANY")
        if self.get_AI_player() is not False:
            game_save = {
                "current player index": self.current_player_index,
                "robber pos": self.robber_pos,
                "flag list": flag_list_to_str,
                "house pos": self.house_positions,
                "road pos": self.road_positions,
                "every house": catan.ai_agent.every_house_in_play
            }
        else:
            game_save = {
                "current player index": self.current_player_index,
                "robber pos": self.robber_pos,
                "flag list": flag_list_to_str,
                "house pos": self.house_positions,
                "road pos": self.road_positions,
                "every house": None
            }
        return game_save


    def load_player_data(self):
        player_data = None
        with open("player_data.txt") as player_file:
            player_data = json.load(player_file)

        for px, data in player_data.items():
            for py in self.players:
                if py.get_name() == px:
                    py.victory_points = data["victory points"]
                    py.houses = data["houses"]
                    py.cities = data["cities"]
                    py.roads = data["roads"]
                    py.resources = data["resources"]
                    py.development_cards = data["dev cards"]
                    py.knights_played = data["knights played"]
                    py.dice_roll = data["dice roll"]
                    py.trade_ratios = data["trade ratios"]

    def load_board_data(self):
        board_data = None
        with open("board_data.txt") as board_file:
            board_data = json.load(board_file)

        for k, data in board_data.items():
            for key, value in self.board.grid.items():
                if str(key) == k:
                    value["number"] = data["number"]

        self.board.update_resources_from_load(board_data["resource_list"])

    def load_bank_data(self):
        bank_data = None
        with open("bank_data.txt") as bank_file:
            bank_data = json.load(bank_file)

        self.bank.dev_cards = bank_data["dev cards"]
        for key, value in bank_data.items():
            for pee, palue in self.bank.bank_resources.items():
                if key == pee:
                    self.bank.bank_resources[pee] = value

    def load_game_data(self):
        game_data = None
        with open("game_data.txt") as game_file:
            game_data = json.load(game_file)

        self.current_player_index = game_data["current player index"]
        self.robber_pos = game_data["robber pos"]
        self.update_robber_pos_list()
        self.remove_robber_pos()
        temp_flag_list = game_data["flag list"]
        self.flag_list = []
        for flag in temp_flag_list:
            if flag == "WOOD":
                self.flag_list.append(WOOD_FLAG)
            elif flag == "WHEAT":
                self.flag_list.append(WHEAT_FLAG)
            elif flag == "SHEEP":
                self.flag_list.append(SHEEP_FLAG)
            elif flag == "ORE":
                self.flag_list.append(ORE_FLAG)
            elif flag == "BRICK":
                self.flag_list.append(BRICK_FLAG)
            elif flag == "ANY":
                self.flag_list.append(ANY_FLAG)

        self.house_positions = game_data["house pos"]
        self.road_positions = game_data["road pos"]
        if self.get_AI_player() is not False:
            catan.ai_agent.every_house_in_play = game_data["every house"]

    def update_state(self, screen):
        # update the game board
        self.bank.draw_bank_resources(screen)
        self.flag_house_check()
        for current_player in self.players:
            current_player.draw_roads(screen)



    def update_trade_player_list(self, current_player):
        player_list = []
        for p in self.players:
            if p != current_player:
                player_list.append(p)
        self.trade_player_list = player_list

    def add_resource_x_trader(self, resource_type):
        self.trader_x_pool[resource_type] += 1

    def remove_resource_x_trader(self, resource_type):
        self.trader_x_pool[resource_type] -= 1

    def add_resource_y_trader(self, resource_type):
        self.trader_y_pool[resource_type] += 1

    def remove_resource_y_trader(self, resource_type):
        self.trader_y_pool[resource_type] -= 1

    def swap_trade_pools(self):
        self.trader_x_pool, self.trader_y_pool = self.trader_y_pool, self.trader_x_pool

    def give_pool_resources_to_players(self, current_player, trade_player):
        for key, value in self.trader_x_pool.items():
            current_player.resources[key] += value

        for key, value in self.trader_y_pool.items():
            trade_player.resources[key] += value

    def reset_trade_pools(self):
        self.trader_x_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}
        self.trader_y_pool = {'forest': 0, 'hills': 0, 'pasture': 0, 'fields': 0, 'mountains': 0}

    def robber_take_resource_from_rand_player(self, current_player):
        tile = None
        resource_to_take = None
        for key, value in self.board.get_grid().items():
            if self.robber_pos == value["position"]:
                tile = key
                resource_to_take = value["resource_type"][0]

        players_on_tile = []
        for p in self.players:
            if p is not current_player:
                for house in p.houses:
                    for tiles, houses in HOUSE_TILE_CHECK.items():
                        if tiles == tile:
                            for h in houses:
                                if house == h:
                                    players_on_tile.append(p)
        if len(players_on_tile) != 0:
            chosen_player = random.choice(players_on_tile)
            if resource_to_take != 'desert':
                if chosen_player.resources[resource_to_take] > 1:
                    chosen_player.remove_resource(resource_to_take)
                    current_player.add_resource(resource_to_take)

    def discard_if_7(self):
        pass
    def update_largest_army_player(self):
        for p in self.players:
            if p.knights_played >= 3:
                if self.largest_army_player is not None:
                    if p.knights_played > self.largest_army_player.knights_played:
                        self.largest_army_player.remove_victory_point()
                        self.largest_army_player.remove_victory_point()
                        p.add_victory_point()
                        p.add_victory_point()
                        self.largest_army_player = p
                else:
                    p.add_victory_point()
                    p.add_victory_point()
                    self.largest_army_player = p

    def update_longest_road_player(self):
        for p in self.players:
            if len(p.roads) >= 3:
                if self.longest_road_player is not None:
                    if len(p.roads) > len(self.longest_road_player.roads):
                        self.longest_road_player.remove_victory_point()
                        self.longest_road_player.remove_victory_point()
                        p.add_victory_point()
                        p.add_victory_point()
                        self.longest_road_player = p
                else:
                    p.add_victory_point()
                    p.add_victory_point()
                    self.longest_road_player = p

    def update_robber_pos_list(self):
        for pos, tile in self.current_board.items():
            if tile["resource_type"] is not None:
                if tile['position'] != (self.robber_pos[0], self.robber_pos[1]):
                    self.possible_robber_pos[pos] = (tile["position"][0] - 45, tile["position"][1])

    def update_robber_pos(self, new_robber_pos):
        self.robber_pos = new_robber_pos

    def remove_robber_pos(self):
        for key, value in self.possible_robber_pos.copy().items():
            if value == (self.robber_pos[0] - 45, self.robber_pos[1]):
                self.possible_robber_pos.pop(key)
                break

    def list_of_players_with_house_at_robber(self):
        tile = None
        for key, values in self.board.get_grid().items():
            if values["position"] == self.robber_pos:
                tile = key
        player_list = {tile: []}
        for p in self.players:
            for house in p.get_house():
                for key, value in HOUSE_TILE_CHECK.items():
                    if key == tile:
                        for v in value:
                            if house == v:
                                if self.players[self.current_player_index] != p:
                                    player_list[tile].append(p)
        return player_list

    def get_robber_pos(self):
        return self.robber_pos

    def draw_house(self, screen):
        house_image = None
        for current_player in self.players:
            if current_player.get_color() == RED:
                house_image = pygame.image.load('assets/UI/house/red.png')
            elif current_player.get_color() == ORANGE:
                house_image = pygame.image.load('assets/UI/house/orange.png')
            elif current_player.get_color() == PURPLE:
                house_image = pygame.image.load('assets/UI/house/purple.png')
            elif current_player.get_color() == BLUE:
                house_image = pygame.image.load('assets/UI/house/blue.png')
            elif current_player.get_color() == CYAN:
                house_image = pygame.image.load('assets/UI/house/cyan.png')
            elif current_player.get_color() == BROWN:
                house_image = pygame.image.load('assets/UI/house/brown.png')
            elif current_player.get_color() == BLACK:
                house_image = pygame.image.load('assets/UI/house/black.png')
            elif current_player.get_color() == PINK:
                house_image = pygame.image.load('assets/UI/house/pink.png')
            current_player.draw_houses(screen, house_image)

    def draw_city(self, screen):
        city_image = None
        for current_player in self.players:
            if current_player.color == RED:
                city_image = pygame.image.load("assets/UI/city/red.png")
            elif current_player.color == BLUE:
                city_image = pygame.image.load("assets/UI/city/blue.png")
            elif current_player.color == PURPLE:
                city_image = pygame.image.load("assets/UI/city/purple.png")
            elif current_player.color == ORANGE:
                city_image = pygame.image.load("assets/UI/city/orange.png")
            elif current_player.color == PINK:
                city_image = pygame.image.load("assets/UI/city/pink.png")
            elif current_player.color == BLACK:
                city_image = pygame.image.load("assets/UI/city/black.png")
            elif current_player.color == CYAN:
                city_image = pygame.image.load("assets/UI/city/cyan.png")
            elif current_player.color == BROWN:
                city_image = pygame.image.load("assets/UI/city/brown.png")

            current_player.draw_cities(screen, city_image)

    def isnt_to_close_to_other_houses(self, pos):
        for p in self.players:
            for house in p.get_house():
                distance = math.sqrt((pos[0] - house[0]) ** 2 + (pos[1] - house[1]) ** 2)
                if distance < 130:
                    return False
            for city in p.get_cities():
                distance = math.sqrt((pos[0] - city[0]) ** 2 + (pos[1] - city[1]) ** 2)
                if distance < 130:
                    return False
        return True

    def draw_robber(self, screen):
        robber_pos = self.robber_pos
        robber_rect = ROBBER.get_rect(center=((robber_pos[0] - 45), robber_pos[1]))
        screen.blit(ROBBER, robber_rect)

    def get_players(self):
        return self.players

    def check_game_over(self, current_player):
        # check if any player has reached 10 victory points
        if current_player.get_victory_points() >= 10:
            return True
        else:
            return False

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
                    if (house[0], house[1]) in house_pos["vertices"]:
                        players_to_receive.append((payer, house_pos["pos"]))

        for p in self.players:
            for pp, tile in players_to_receive:
                if pp == p:
                    print("adding resource: {} to".format(tile_grid[tile]["resource_type"][0]), p.get_name())
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
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == "initial house placements P1" or game_state == "initial road placements P1":
            self.draw_trade_dev_buttons(screen)
            message_1 = NUMBER_FONT.render("Place Initial Settlements!".format(current_player.get_name()), True,
                                           current_player.get_color())
            message_1_rect = message_1.get_rect(center=(960, 50))
            message_2 = NUMBER_FONT.render("{}! Place 1 settlement and 1 road!".format(current_player.get_name()), True,
                                           current_player.get_color())
            message_2_rect = message_2.get_rect(center=(960, 90))
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
            message_1_rect = message_1.get_rect(center=(960, 50))
            message_2 = NUMBER_FONT.render("{}! Place 2 settlements and 2 roads!".format(current_player.get_name()),
                                           True, current_player.get_color())
            message_2_rect = message_2.get_rect(center=(960, 90))
            screen.blit(message_1, message_1_rect)
            screen.blit(message_2, message_2_rect)

            dice_rect_1 = QUESTION_MARK_DICE.get_rect(center=(508, 47))
            dice_rect_2 = QUESTION_MARK_DICE.get_rect(center=(593, 47))
            screen.blit(QUESTION_MARK_DICE, dice_rect_1)
            screen.blit(QUESTION_MARK_DICE, dice_rect_2)

        elif game_state == 'place house':
            self.draw_trade_dev_buttons(screen)
            message = pygame.image.load("assets/UI/building_costs/house_cost.png")
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == 'place city':
            self.draw_trade_dev_buttons(screen)
            message = pygame.image.load("assets/UI/building_costs/city_cost.png")
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == 'place road':
            self.draw_trade_dev_buttons(screen)
            message = pygame.image.load("assets/UI/building_costs/road_cost.png")
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)
            self.players[self.current_player_index].draw_dice(screen)

        elif game_state == 'dice roll':
            self.draw_trade_dev_buttons(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            dice_rect_1 = QUESTION_MARK_DICE.get_rect(center=(508, 47))
            dice_rect_2 = QUESTION_MARK_DICE.get_rect(center=(593, 47))
            screen.blit(QUESTION_MARK_DICE, dice_rect_1)
            screen.blit(QUESTION_MARK_DICE, dice_rect_2)
        elif game_state == "dev cards":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_UI_IMAGE, DEV_CARDS_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(GREY_USE_DEV, GREY_USE_RECT)

            screen.blit(BLANK_INFO_DEV, BLANK_INFO_DEV_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "player trading":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

        elif game_state == "knight":
            self.players[self.current_player_index].draw_dice(screen)

            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_KNIGHT_UI_IMAGE, DEV_CARDS_KNIGHT_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(KNIGHT_INFO_DEV, KNIGHT_INFO_DEV_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "victory":
            self.players[self.current_player_index].draw_dice(screen)

            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_VICTORY_UI_IMAGE, DEV_CARDS_VICTORY_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(VICTORY_INFO_DEV, VICTORY_INFO_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "road":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_ROAD_BUILDING_UI_IMAGE, DEV_CARDS_ROAD_BUILDING_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(ROAD_BUILDING_INFO_DEV, ROAD_BUILDING_INFO_DEV_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "road effect":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, place 2 roads for free!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

        elif game_state == "monopoly":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_MONOPOLY_UI_IMAGE, DEV_CARDS_MONOPOLY_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(MONOPOLY_INFO_DEV, MONOPOLY_INFO_DEV_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "monopoly effect":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(MONOPOLY_EFFECT_IMAGE, MONOPOLY_EFFECT_RECT)

        elif game_state == "year":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            screen.blit(DEV_CARDS_YEAR_UI_IMAGE, DEV_CARDS_YEAR_UI_RECT)

            current_player.draw_dev_card_numbers(screen)

            screen.blit(YEAR_INFO_DEV, YEAR_INFO_DEV_RECT)

            player_trading_rect = pygame.Rect(PLAYER_TRADING_BUTTON)
            player_trading_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, player_trading_rect)
            screen.blit(PLAYER_TRADING_IMAGE, PLAYER_TRADING_BUTTON)

        elif game_state == "year effect":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(YEAR_EFFECT_IMAGE, YEAR_EFFECT_RECT)

        elif game_state == "robber":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, Pick a tile to place the robber!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)
            self.draw_trade_dev_buttons(screen)

        elif game_state == "bank sheep":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            maritime_rect = MARITIME_TRADE.get_rect(center=(960, 540))
            screen.blit(MARITIME_TRADE, maritime_rect)
            current_player.draw_resource_in_maritime(screen, "sheep")
            current_player.draw_trade_ratio_maritime(screen)
            sheep_rect = SHEEP_IMAGE.get_rect(center=(1217, 383))
            screen.blit(SHEEP_IMAGE, sheep_rect)

        elif game_state == "bank wood":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            maritime_rect = MARITIME_TRADE.get_rect(center=(960, 540))
            screen.blit(MARITIME_TRADE, maritime_rect)
            current_player.draw_resource_in_maritime(screen, "wood")
            current_player.draw_trade_ratio_maritime(screen)
            wood_rect = WOOD_IMAGE.get_rect(center=(1217, 383))
            screen.blit(WOOD_IMAGE, wood_rect)

        elif game_state == "bank wheat":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            maritime_rect = MARITIME_TRADE.get_rect(center=(960, 540))
            screen.blit(MARITIME_TRADE, maritime_rect)
            current_player.draw_resource_in_maritime(screen, "wheat")
            current_player.draw_trade_ratio_maritime(screen)
            wheat_rect = WHEAT_IMAGE.get_rect(center=(1217, 383))
            screen.blit(WHEAT_IMAGE, wheat_rect)

        elif game_state == "bank ore":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            maritime_rect = MARITIME_TRADE.get_rect(center=(960, 540))
            screen.blit(MARITIME_TRADE, maritime_rect)
            current_player.draw_resource_in_maritime(screen, "ore")
            current_player.draw_trade_ratio_maritime(screen)
            ore_rect = ORE_IMAGE.get_rect(center=(1217, 383))
            screen.blit(ORE_IMAGE, ore_rect)

        elif game_state == "bank brick":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            maritime_rect = MARITIME_TRADE.get_rect(center=(960, 540))
            screen.blit(MARITIME_TRADE, maritime_rect)
            current_player.draw_resource_in_maritime(screen, "brick")
            current_player.draw_trade_ratio_maritime(screen)
            brick_rect = BRICK_IMAGE.get_rect(center=(1217, 383))
            screen.blit(BRICK_IMAGE, brick_rect)

        elif game_state == "bank dev":
            self.players[self.current_player_index].draw_dice(screen)
            dev_cost = pygame.image.load("assets/UI/building_costs/dev_cost.png")
            dev_cost_rect = dev_cost.get_rect(center=(960, 50))
            screen.blit(dev_cost, dev_cost_rect)

            self.draw_trade_dev_buttons(screen)

            buy_dev_rect = BUY_DEV_TRADE.get_rect(center=(960, 540))
            screen.blit(BUY_DEV_TRADE, buy_dev_rect)

            knight_dev = KNIGHT_BUY_DEV.get_rect(center=(742, 520))
            screen.blit(KNIGHT_BUY_DEV, knight_dev)

            victory_dev = VICTORY_BUY_DEV.get_rect(center=(851, 520))
            screen.blit(VICTORY_BUY_DEV, victory_dev)

            road_building_dev = ROAD_BUILDING_BUY_DEV.get_rect(center=(960, 520))
            screen.blit(ROAD_BUILDING_BUY_DEV, road_building_dev)

            monopoly_dev = MONOPOLY_BUY_DEV.get_rect(center=(1069, 520))
            screen.blit(MONOPOLY_BUY_DEV, monopoly_dev)

            year_dev = YEAR_BUY_DEV.get_rect(center=(1178, 520))
            screen.blit(YEAR_BUY_DEV, year_dev)

            current_player.draw_dev_card_num_in_bank_trade(screen)

        elif game_state == "robber effect":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a resource!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(ROBBER_EFFECT, ROBBER_EFFECT_RECT)

        elif game_state == "pick player for trade":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, pick a player to trade with!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            dev_cards_rect = pygame.Rect(DEV_CARDS_BUTTON)
            dev_cards_rect.inflate_ip(20, 20)
            pygame.draw.rect(screen, BLACK, dev_cards_rect)
            screen.blit(DEV_CARDS_IMAGE, DEV_CARDS_BUTTON)

            player_trade_UI_rect = PLAYER_TRADING_UI.get_rect(topright=(1920, 486))
            screen.blit(PLAYER_TRADING_UI, player_trade_UI_rect)

        elif game_state == "trade player 1":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, make a trade offer!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(PLAYER_TRADE_UI, PLAYER_TRADE_UI_RECT)
            self.draw_names_on_trade_screen(screen, current_player, 0)
            self.draw_numbers_on_trade_menu(screen, current_player, 0)

        elif game_state == "trade player 2":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, make a trade offer!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(PLAYER_TRADE_UI, PLAYER_TRADE_UI_RECT)
            self.draw_names_on_trade_screen(screen, current_player, 1)
            self.draw_numbers_on_trade_menu(screen, current_player, 1)

        elif game_state == "trade player 3":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("{}, make a trade offer!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)

            screen.blit(PLAYER_TRADE_UI, PLAYER_TRADE_UI_RECT)
            self.draw_names_on_trade_screen(screen, current_player, 2)
            self.draw_numbers_on_trade_menu(screen, current_player, 2)

        elif game_state == "pause menu":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)
            screen.blit(PAUSE_MENU_UI, PAUSE_MENU_RECT)

        elif game_state == "help menu":
            self.players[self.current_player_index].draw_dice(screen)
            message = NUMBER_FONT.render("Ready player {}!".format(current_player.get_name()), True,
                                         current_player.get_color())
            message_rect = message.get_rect(center=(960, 50))
            screen.blit(message, message_rect)

            self.draw_trade_dev_buttons(screen)
            screen.blit(GAME_HELP_IMAGE, GAME_HELP_IMAGE_RECT)

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

    def flag_house_check(self):
        for p in self.players:
            for pos in p.get_house():
                for index, houses in FLAG_HOUSE_CHECK.items():
                    if pos == houses[0] or pos == houses[1]:
                        if FLAG_LIST[index - 1] == WOOD_FLAG:
                            p.update_trade_ratios("forest", (2, 1))
                        elif FLAG_LIST[index - 1] == WHEAT_FLAG:
                            p.update_trade_ratios("fields", (2, 1))
                        elif FLAG_LIST[index - 1] == ORE_FLAG:
                            p.update_trade_ratios("mountains", (2, 1))
                        elif FLAG_LIST[index - 1] == BRICK_FLAG:
                            p.update_trade_ratios("hills", (2, 1))
                        elif FLAG_LIST[index - 1] == SHEEP_FLAG:
                            p.update_trade_ratios("pasture", (2, 1))
                        elif FLAG_LIST[index - 1] == ANY_FLAG:
                            p.update_all_trade_ratios((3, 1))

    def draw_flags(self, screen):
        flag_list = self.flag_list.copy()
        for pos in FLAG_POSITIONS.copy():
            flag_image = flag_list.pop(0)
            flag_rect = flag_image.get_rect(center=pos)
            screen.blit(flag_image, flag_rect)


    def make_buttons_for_player_trading(self, current_player):
        player_buttons = []
        y_pos = 675
        for p in self.players:
            if p != current_player:
                player_button = button.Button(image=NAME_PLATE, pos=(1628, y_pos),text_input="{}".format(p.get_name()),
                                              font=NUMBER_FONT, base_color=p.get_color(), hovering_color=p.get_color(),
                                              border=True, border_width=5, border_color=(127, 127, 127))
                player_buttons.append(player_button)
                y_pos += 97
        return player_buttons

    def draw_names_on_trade_screen(self,screen, current_player, trade_player_index):
        if trade_player_index == 0:
            trade_player_name = NUMBER_FONT.render("{}".format(self.trade_player_list[0].get_name()),True,self.trade_player_list[0].get_color())
        elif trade_player_index == 1:
            trade_player_name = NUMBER_FONT.render("{}".format(self.trade_player_list[1].get_name()),True,self.trade_player_list[1].get_color())
        elif trade_player_index == 2:
            trade_player_name = NUMBER_FONT.render("{}".format(self.trade_player_list[2].get_name()),True,self.trade_player_list[2].get_color())

        current_player_name = NUMBER_FONT.render("{}".format(current_player.get_name()),True,current_player.get_color())
        trade_player_name_rect = trade_player_name.get_rect(center=(1251, 669))
        current_player_name_rect = current_player_name.get_rect(center=(675, 671))
        screen.blit(trade_player_name,trade_player_name_rect)
        screen.blit(current_player_name, current_player_name_rect)


    def draw_numbers_on_trade_menu(self, screen, current_player, trade_player_index):
        # current players resources
        for key, value in current_player.resources.items():
            y_pos = 845
            if key == "forest":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(472, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "pasture":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(574, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "fields":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(676, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "mountains":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(778, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "hills":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(880, y_pos))
                screen.blit(resource_num, resource_rect)

        for key, value in self.trade_player_list[trade_player_index].resources.items():
            y_pos = 845
            if key == "forest":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1055, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "pasture":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1157, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "fields":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1259, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "mountains":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1361, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "hills":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1463, y_pos))
                screen.blit(resource_num, resource_rect)

        for key, value in self.trader_x_pool.items():
            y_pos = 492
            if key == "forest":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(472, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "pasture":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(574, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "fields":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(676, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "mountains":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(778, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "hills":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(880, y_pos))
                screen.blit(resource_num, resource_rect)

        for key, value in self.trader_y_pool.items():
            y_pos = 492
            if key == "forest":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1055, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "pasture":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1157, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "fields":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1259, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "mountains":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1361, y_pos))
                screen.blit(resource_num, resource_rect)
            elif key == "hills":
                resource_num = NUMBER_FONT.render("{}".format(value), True, BLACK)
                resource_rect = resource_num.get_rect(center=(1463, y_pos))
                screen.blit(resource_num, resource_rect)

    def generate_victory_point_list(self):
        vic_list = []
        for p in self.players:
            vic_list.append(p.get_victory_points())
        return vic_list

    def generate_player_name_list(self):
        name_list = []
        for p in self.players:
            name_list.append(p.get_name())
        return name_list

    def generate_sorted_player_score(self):
        vic_list = self.generate_victory_point_list()
        name_list = self.generate_player_name_list()

        name_score_dict = {}
        for score, name in zip(vic_list, name_list):
            name_score_dict[name] = score

        sorted_name_score_dict = dict(sorted(name_score_dict.items(), key=lambda item: item[1], reverse=True))
        return sorted_name_score_dict

    def generate_players_save_data(self):
        players_data = {}
        for p in self.players:
            players_data[p.get_name()] = {
                "color": p.get_color(),
                "victory points": p.get_victory_points(),
                "houses": p.get_house(),
                "cities": p.get_cities(),
                "roads": p.get_roads(),
                "resources": p.get_resources(),
                "dev cards": p.get_development_cards(),
                "knights played": p.get_knights_played(),
                "dice roll": p.get_dice_roll(),
                "trade ratios": p.get_trade_ratios()
            }
        return players_data
