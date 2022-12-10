
from .entity import Entity


class Turret(Entity):

    """ Turret entity """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type = Entity.TURRET


    def isTurret(self):
        return True



if (__name__ == "__main__") :

    turret = Turret.sample()

    print(turret)
