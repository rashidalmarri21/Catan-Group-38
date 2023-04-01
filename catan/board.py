import math

import pygame
import random

from catan.constants import BEIGE, HEXAGON_RADIUS, BUFFER, SCREEN_HEIGHT, SCREEN_WIDTH, GRID_SIZE, \
    EXCLUDED_INDICES, RESOURCE_TYPES


class Board:
    def __init__(self):
        self.grid = {}
        self.selected_piece = None
        self.hexagon_positions = self.generate_hex_positions(GRID_SIZE, HEXAGON_RADIUS)
        self.resources = RESOURCE_TYPES.copy()

    def get_grid(self):
        return self.grid

    def update_resources(self, resources):
        if not resources:
            return
        random.shuffle(self.resources)  # Shuffle the list of resources
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                resource_type = self.resources.pop(0)  # Remove the first resource from the list and assign it
                values["resource_type"] = resource_type  # Update the "resource_type" value in the dictionary

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
                        "rect": None
                    }
                else:
                    # store hexagon position in the dictionary
                    self.grid[(x, y)] = {
                        "position": pos,
                        "resource_type": None,
                        "rect": pygame.Rect(pos[0] - HEXAGON_RADIUS, pos[1] - HEXAGON_RADIUS, HEXAGON_RADIUS * 2,
                                            HEXAGON_RADIUS * 2)
                    }
                    positions.append(pos)
        # for key, value in self.grid.items():
        # print(f"{key}:")
        # print(f"\tposition: {value['position']}")
        # print(f"\tresource_type: {value['resource_type']}")
        # print(f"\trect: {value['rect']}")
        return positions

    def draw_board(self, screen):
        screen.fill(BEIGE)
        self.update_resources(self.resources)
        for pos, values in self.grid.items():
            if values["resource_type"] is not None:
                # Blit the resource tile onto the screen at the hexagon position
                resource_image = values["resource_type"]
                resource_rect = resource_image.get_rect(center=values["position"])
                screen.blit(resource_image, resource_rect)
