
from .entity import Entity


class Chest(Entity):

    """ Chest entity """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = Entity.CHEST


    def isChest(self):
        return True



if (__name__ == "__main__") :

    chest = Chest.sample()

    print(chest)
