import random, sys
from game_utils import *


class GameObject:
    def __init__(self, position, symbol, color):
        self.position = position
        self.symbol = symbol
        self.color = color

    def update(self, game):
        pass

    def render(self):
        print_at_location(*self.position, self.symbol, self.color)


class Wall(GameObject):
    pass


class Sock(GameObject):
    color_points = {'blue': 3, 'green': 2, 'red': 1}


class MobileGameObject(GameObject):
    movement_deltas = {
        'UP': (-1, 0),
        'DOWN': (1, 0),
        'LEFT': (0, -1),
        'RIGHT': (0, 1),
        None: (0, 0)
    }
    opposites = {
        'UP': 'DOWN',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT',
        'DOWN': 'UP',
        None: None
    }


class Player(MobileGameObject):
    pass


class Human(Player):
    pass


class Bot(Player):
    pass


fps = 10

class Game:
    def __init__(self, height, width, length=20*30):
        self.height = height
        self.width = width
        self.length = length

        self.all_objects = []
        for r in range(1, height+1):
            self.all_objects.append(Wall((r, 1)))
            self.all_objects.append(Wall((r, width)))
        for c in range(2, width):
            self.all_objects.append(Wall((1, c)))
            self.all_objects.append(Wall((height, c)))

        self.player = Human((height-1, 2), 1)
        self.bot = Bot((2, width-1), 1)

        self.all_objects.append(self.player)
        self.all_objects.append(self.bot)

    def objects_at(self, position, instance_of=object):
        return [thing for thing in self.all_objects
                if thing.position == position
                and isinstance(thing, instance_of)]

    def update(self):
        if random.random() < 0.2:
            r = random.randint(2, self.height-1)
            c = random.randint(2, self.width-1)
            color = random.choice(['red', 'green', 'blue'])
            ttl = random.randint(5, 50)
            self.all_objects.append(Sock((r, c), color, ttl))

        for e in self.all_objects:
            e.update(self)

        self.all_objects = [e for e in self.all_objects if e.alive]

    def render(self, tick):
        clear_screen()
        print_at_location(self.height+1,0,'You: ' + str(self.player.score))
        print_at_location(self.height+2,0,'Bot: ' + str(self.bot.score))
        print_at_location(self.height+3,0,'Time: ' + str(self.length-tick))
        for e in self.all_objects:
            e.render()

    def run(self):
        with keystrokes(sys.stdin) as keyb:
            for i in range(self.length):
                self.keys = keyb.regioned_keys()
                self.update()
                self.render(i)
                time.sleep(1/fps)

        if self.player.score > self.bot.score:
            text = 'A WINNER IS YOU!'
            color = 'green'
        else:
            text = 'YOU ARE NOT WINNER!'
            color = 'red'
        print_at_location(self.height+4,0,text,color)

        input('Press Enter to continue')


if __name__ == '__main__':
    Game(20, 20, 30*fps).run()