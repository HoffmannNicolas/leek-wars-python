


class Battle:

    """ Battle environment that contains everything about a fight """

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
