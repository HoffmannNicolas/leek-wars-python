
class Entity():

    """ Base class for all entities in the game. """

    n_entities = 0

    def __init__(self, position):
        self._position = position
        self._index = Entity.n_entities
        Entity.n_entities += 1


    def get_position(self):
        return self._position



def main():

    # Create a bunch of entities and verify their their index
    for _ in range(10):
        e = Entity((0, 0))
        print(e._index)

    print(f"n_entities: {Entity.n_entities}")



if __name__ == "__main__":
    main()