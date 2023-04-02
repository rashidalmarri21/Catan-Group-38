import math
import pygame
import random
from catan.constants import BEIGE, HEXAGON_RADIUS, BUFFER, SCREEN_HEIGHT, SCREEN_WIDTH, GRID_SIZE, \
    EXCLUDED_INDICES, RESOURCE_TYPES, NUMBER_LIST, NUMBER_FONT, BLACK, CYAN


class Board:
    def __init__(self):
        self.grid = {}
        self.resources = RESOURCE_TYPES.copy()

        self.generate_hex_positions(GRID_SIZE, HEXAGON_RADIUS)
        self.update_numbers()
        self.update_resources()

    def get_grid(self):
        return self.grid

    def get_hexagons_positions(self):
        positions = []
        for key, values in self.grid.items():
            if values["position"] is not None:
                positions.append([key, values["position"]])
        return positions

    def update_resources(self):
        if not self.resources:
            return

        random.shuffle(self.resources)  # Shuffle the list of resources
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                resource_type_name = self.resources.pop(0)  # Remove the first resource from the list and assign it
                resource_type_surface = pygame.image.load(f"assets/tile/{resource_type_name}.png")  # Load image
                values["resource_type"] = (resource_type_name, resource_type_surface)  # Store (name, image_surface)

    def update_numbers(self):
        number_list_copy = list(NUMBER_LIST)
        if not number_list_copy:
            return
        random.shuffle(number_list_copy)  # Shuffle the list of numbers
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                number_type = number_list_copy.pop(0)  # Remove the first number from the list and assign it
                values["number"] = number_type  # Update the "number_type" value in the dictionary

    def generate_hex_positions(self, n, radius):
        positions = []
        x_offset = (radius + BUFFER) * math.sqrt(3)
        y_offset = (radius + BUFFER) * 1.5

        # define indices of hexagons to exclude
        excluded_indices = EXCLUDED_INDICES

        for y in range(n):
            for x in range(n):
                # calculate position of hexagon
                x_pos = (x_offset * x) + ((y % 2) * x_offset / 2) + (
                        (SCREEN_WIDTH / 2) - ((n - 1) * x_offset / 2))
                y_pos = (y_offset * y) + ((SCREEN_HEIGHT / 2) - ((n - 1) * y_offset / 2))
                pos = (x_pos, y_pos)

                # check if hexagon is excluded
                if (x, y) in excluded_indices:
                    # store excluded hexagon with None value
                    self.grid[(x, y)] = {
                        "position": pos,
                        "resource_type": None,
                        "number": None
                    }
                else:
                    # store hexagon position in the dictionary
                    self.grid[(x, y)] = {
                        "position": pos,
                        "resource_type": None,
                        "number": None
                    }
                    positions.append(pos)

        return positions

    def draw_board(self, screen):
        screen.fill(BEIGE)

        for pos, values in self.grid.items():

            if values["resource_type"] is not None:
                # Blit the resource tile onto the screen at the hexagon position
                resource_image = values["resource_type"][1]
                resource_rect = resource_image.get_rect(center=values["position"])
                screen.blit(resource_image, resource_rect)

            if values["number"] is not None and values["resource_type"][0] != 'desert':
                number_text = NUMBER_FONT.render(str(values["number"]), True, BLACK)
                number_rect = number_text.get_rect(center=values["position"])
                screen.blit(number_text, number_rect)
