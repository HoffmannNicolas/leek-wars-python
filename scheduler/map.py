
import numpy as np
import matplotlib.pyplot as plt



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


    def cell_is_in_map(self, cell):
        x, y = cell
        if x < 0 or x >= self._width:
            return False
        if y < 0 or y >= self._height:
            return False
        return True


    def cell_contains_obstacle(self, cell):
        x, y = cell
        return self._obstacle_layer[x, y] == 1


    def cell_contains_entity(self, cell):
        x, y = cell
        return self._entity_layer[x, y] != 0


    def compute_distance_between_cells(self, cell1, cell2):
        return abs(cell1[0] - cell2[0]) + abs(cell1[1] - cell2[1])
    def compute_distance_between_entities(self, entity1, entity2):
        return self.compute_distance_between_cells(entity1.get_cell(), entity2.get_cell())


    def add_entity(self, entity_index, cell):

        """ Add the entity to the map at the given cell, if possible.
        Return True if the entity was added, False otherwise. """

        if not self.cell_is_in_map(cell):
            return False
        if self.cell_contains_obstacle(cell):
            return False
        if self.cell_contains_entity(cell):
            return False

        x, y = cell
        self._entity_layer[x, y] = entity_index
        return True


    def remove_entity_by_cell(self, cell):

        """ Remove the entity at the given cell, if possible.
        Return True if the entity was removed, False otherwise. """

        if not self.cell_is_in_map(cell):
            return False

        x, y = cell
        self._entity_layer[x, y] = 0
        return True


    def find_cell_of_entity(self, entity_index):

        """ Return the cell of the entity with the given index, if any.
        This function is not efficient and should be used sparingly."""

        x, y = np.where(self._entity_layer == entity_index)

        if len(x) == 0:
            return None

        return (x[0], y[0])


    def remove_entity_by_index(self, entity_index):

        """ Remove the entity with the given index, if possible.
        Return True if the entity was removed, False otherwise.
        This function is not efficient and should be used sparingly."""

        entity_cell = self.find_cell_of_entity(entity_index)
        if entity_cell is None:
            return False
        return self.remove_entity_by_cell(entity_cell)


    def iterate_neighbouring_cells(self, cell):

        """ Iterate over the neighbouring valid cells of the given cell."""

        x, y = cell
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:

                if dx == 0 and dy == 0:
                    continue # Skip the cell itself

                neighbour = (x + dx, y + dy)

                if not self.cell_is_in_map(neighbour):
                    continue

                yield neighbour


    def compute_cells_in_area(self, cell, distance):

        """ Return a dictionary of cells in the area around the given cell."""

        assert distance >= 0, "Distance must be positive."
        assert self.cell_is_in_map(cell), "Cell must be in the map."

        frontier = [cell]
        cells_in_area = {}

        while len(frontier) > 0:

            current_cell = frontier.pop(0)
            cell_distance = self.compute_distance_between_cells(cell, current_cell)

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

            if self.cell_contains_entity(cell):
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
    map = Map_test.generate_default_map(width=300, height=300)
    map.plot_obstacles()
    map.plot_distance()



if __name__ == "__main__":
    main()