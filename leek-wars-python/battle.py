
from .terrain import Terrain
from .entity.leek import Leek
from .entity.turret import Turret
from .entity.chest import Chest
import random
from copy import copy


class Battle:

    """ Battle environment that contains everything about a fight """

    GAMEMODE_SOLO = 0
    GAMEMODE_BATTLE_ROYALE = 1
    GAMEMODE_FARMER = 2
    GAMEMODE_TEAM = 3

    def __init__(self, terrain, entities, max_turns=64):
        self.terrain = terrain
        self.entities = entities
        self.max_turns = max_turns
        self.current_turn = 0
        self.play_order = self.compute_play_order()
        self.play_order[0].start_turn() # At the beginning of the battle, let the first player initiate it's turn


    def compute_play_order(self, verbose=True):
        """ The order in which entities play """
        all_remaining_teams = [entity.current_team for entity in self.entities]
        all_remaining_teams = list(set(all_remaining_teams)) # Remove duplicates
        entities_to_place = copy(self.entities)
        entities_to_place.sort(key=lambda entity:entity.current_frequency)
        teams_to_play = copy(all_remaining_teams)
        play_order = []
        while (len(entities_to_place) > 0):
            for i_entity in range(len(entities_to_place), 0, -1):
                i_entity -= 1
                if (entities_to_place[i_entity].current_team in teams_to_play):
                    break
            play_order.append(entities_to_place[i_entity])
            placed_entity_team = play_order[-1].current_team
            entities_to_place.pop(i_entity)

            # Remove team if no other entities of the team remain
            teams_left = [entity.current_team for entity in entities_to_place]
            if not(placed_entity_team in teams_left):
                all_remaining_teams.remove(placed_entity_team)

            teams_to_play.remove(placed_entity_team)
            if(len(teams_to_play) == 0): # Once an entity from each team is placed in the play order, re-allow them all to be chosena gain
                teams_to_play = copy(all_remaining_teams) # TODO : Teams_to_play shoudl round robin instead of flat allowing all teams to be chosen again. currently, it might (and does sometimes) reselect the same team twice in a row.

        if (verbose):
            for entity in play_order:
                print("freq : ", entity.current_frequency, "   team : ", entity.current_team)

        return play_order


    def battle_is_over(self) -> bool:
        """ Return True iif the fight is over """
        return True # TODO


    def play_effect_on_cell(self, entity, effect, cell):
        """ Simulate <player> using <effect> on <cell> """
        value = 42 # TODO
        affected_entities = [] # TODO
        for entity in affected_entities:
            entity.applyEffect(effect, value)


    def play_item_on_cell(self, entity, item, cell):
        """ Simulate <entity> using <item> on <cell> """
        for effect in item.effects:
            self.play_effect_on_cell(entity, effect, cell)


    def play_action(self, action, entity):
        """ Simulate <entity> using <action> """
        turn_is_over = False
        # TODO
        return turn_is_over


    def play_turn(self):
        """ Play the turn of the current player """

        if (self.battle_is_over()):
            return # No turn to simulate if the battle is over

        player = self.play_order[0] # Get player
        turnEnded = False
        while(not(turnEnded)) :
            state = [self.terrain, self.entities, self.play_order]
            action = player.policy(state)
            turnEnded = self.play_action(action)

        player.end_turn() # End player's turn

            # Change the player
        self.play_order = self.play_order[1:]
        self.play_order.append(player)

        self.play_order[0].start_turn() # Start next player's turn


    def play_entire_battle(self):
        """ Keep playing individual turns until the battle is over """
        while not(self.battle_is_over()):
            self.play_turn()


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
