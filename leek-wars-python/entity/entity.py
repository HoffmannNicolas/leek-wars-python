
from abc import ABC
import random

class Entity(ABC):

    """ Abstract mother class of all entities: Leeks, Bulbs, Turrets and chests """

    # Names of entities
    LEEK = 0
    BULB = 1
    TURRET = 2
    CHEST = 3

    def __init__(self, base_stats, dynamic_stats, items, policy):
        for (stat_name, stat_value) in base_stats.items():
            self.__dict__[stat_name] = stat_value
        for (stat_name, stat_value) in dynamic_stats.items():
            self.__dict__[stat_name] = stat_value
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
        for stat_name in self.__dict__.keys():
            if ("base_" in stat_name or "current_" in stat_name):
                toPrint += f"\t-{stat_name}: {self.__dict__[stat_name]}\n"
        return toPrint


    @classmethod
    def sample(cls):

        """ Sample a random <Entity>.
        Although this very class cannot be instanciated, all children can be randomly sampled the same way."""

        random_base_stats = {
            "base_max_health_points": random.randint(0, 100),
            "base_strength": random.randint(0, 100),
            "base_wisdom": random.randint(0, 100),
            "base_agility": random.randint(0, 100),
            "base_resistance": random.randint(0, 100),
            "base_science": random.randint(0, 100),
            "base_magic": random.randint(0, 100),
            "base_frequency": random.randint(0, 100),
            "base_max_movement_points": random.randint(0, 100),
            "base_max_turn_points": random.randint(0, 100)
        }

        random_dynamic_stats = {
            "current_relative_shield": 0,
            "current_absolute_shield": 0,
            "current_poison": 0,
            "current_weakness": 0,
            "current_health_points": random_base_stats["base_max_health_points"],
            "current_movement_Points": random_base_stats["base_max_movement_points"],
            "current_turn_points": random_base_stats["base_max_turn_points"],
            "current_team": random.randint(0, 10),
            "current_x_coordinate": random.randint(0, 17),
            "current_y_cordinate": random.randint(0, 17),
            "current_max_health_points": random_base_stats["base_max_health_points"],
            "current_strength": random_base_stats["base_strength"],
            "current_wisdom": random_base_stats["base_wisdom"],
            "current_agility": random_base_stats["base_agility"],
            "current_resistance": random_base_stats["base_resistance"],
            "current_science": random_base_stats["base_science"],
            "current_magic": random_base_stats["base_magic"],
            "current_frequency": random_base_stats["base_frequency"],
            "current_max_movement_points": random_base_stats["base_max_movement_points"],
            "current_max_turn_points": random_base_stats["base_max_turn_points"],
        }

        items = [] # TODO
        randomPolicy = [] # TODO
        return cls(random_base_stats, random_dynamic_stats, items, randomPolicy)
