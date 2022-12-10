
from .entity import Entity


class Bulb(Entity):

    """ Bulb entity """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = Entity.BULB


    def isBulb(self):
        return True



if (__name__ == "__main__") :

    bulb = Bulb.sample()

    print(bulb)
