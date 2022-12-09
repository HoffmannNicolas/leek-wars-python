
from abc import ABC
import random

class Entity(ABC):

    """ Abstract mother class of all entities: Leeks, Bulbs, Turrets and chests """

    # Names of entities
    LEEK = 0
    BULB = 1
    TURRET = 2
    CHEST = 3

    def __init__(self, staticStats, dynamicStats, items, policy):
        self.staticStats = staticStats # Stats of the leek outside combat
        self.dynamicStats = dynamicStats # Stats that change in combat
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


    def applyEffect(self, effect, value):
        if (effect == Effect.EFFECT_DAMAGE):
            effective_relative_shield_percent = min(100, self.relative_shield_percent)
            relative_shield_multiplier = 1 - effective_relative_shield_percent / 100
            effectiveDammage = int(value * relative_shield_percent - self.absolute_shield)
            effectiveDammage = max(0, effectiveDammage) # Negative damage does not heal entity
            self.hp -= effectiveDammage
            self.hp = max(0, self.hp) # HP cannot be negative
        # TODO: Implement impact of every effect on entity


    def __str__(self):
        toPrint = ""
        if (self.type == Entity.LEEK): toPrint += f"[Leek]"
        if (self.type == Entity.BULB): toPrint += f"[Bulb]"
        if (self.type == Entity.TURRET): toPrint += f"[Turret]"
        if (self.type == Entity.CHEST): toPrint += f"[Chest]"
        toPrint += "\n"
        toPrint += f"\t-Items: {self.items}\n"
        for (stat_name, stat_value) in self.staticStats.items():
            toPrint += f"\t-{stat_name}: {stat_value}\n"
        for (stat_name, stat_value) in self.dynamicStats.items():
            toPrint += f"\t-{stat_name}: {stat_value}\n"
        return toPrint


    @classmethod
    def sample(cls):

        """ Sample a random <Entity>.
        Although this very class cannot be instanciated, all children can be randomly sampled the same way."""

        randomStaticStats = {
            "Max Life Points": random.randint(0, 100),
            "Strength": random.randint(0, 100),
            "Wisdom": random.randint(0, 100),
            "Agility": random.randint(0, 100),
            "Resistance": random.randint(0, 100),
            "Science": random.randint(0, 100),
            "Magic": random.randint(0, 100),
            "Frequency": random.randint(0, 100),
            "Max Movement Points": random.randint(0, 100),
            "Max Turn Points": random.randint(0, 100),
        }

        randomDynamicStats = {
            "Relative Shield": 0,
            "Absolute Shield": 0,
            "Poison": 0,
            "Weakness": 0,
            "Life Points": randomStaticStats["Max Life Points"],
            "Movement Points": randomStaticStats["Max Movement Points"],
            "Turn Points": randomStaticStats["Max Turn Points"]
        }

        items = [] # TODO
        randomPolicy = [] # TODO
        return cls(randomStaticStats, randomDynamicStats, items, randomPolicy)
