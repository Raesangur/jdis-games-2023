import random
from core.action import Action, Direction, Pattern, Teleport
from core.game_state import GameState

class BotMatin:
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

        self.defaultMode = "Building"
        self.defaultDirection = "up"
        self.mode = self.defaultMode
        self.direction = self.defaultDirection

        self.ignoreList = [self.__name] #, "Talgarr", "C3P0", "VK", "Jacques Cartier", "Stonks"]


        self.defaultBuildThreshold = 60
        self.defaultKillThreshold = 50
        self.defaultLowerKillThreshold = 5
        self.buildThreshold = self.defaultBuildThreshold
        self.killThreshold = self.defaultKillThreshold
        self.lowerKillThreshold = self.defaultLowerKillThreshold

        self.ticks = -1

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

        def make_square_region(player):
            totCount = 14

            def find_direction():
                # 1200x1200
                if player.pos[0] == 0:
                    return 'up'
                elif player.pos[1] == 0:
                    return 'right'
                elif player.pos[0] == 119:
                    return 'down'
                elif player.pos[1] == 119:
                    return 'left'
                else:
                    return self.direction

            self.direction = find_direction()
    
            if self.direction == 'up':
                if self.ticks % totCount < 3:
                    return Action(Direction.UP)
                elif self.ticks % totCount < 6:
                    return Action(Direction.RIGHT)
                elif self.ticks % totCount < 9:
                    return Action(Direction.DOWN)
                elif self.ticks % totCount < 12:
                    return Action(Direction.LEFT)
                elif self.ticks % totCount < 15:
                    return Action(Direction.UP)
                else:
                    return Action(Direction.DOWN)
    
            elif self.direction == 'right':
                if self.ticks % totCount < 3:
                    return Action(Direction.RIGHT)
                elif self.ticks % totCount < 6:
                    return Action(Direction.DOWN)
                elif self.ticks % totCount < 9:
                    return Action(Direction.LEFT)
                elif self.ticks % totCount < 12:
                    return Action(Direction.UP)
                elif self.ticks % totCount < 15:
                    return Action(Direction.RIGHT)
                else:
                    return Action(Direction.DOWN)
    
            elif self.direction == 'left':
                if self.ticks % totCount < 3:
                    return Action(Direction.LEFT)
                elif self.ticks % totCount < 6:
                    return Action(Direction.DOWN)
                elif self.ticks % totCount < 9:
                    return Action(Direction.RIGHT)
                elif self.ticks % totCount < 12:
                    return Action(Direction.UP)
                elif self.ticks % totCount < 15:
                    return Action(Direction.LEFT)
                else:
                    return Action(Direction.DOWN)
    
    
            else:
                if self.ticks % totCount < 3:
                    return Action(Direction.DOWN)
                elif self.ticks % totCount < 6:
                    return Action(Direction.RIGHT)
                elif self.ticks % totCount < 9:
                    return Action(Direction.UP)
                elif self.ticks % totCount < 12:
                    return Action(Direction.LEFT)
                elif self.ticks % totCount < 15:
                    return Action(Direction.DOWN)
                else:
                    return Action(Direction.DOWN)
            


        def get_closest_trail_to_player(player):
            x = player.pos[0]
            y = player.pos[1]

            for t in player.trail:
                delta = abs(t[0] - x) + abs(t[1] - y)
                if delta == 1:
                    return t
            return (x, y)


        def get_closest_player(player, players):
            currentPosX = player.pos[0]
            currentPosY = player.pos[1]

            closestP = None
            closestSum = 10000
            for p in players.values():
                if p.name in self.ignoreList:
                    continue

                deltaX = abs(p.pos[0] - currentPosX)
                deltaY = abs(p.pos[1] - currentPosY)
                if deltaX + deltaX < closestSum:
                    closestSum = deltaX + deltaY
                    closestP = p
                
            print(str(currentPosX) + " " + str(currentPosY))
            print(closestP.name + " " + str(closestP.pos[0]) + " " + str(closestP.pos[1]) + " " + str(get_closest_trail_to_player(closestP)))

            return currentPosX - closestP.pos[0], currentPosY - closestP.pos[1]


        def get_closest_trail(players, player):
            x = player.pos[0]
            y = player.pos[1]
            closestTrail = None
            closestSum = 10000
            for p in players.values():
                if p.name in self.ignoreList:
                    continue

                for t in p.trail:
                    dx = abs(t[0] - x)
                    dy = abs(t[1] - y)
                    if dx + dy < closestSum:
                        closestTrail = t
                        closestSum = dx + dy
            return closestTrail, closestSum


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

        def teleport_home(player):
            regionPoint = list(player.region)[0]
            return Action(Teleport(regionPoint[0], regionPoint[1]))

        def check_if_about_to_be_killed(player, players):
            for p in players.values():
                if p.name in self.ignoreList:
                    continue
                for t in player.trail:
                    if abs(p.pos[0] - t[0]) + abs(p.pos[1] - t[1]) <= 2:
                        print("Avoiding death")
                        return teleport_home(player)

            return None

        def check_if_enemy_in_region(player, players):
            for p in players.values():
                if p.name in self.ignoreList:
                    continue

                for t in p.trail:
                    for r in player.region:
                        if t[0] == r[0] and t[1] == r[1]:
                            print("Instakill Target: " + t[0] + " " + t[1])
                            if (t[0], t[1] + 1) in player.region and (t[0], t[1] + 1) not in t:
                                print("Instakilling " + p.name + " (going up)")
                                self.mode = "InstaKill Up"
                                return Action(Teleport(t[0], t[1] + 1))
                            elif (t[0], t[1] - 1) in player.region and (t[0], t[1] - 1) not in t:
                                print("Instakilling " + p.name + " (going down)")
                                self.mode = "InstaKill Down"
                                return Action(Teleport(t[0], t[1] - 1))
                            elif (t[0 - 1], t[1]) in player.region and (t[0 - 1], t[1]) not in t:
                                print("Instakilling " + p.name + " (going right)")
                                self.mode = "InstaKill Right"
                                return Action(Teleport(t[0] - 1, t[1]))
                            elif (t[0 + 1], t[1]) in player.region and (t[0 + 1], t[1]) not in t:
                                print("Instakilling " + p.name + " (going left)")
                                self.mode = "InstaKill Left"
                                return Action(Teleport(t[0] + 1, t[1]))
            return None


        def handle_instakill(player, players):
            if self.mode == "InstaKill Up":
                print("Killing Up (" + x + " " + y + ")")
                return Action(Direction.UP)
            elif self.mode == "InstaKill Down":
                print("Killing Down (" + x + " " + y + ")")
                return Action(Direction.DOWN)
            elif self.mode == "InstaKill Right":
                print("Killing Right ("  + x + " " + y + ")")
                return Action(Direction.RIGHT)
            elif self.mode == "InstaKill Left":
                print("Killing Left (" + x + " " + y + ")")
                return Action(Direction.LEFT)
            else:
                return check_if_enemy_in_region(player, players)


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
                self.ticks = 0
                return Action(Teleport(regionPoint[0], regionPoint[1]))
            else:
                return action

        def find_upper_left_corner(player):
            x = 2000
            y = 2000

            # trouver tile la plus haute
            for tile in player.region:
                tile_y = tile[1]

                if tile_y < y:
                    y = tile_y

            # trouver la tile en haut à gauche
            for tile in player.region:
                tile_x = tile[0]
                tile_y = tile[1]

                if tile_y == y:
                    if tile_x < x:
                        x = tile_x

            return (x, y)


        ###########################################################################################
        if self.__first_turn:
            self.__first_turn = False
            return Action(Pattern([Direction.RIGHT, Direction.RIGHT, Direction.DOWN, Direction.DOWN, Direction.LEFT, Direction.UP, Direction.UP]))

        player = state.players[self.__name]
        x = player.pos[0]
        y = player.pos[1]
        self.ticks += 1

        # Avoiding death if in danger
        avoidance = check_if_about_to_be_killed(player, state.players)
        if avoidance is not None:
            self.ticks = -1
            return avoidance

        if self.mode != "Building" and self.mode != "Killing":
            print(self.mode)

        # Mode after InstaKill
        #instaKill = handle_instakill(player, state.players)
        #if instaKill is not None:
        #    self.ticks = -1
        #    self.mode = self.defaultMode
        #    return instaKill
            

        # Resetting if just died
        if player.alive == 0:
            print("Restarting")
            self.mode = self.defaultMode
            self.direction = self.defaultDirection
            self.buildThreshold = self.defaultBuildThreshold
            self.killThreshold = self.defaultKillThreshold
            self.ticks = -1


        # Checking mode
        action = Action(Pattern([]))
        if self.mode == "Building":
            action = make_square_region(player)

            _, distance = get_closest_trail(state.players, player)
            if distance < self.lowerKillThreshold:
                print("Enemy close enough, switching to Kill Mode")
                self.mode = "Killing"
                
            if len(player.region) > self.buildThreshold:
                print("Region big enough, switching to Kill Mode")
                self.mode = "Killing"
        else:
            targetPosition, distance = get_closest_trail(state.players, player)
            if distance > self.killThreshold:
                action = teleport_home(player)
                self.mode = self.defaultMode
                self.buildThreshold += self.defaultBuildThreshold
                self.ticks = -1
            else:
                action = get_direction_from_delta(x - targetPosition[0], y - targetPosition[1])


        return will_it_suicide(player, action)
        
