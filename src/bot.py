import random
from core.action import Action, Direction, Pattern, Teleport
from core.game_state import GameState

class MyBot:
    """
    (fr)
    Cette classe représente votre bot. Vous pouvez y définir des attributs et des méthodes qui 
    seront conservés entre chaque appel de la méthode `tick`.

    (en)
    This class represents your bot. You can define attributes and methods in it that will be kept 
    between each call of the `tick` method.
    """
    def __init__(self):
        self.__name = "Bon_Matin_2.0"
        self.__first_turn = True

        self.turnCount = 0
        

    def __random_action(self) -> Action:
        return random.choice(list(Direction))


    def tick(self, state: GameState) -> Action:    
        """
        (fr)
        Cette méthode est appelée à chaque tick de jeu. Vous pouvez y définir le comportement de
        votre bot. Elle doit retourner une instance de `Action` qui sera exécutée par le serveur.

        (en)
        This method is called every game tick. You can define the behavior of your bot. It must 
        return an instance of `Action` which will be executed by the server.

        Args:
            state (GameState):  (fr) L'état du jeu.
                                (en) The state of the game.
        """

        def get_closest_trail_to_player(player):
            x = player.pos[0]
            y = player.pos[1]

            for t in player.trail:
                delta = abs(t[0] - x) + abs(t[1] - y)
                if delta == 1:
                    return t
            return (x, y)

        def get_closest_player(players, player):
            currentPosX = player.pos[0]
            currentPosY = player.pos[1]

            closestP = None
            closestSum = 10000
            for p in players.values():
                if p.name == "Bon_Matin_2.0":
                    continue

                deltaX = abs(p.pos[0] - currentPosX)
                deltaY = abs(p.pos[1] - currentPosY)
                if deltaX + deltaX < closestSum:
                    closestSum = deltaX + deltaY
                    closestP = p
                
            print(str(currentPosX) + " " + str(currentPosY))
            print(closestP.name + " " + str(closestP.pos[0]) + " " + str(closestP.pos[1]) + " " + str(get_closest_trail_to_player(closestP)))

            return get_direction_from_delta(currentPosX - closestP.pos[0], currentPosY - closestP.pos[1])

        def get_closest_trail(players, player):
            x = player.pos[0]
            y = player.pos[1]
            closestTrail = None
            closestSum = 10000
            for p in players.values():
                if p.name == "Bon_Matin_2.0":
                    continue

                for t in p.trail:
                    dx = abs(t[0] - x)
                    dy = abs(t[1] - y)
                    if dx + dy < closestSum:
                        closestTrail = t
                        closestSum = dx + dy
            return get_direction_from_delta(x - closestTrail[0], y - closestTrail[1])

        def get_direction_from_delta(deltaX, deltaY) -> Action:
            if abs(deltaX) > abs(deltaY):
                if deltaX > 0:
                    return Action(Direction.LEFT)
                else:
                    return Action(Direction.RIGHT)
            else:
                if deltaY > 0:
                    return Action(Direction.UP)
                else:
                    return Action(Direction.DOWN)
                

        
        if self.__first_turn:
            self.__first_turn = False
            return Action(Pattern([Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.DOWN, Direction.DOWN, Direction.LEFT, Direction.LEFT, Direction.UP, Direction.UP]))

        player = state.players["Bon_Matin_2.0"]

        direction = 'up'
        totCount = 39

        if direction == 'up':
            if player.alive % totCount < 7:
                return Action(Direction.UP)
            elif player.alive % totCount < 17:
                return Action(Direction.RIGHT)
            elif player.alive % totCount < 24:
                return Action(Direction.DOWN)
            elif player.alive % totCount < 34:
                return Action(Direction.LEFT)
            elif player.alive % totCount < 40:
                return Action(Direction.UP)
            else:
                return Action(Direction.DOWN)




        elif direction < 'right':
            return Action(Direction.RIGHT)
        elif direction >= 'left':
            return Action(Direction.RIGHT)
        else:
            return Action(Direction.RIGHT)