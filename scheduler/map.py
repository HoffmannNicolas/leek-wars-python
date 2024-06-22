
import numpy as np
import matplotlib.pyplot as plt

from typing import Tuple

# Make a new type called "Position" for a tuple of two ints
Position = Tuple[int, int]


class Map():

    """ A 2D discretized map of the world.
    It is composed of two layers on top of each other:
    - The obstacle layer containing 0 (free cell) or 1 (obstacle).
    - The entity layer containing 0 (free) or n (entity index). At most one entity per cell. """

    def __init__(
        self,
        obstacle_layer,
        entity_layer,
    ):

        assert entity_layer.shape == obstacle_layer.shape, f"Layers must have the same shape. Got {obstacle_layer.shape} and {entity_layer.shape}."

        width, height = obstacle_layer.shape
        self._width, self._height = width, height
        self._obstacle_layer = obstacle_layer
        self._entity_layer = entity_layer


    def position_is_in_map(self, position: Position):
        x, y = position
        if x < 0 or x >= self._width:
            return False
        if y < 0 or y >= self._height:
            return False
        return True


    def obstacle_at_position(self, position: Position) -> bool:
        """Check if a cell contains an obstacle.
        
        Parameters
        ==========
        position
            The position to check for an obstacle.

        Returns
        =======
        bool
            True if the cell contains an obstacle, False otherwise.
        """
        return self._obstacle_layer[position] == 1


    def entity_at_position(self, position: Position) -> bool:
        """Check if a cell contains an entity.
        
        Parameters
        ==========
        position
            The position to check for an entity.

        Returns
        =======
        bool
            True if the cell contains an entity, False otherwise.
        """
        return self._entity_layer[position] != 0


    def distance_between(self, position_1: Position, position_2: Position, order: int = 1) -> float:
        """Compute the L1 or L2 distance between two positions.

        Parameters
        ==========
        position_1
            The first position.
        position_2
            The second position.
        order
            The norm to use for the distance computation. Must be 1 or 2.

        Returns
        =======
        float
            The distance between the two positions.
        """

        if order == 1:
            return abs(position_1[0] - position_2[0]) + abs(position_1[1] - position_2[1])

        return np.linalg.norm(np.array(position_1) - np.array(position_2), ord=2)


    def add_entity(self, entity_index: int, position: Position) -> bool:
        """Add an entity to the map at a specified position.

        Parameters
        ==========
        entity_index
            The index of the entity to be added.
        position
            The coordinates of the position where the entity is to be added.

        Returns
        =======
        bool
            True if the entity was successfully added, False otherwise.
        """
        if not self.position_is_in_map(position):
            return False
        if self.obstacle_at_position(position):
            return False
        if self.entity_at_position(position):
            return False

        self._entity_layer[position] = entity_index
        return True


    def remove_entity_at(self, position: Position) -> bool:
        """Remove an entity from the map at a specified position.

        Parameters
        ==========
        position
            The coordinates of the position where the entity is to be removed.
        
        Returns
        =======
        bool
            True if the entity was successfully removed, False otherwise.
        """

        if not self.position_is_in_map(position):
            return False

        self._entity_layer[position] = 0
        return True


    def iterate_neighbouring_cells(self, position: Position) -> list[Position]:
        """ Return a list of neighbouring cells of the given cell.
        
        Parameters
        ==========
        position
            The position of the cell for which to find neighbouring cells.
            
        Returns
        =======
        list
            A list of neighbouring cells.
        """

        x, y = position
        return filter([
            (x-1, y-1),
            (x-1, y),
            (x-1, y+1),
            (x, y-1),
            (x, y+1),
            (x+1, y-1),
            (x+1, y),
            (x+1, y+1)
        ], self.position_is_in_map)
 

    def compute_cells_in_area(self, cell, distance):

        """ Return a dictionary of cells in the area around the given cell."""

        assert distance >= 0, "Distance must be positive."
        assert self.position_is_in_map(cell), "Cell must be in the map."

        frontier = [cell]
        cells_in_area = {}

        while len(frontier) > 0:

            current_cell = frontier.pop(0)
            cell_distance = self.distance_between(cell, current_cell)

            if cell_distance > distance:
                continue

            if current_cell in cells_in_area:
                continue

            cells_in_area[current_cell] = cell_distance

            for neighbour_cell in self.iterate_neighbouring_cells(current_cell):
                frontier.append(neighbour_cell)

        return cells_in_area


    def compute_entities_in_area(self, cell, distance):

        """ Return a list of entities in the area around the given cell.
        This can be greatly optimized by using a spatial data structure."""

        entities_in_area = []

        for cell in self.compute_cells_in_area(cell, distance):

            if self.entity_at_position(cell):
                entities_in_area.append(self._entity_layer[cell])

        return entities_in_area


    @classmethod
    def generate_empty(cls, width=10, height=10):

        """ Generate an empty map with the given dimensions."""

        entity_layer = np.zeros((width, height), dtype=np.uint8)
        obstacle_layer = np.zeros((width, height), dtype=np.uint8)

        return cls(obstacle_layer, entity_layer)


    @classmethod
    def sample_uniform(cls, width=10, height=10, obstacle_probability=0.1):

        """ Generate a map with random obstacles."""

        entity_layer = np.zeros((width, height), dtype=np.uint8)
        obstacle_layer = np.random.rand(width, height) < obstacle_probability

        return cls(obstacle_layer, entity_layer)


    @classmethod
    def generate_default_map(cls, width=100, height=20, obstacle_probability=0.1, spawn_size_prop=0.1):

        """ Generate a default map with a door in the middle and a Z shape path."""

        entity_layer = np.zeros((width, height), dtype=np.uint8)
        obstacle_layer = np.random.rand(width, height) < obstacle_probability

        # Remove obstacles in the spawn area
        spawn_size_pixel = int(spawn_size_prop * width)
        obstacle_layer[:spawn_size_pixel, :] = 0
        obstacle_layer[-spawn_size_pixel:, :] = 0

        # Add walls around the spawn area
        obstacle_layer[spawn_size_pixel, :] = 1
        obstacle_layer[-spawn_size_pixel, :] = 1
        # Add door in the middle
        mid_y = height // 2
        obstacle_layer[spawn_size_pixel, mid_y] = 0
        obstacle_layer[-spawn_size_pixel, mid_y] = 0

        # Ensure there is always at least one attack path by carving a Z shape path.
        mid_x = width // 2
        obstacle_layer[mid_x:, 0] = 0
        obstacle_layer[mid_x, :] = 0
        obstacle_layer[:-mid_x, -1:] = 0

        return cls(obstacle_layer, entity_layer)



class Map_test(Map):

    """ A subclass of the Map class with additional testing methods."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def plot_obstacles(self):

        plt.imshow(self._obstacle_layer, cmap='gray')
        plt.show()


    def plot_distance(self):

        to_show = self._obstacle_layer.copy().astype(np.float32)

        mid_cell = (self._width // 2, self._height // 2)
        cells_in_area = self.compute_cells_in_area(mid_cell, 50)

        for cell in cells_in_area:
            to_show[cell] = 0.5

        plt.imshow(to_show, cmap='gray')
        plt.show()



def main():
    map = Map_test.generate_default_map(width=200, height=200)
    map.plot_obstacles()
    # map.plot_distance()

    # Inspect object map and print all methods with params
    methods = [method for method in dir(map) if callable(getattr(map, method))]
    methods = [method for method in methods if not method.startswith("__")]
    for method in methods:
        print(f"Method: {method}")
    


if __name__ == "__main__":
    main()