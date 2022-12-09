
import numpy as np
import random
import math


class Terrain():

    """ A terrain inhabited with static obstacles """

    FREE_CELL = 0
    OBSTACLE = 1

    def __init__(self, map):
        self.map = map
        self.width, self.height = map.shape


    def cellIsInMap(self, x, y):
        if (
            x < 0
            or x >= self.width
            or y < 0
            or y >= self.height
        ):
            return False
        return True


    def cellIsFree(self, x, y):
        """ Cell is free.. of static obstacles """
        if (cellIsInMap(x, y)):
            return self.map[x, y] == Terrain.FREE_CELL
        return False


    def __str__(self):
        toPrint = ""
        toPrint += f"[Map] : Height:{self.height} ; Width:{self.width}\n"
        toPrint += str(self.map)
        return toPrint


    @classmethod
    def sample(cls, width=17, height=17, obstacle_proportion=0.15):
        map = np.full([width, height], Terrain.OBSTACLE)
        for x in range(0, width):
            y_range = (width - 1) / 2 - abs((width - 1) / 2 - x)
            y_min = round((height - 1) / 2 - y_range)
            y_max = round((height - 1) / 2 + y_range)
            for y in range(y_min, y_max + 1):
                if (random.random() < obstacle_proportion):
                    map[x, y] = Terrain.OBSTACLE
                else:
                    map[x, y] = Terrain.FREE_CELL
        return cls(map)



if (__name__ == "__main__"):
    terrain = Terrain.sample()
    print(terrain)
