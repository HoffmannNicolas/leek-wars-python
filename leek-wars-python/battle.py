
from .terrain import Terrain
from .entity.leek import Leek
from .entity.turret import Turret
from .entity.chest import Chest
import random


class Battle:

    """ Battle environment that contains everything about a fight """

    GAMEMODE_SOLO = 0
    GAMEMODE_BATTLE_ROYALE = 1
    GAMEMODE_FARMER = 2
    GAMEMODE_TEAM = 3

    def __init__(self, terrain, entities):
        self.terrain = terrain
        self.entities = entities


    def getState(self):
        """ Compute the raw state of the Battle.
        Pre-processing and accomodation can be performed to simplify learning, but not here. """
        return 42.666 # TODO


    def fightIsOver(self) -> bool:
        """ Return True iif the fight is over """
        return True # TODO


    def entityUseItemOnCell(self, entity, item, cell):
        for effect in item:
            self.entityApplyEffectOnCell(entity, effect, cell)


    def entityApplyEffectOnCell(self, entity, effect, cell):
        value = 42 # TODO
        affected_entities = [] # TODO
        for entity in affected_entities:
            entity.applyEffect(effect, value)


    def carryOutAtomicAction(self, action, player) -> bool:
        """ Modify the entities according to the <action> performed by the <player> """
        # TODO
        return self._fightIsOver()


    def conductPlayerTurn(self, player) -> bool:
        """ Performs the turn of the <player> """
        turnEnded = False
        while(not(turnEnded)) :
            state = self.getState()
            action = player.policy(state)
            turnEnded = self.carryOutAtomicAction(action)


    def run(self):
        while not(self.fightIsOver()):
            player = self.getPlayer()
            self.runPlayerTurn(player)


    def __str__(self):
        toPrint = ""
        toPrint += f"[Battle]\n"
        toPrint += str(self.terrain) + '\n'
        for entity in self.entities:
            toPrint += str(entity)
        return toPrint


    @classmethod
    def sample(cls, map_width=17, map_height=17, obstacle_proportion=0.15, gamemode=None, chest_probability=0.01):
        terrain = Terrain.sample(width=map_width, height=map_height, obstacle_proportion=obstacle_proportion)
        if (gamemode is None):
            gamemode = random.choice([Battle.GAMEMODE_SOLO, Battle.GAMEMODE_TEAM, Battle.GAMEMODE_FARMER, Battle.GAMEMODE_BATTLE_ROYALE])

        def _placeEntityRandomly(entity, terrain, otherEntities):
            while True: # TODO : Fix this possibly infinite loop (if map is not big enough)
                x = random.randint(0, terrain.width)
                y = random.randint(0, terrain.height)
                if (terrain.cell_is_not_free(x, y)): # Sampled cell contains an obstacle
                    continue
                for otherEntity in otherEntities: # Sample cell contains another entity already
                    if (x == otherEntity.current_x_coordinate and y == otherEntity.current_y_coordinate):
                        pass
                entity.current_x_coordinate = x
                entity.current_y_coordinate = y
                return

        def _addSampledEntity(team, cls):
            entity = cls.sample()
            entity.current_team = team
            _placeEntityRandomly(entity, terrain, entities)
            entities.append(entity)

        entities = []
        if (gamemode == Battle.GAMEMODE_SOLO):
            _addSampledEntity(0, Leek)
            _addSampledEntity(1, Leek)

        elif (gamemode == Battle.GAMEMODE_TEAM):
            for i_leek in range(6):
                _addSampledEntity(0, Leek)
                _addSampledEntity(1, Leek)
            _addSampledEntity(0, Turret)
            _addSampledEntity(1, Turret)

        elif (gamemode == Battle.GAMEMODE_FARMER):
            for i_leek in range(4):
                _addSampledEntity(0, Leek)
                _addSampledEntity(1, Leek)

        elif (gamemode == Battle.GAMEMODE_BATTLE_ROYALE):
            for i_leek in range(10):
                _addSampledEntity(i_leek, Leek)

        else:
            print("ERROR : Unrecognized gamemode")
            exit() # TODO : Raise proper error instead

        if (random.random() < chest_probability):
            _addSampledEntity(-1, Chest)

        return cls(terrain, entities)



if (__name__ == "__main__"):
    battle = Battle.sample()
    print(battle)
