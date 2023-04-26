import math
import pygame
import random
from catan.constants import BEIGE, HEXAGON_RADIUS, BUFFER, SCREEN_HEIGHT, SCREEN_WIDTH, GRID_SIZE, \
    EXCLUDED_INDICES, RESOURCE_TYPES, NUMBER_LIST, NUMBER_FONT, BLACK, CYAN, BACKGROUND_UI_IMAGE


class Board:
    """
    A class representing the game board.

    Attributes:
       grid (dict): A dictionary storing the position, resource type, and number for each hexagon on the board.
       resources (list): A list of all resource types available in the game.
       resource_list (list): A list of resource types to be used to assign resource types to the hexagons.
                             This list is shuffled each time the `update_resources` method is called.
    """
    def __init__(self):
        """
        Initializes a new instance of the `Board` class with an empty `grid` dictionary, copies of `RESOURCE_TYPES`,
        `resource_list` set to `None`, and positions generated using `generate_hex_positions`. Calls the
        `update_numbers` and `update_resources` methods to assign random numbers and resource types to the hexagons.
        """
        self.grid = {}
        self.resources = RESOURCE_TYPES.copy()
        self.resource_list = None
        self.generate_hex_positions(GRID_SIZE, HEXAGON_RADIUS)
        self.update_numbers()
        self.update_resources()


    def draw_house(self, surface, position):
        """
        Draws a house on the specified surface at the specified position.

        Args:
            surface (pygame.Surface): The surface on which the house will be drawn.
            position (tuple): A tuple representing the x and y coordinates of the position at which the house will be
                              drawn.

        Returns:
            None
        """

        pygame.draw.circle(surface, CYAN, position, 15)

    def get_grid(self):
        """
        Returns the `grid` dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the position, resource type, and number for each hexagon on the board.
        """
        pass
        return self.grid

    def get_hexagons_positions(self):
        """
        Returns a list of positions for each hexagon on the board.

        Args:
            None

        Returns:
            list: A list of positions for each hexagon on the board.
        """
        positions = []
        for key, values in self.grid.items():
            if values["position"] is not None:
                positions.append([key, values["position"]])
        return positions

    def update_resources(self):
        """
        Assigns resource types to the hexagons on the board. This method shuffles the `resource_list` attribute and
        assigns each resource type to a hexagon until the list is exhausted.

        Args:
            None

        Returns:
            None
        """
        if not self.resources:
            return

        resource_list = self.resources.copy()
        random.shuffle(resource_list)
        self.resource_list = resource_list.copy()
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                resource_type_name = resource_list.pop(0)  # Remove the first resource from the list and assign it
                resource_type_surface = pygame.image.load(f"assets/tile/{resource_type_name}.png")  # Load image
                values["resource_type"] = (resource_type_name, resource_type_surface)  # Store (name, image_surface)

    def update_resources_from_load(self, resource_list):
        """
        Assigns resource types to the hexagons on the board from a given list of resource types.

        Args:
            resource_list (list): A list of resource types to be assigned to the hexagons.

        Returns:
            None
        """
        if not resource_list:
            return

        self.resource_list = resource_list.copy()
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                resource_type_name = resource_list.pop(0)  # Remove the first resource from the list and assign it
                resource_type_surface = pygame.image.load(f"assets/tile/{resource_type_name}.png")  # Load image
                values["resource_type"] = (resource_type_name, resource_type_surface)  # Store (name, image_surface)

    def update_numbers(self):
        """
        Assigns random numbers to the hexagons on the board.

        Args:
            None

        Returns:
            None
        """
        number_list_copy = list(NUMBER_LIST)
        if not number_list_copy:
            return
        random.shuffle(number_list_copy)  # Shuffle the list of numbers
        for pos, values in self.grid.items():
            if pos not in EXCLUDED_INDICES:
                number_type = number_list_copy.pop(0)  # Remove the first number from the list and assign it
                values["number"] = number_type  # Update the "number_type" value in the dictionary

    def generate_hex_positions(self, n, radius):
        """
        Generates positions for each hexagon on the board and stores them in the `grid` dictionary.

        Args:
            n (int): The number of hexagons per row/column on the board.
            radius (int): The radius of each hexagon.

        Returns:
            list: A list of positions for each hexagon on the board.
        """
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
        """
        Draws the game board on the specified screen.

        Args:
            screen (pygame.Surface): The screen on which the game board will be drawn.

        Returns:
            None
        """
        screen.blit(BACKGROUND_UI_IMAGE, (0, 0))

        for pos, values in self.grid.items():

            if values["resource_type"] is not None:
                # Blit the resource tile onto the screen at the hexagon position
                resource_image = values["resource_type"][1]
                resource_rect = resource_image.get_rect(center=values["position"])
                screen.blit(resource_image, resource_rect)

            if values["number"] is not None and values["resource_type"][0] != 'desert':
                number_text = NUMBER_FONT.render(str(values["number"]), True, BLACK)
                number_rect = number_text.get_rect(center=(values["position"][0], values['position'][1] - 29.5))
                screen.blit(number_text, number_rect)

    def generate_grid_save(self):
        """
        Generates a dictionary representing the `grid` attribute and `resource_list` attribute, which can be used to
        save the game state.

        Args:
            None

        Returns:
            dict: A dictionary representing the `grid` attribute and `resource_list`
        """
        save_grid = {"resource_list": self.resource_list}
        for key, value in self.grid.items():
            save_grid[str(key)] = {
                "position": value["position"],
                "resource_type": None,
                "number": value["number"]
            }
        return save_grid
