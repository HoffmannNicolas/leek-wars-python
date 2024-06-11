
from .effect import Effect
import random


class Effect_Over_Time():

    """ Effect that lasts several turns, such as poison, buff or debuff.
    These effects are re-applied at the beginning of the turn """

    def __init__(self, type, value, turns):
        self.type = type
        self.value = value
        self.turns = turns


    def __str__(self):
        toPrint = ""
        toPrint += f"[Effect over time] :: Type={self.type} :: Value={self.value} :: Turns={self.turns}"
        return toPrint


    @classmethod
    def sample(cls):
        type = random.choice(Effect.EFFECTS)
        value = random.uniform(0, 100)
        turns = random.randint(1, 10)
        return cls(type, value, turns)


if (__name__ == "__main__"):
    effect_over_time = Effect_Over_Time.sample()
    print(effect_over_time)
