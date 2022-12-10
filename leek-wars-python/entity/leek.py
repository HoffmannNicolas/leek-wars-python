
from .entity import Entity


class Leek(Entity):

    """ Leek entity """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = Entity.LEEK


    def isLeek(self):
        return True



if (__name__ == "__main__") :

    leek = Leek.sample()

    print(leek)
