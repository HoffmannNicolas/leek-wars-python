
from abc import ABC
import random

class Entity(ABC):

    """ Abstract mother class of all entities : Leeks, Bulbs, Turrets and chests """

    # Names of entities
    LEEK = 0
    BULB = 1
    TURRET = 2
    CHEST = 3

    def __init__(self, stats, items, policy):
        self.stats = stats
        self.items = items
        self.policy = policy
        self.type = None # Exactely one of <LEEK>, <BULB>, <TURRET> or <CHEST>


    def isLeek(self):
        return False


    def isBulb(self):
        return False


    def isTurret(self):
        return False


    def isChest(self):
        return False


    def __str__(self):
        toPrint = ""
        if (self.type == Entity.LEEK) : toPrint += f"[Leek]"
        if (self.type == Entity.BULB) : toPrint += f"[Bulb]"
        if (self.type == Entity.TURRET) : toPrint += f"[Turret]"
        if (self.type == Entity.CHEST) : toPrint += f"[Chest]"
        toPrint += "\n"
        toPrint += f"\t-Items: {self.items}\n"
        for (stat_name, stat_value) in self.stats.items() :
            toPrint += f"\t-{stat_name}: {stat_value}\n"
        return toPrint


    @classmethod
    def sample(cls) :

        """ Sample a random <Entity>.
        Although this very class cannot be instanciated, all children can be randomly sampled the same way."""

        randomStats = {
            "Max Life Points" : random.randint(0, 100),
            "Strength" : random.randint(0, 100),
            "Wisdom" : random.randint(0, 100),
            "Agility" : random.randint(0, 100),
            "Resistance" : random.randint(0, 100),
            "Science" : random.randint(0, 100),
            "Magic" : random.randint(0, 100),
            "Frequency" : random.randint(0, 100),
            "Max Movement Points" : random.randint(0, 100),
            "Max Turn Points" : random.randint(0, 100),
        }
        randomStats["Life Points"] = randomStats["Max Life Points"]
        randomStats["Movement Points"] = randomStats["Max Movement Points"]
        randomStats["Turn Points"] = randomStats["Max Turn Points"]
        items = [] # TODO
        randomPolicy = [] # TODO
        return cls(randomStats, items, randomPolicy)
