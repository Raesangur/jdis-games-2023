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
        if self.__first_turn:
            self.__first_turn = False
            return Action(Pattern([Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.LEFT, Direction.UP]))

        player = state.players["Bon_Matin_2.0"]
        print(player)
        self.turnCount = player.alive
        
        if self.turnCount < 5:
            return Action(Direction.LEFT)
        elif self.turnCount == 5:
            return Action(Direction.UP)
        elif self.turnCount < 10 and self.turnCount > 5:
            return Action(Direction.RIGHT)
        elif self.turnCount == 10:
            return Action(Direction.DOWN)

        else:
            return self.__random_action()
