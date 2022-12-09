

from abc import ABC

class Item(ABC):

    """ Abstract class containing items """

    def __init__(self, range_min, range_max, turn_points, area, effects):
        self.range_min = range_min
        self.range_max = range_max
        self.turn_points = turn_points # Cost of using the item in PT
        self.area = area # Cells affected by the item
        self.effects = effects # Effects of the item on affected entities
