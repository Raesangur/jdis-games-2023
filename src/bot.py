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

        self.mode = "Building"
        self.direction = "up"

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
            return closestTrail

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

        def check_if_about_to_be_killed(player, players):
            for p in players.values():
                if p.name == "Bon_Matin_2.0":
                    continue
                for t in player.trail:
                    if abs(p.pos[0] - t[0]) + abs(p.pos[1] - t[1]) == 1:
                        regionPoint = list(player.region)[0]
                        print("Avoiding death")
                        return Action(Teleport(regionPoint[0], regionPoint[1]))

            return None

        def check_if_enemy_in_region(player, players):
            for p in players.values():
                if p.name == "Bon_Matin_2.0":
                    continue

                for t in p.trail:
                    for r in player.region:
                        if t[0] == r[0] and t[1] == r[1]:
                            if (t[0], t[1] + 1) in player.region:
                                print("Instakilling " + p.name + " (going up)")
                                self.mode = "InstaKill Up"
                                return Action(Teleport(t[0], t[1] + 1))
                            elif (t[0], t[1] - 1) in player.region:
                                print("Instakilling " + p.name + " (going down)")
                                self.mode = "InstaKill Down"
                                return Action(Teleport(t[0], t[1] - 1))
            return None
            

        def will_it_suicide(player, action):
            if action == Action(Direction.UP):
                nextX = player.pos[0]
                nextY = player.pos[1] - 1
            elif action == Action(Direction.DOWN):
                nextX = player.pos[0]
                nextY = player.pos[1] + 1
            elif action == Action(Direction.LEFT):
                nextX = player.pos[0] - 1
                nextY = player.pos[1]
            else:
                nextX = player.pos[0] + 1
                nextY = player.pos[1]

            if (nextX, nextY) in player.trail:
                regionPoint = list(player.region)[0]
                print("Avoiding suicide")
                return Action(Teleport(regionPoint[0], regionPoint[1]))
            else:
                return action

        def make_square_region(player):
            self.direction = 'right'
            totCount = 39
    
            if self.direction == 'up':
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
    
            elif self.direction == 'right':
                if player.alive % totCount < 7:
                    return Action(Direction.RIGHT)
                elif player.alive % totCount < 17:
                    return Action(Direction.DOWN)
                elif player.alive % totCount < 24:
                    return Action(Direction.LEFT)
                elif player.alive % totCount < 34:
                    return Action(Direction.UP)
                elif player.alive % totCount < 40:
                    return Action(Direction.RIGHT)
                else:
                    return Action(Direction.DOWN)
    
            elif self.direction == 'left':
                if player.alive % totCount < 7:
                    return Action(Direction.LEFT)
                elif player.alive % totCount < 17:
                    return Action(Direction.DOWN)
                elif player.alive % totCount < 24:
                    return Action(Direction.RIGHT)
                elif player.alive % totCount < 34:
                    return Action(Direction.UP)
                elif player.alive % totCount < 40:
                    return Action(Direction.LEFT)
                else:
                    return Action(Direction.DOWN)
    
    
            else:
                if player.alive % totCount < 7:
                    return Action(Direction.DOWN)
                elif player.alive % totCount < 17:
                    return Action(Direction.RIGHT)
                elif player.alive % totCount < 24:
                    return Action(Direction.UP)
                elif player.alive % totCount < 34:
                    return Action(Direction.LEFT)
                elif player.alive % totCount < 40:
                    return Action(Direction.DOWN)
                else:
                    return Action(Direction.DOWN)
        
        if self.__first_turn:
            self.__first_turn = False
            return Action(Pattern([Direction.RIGHT, Direction.RIGHT, Direction.RIGHT, Direction.DOWN, Direction.DOWN, Direction.LEFT, Direction.LEFT, Direction.UP, Direction.UP]))
        player = state.players["Bon_Matin_2.0"]

        x = player.pos[0]
        y = player.pos[1]

        # Avoiding death if in danger
        avoidance = check_if_about_to_be_killed(player, state.players)
        if avoidance is not None:
            return avoidance

        # Mode after InstaKill
        if self.mode == "InstaKill Up":
            print("Killing Up")
            self.mode = "Building"
            return Action(Direction.UP)
        elif self.mode == "InstaKill Down":
            print("Killing Down")
            self.mode = "Building"
            return Action(Direction.Down)

        # Killing an enemy trying to take our region
        instaKill = check_if_enemy_in_region(player, state.players)
        if instaKill is not None:
            return instaKill

        # Resetting if just died
        if player.alive == 0:
            print("Restarting")
            self.mode = "Building"

        # Changing to kill mode on map edge
        

        # Checking mode
        action = Action(Pattern([]))
        if self.mode == "Building":
            action = make_square_region(player)
                
            if len(player.region) > 100:
                self.mode = "Killing"
        else:
            targetPosition = get_closest_trail(state.players, player)
            action = get_direction_from_delta(x - targetPosition[0], y - targetPosition[1])

        return will_it_suicide(player, action)
        
