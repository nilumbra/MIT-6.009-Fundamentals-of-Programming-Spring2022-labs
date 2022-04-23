import pygame


class Vector:
    def __init__(self, *coords):
        self.coords = coords
        self.dimension = len(self.coords)

    def __len__(self):
        # len(x)  ==> x.__len__()
        return self.dimension

    def __abs__(self):
        # abs(x)  ==> x.__abs__()
        return sum(i ** 2 for i in self.coords) ** 0.5

    def normalize(self):
        return self / abs(self)

    def __getitem__(self, ix):
        # x[i]  ==> x.__getitem__(i)
        return self.coords[ix]

    def __iter__(self):
        # for i in x  ==> for i in x.__iter__()
        yield from self.coords

    def __add__(self, other):
        # x + y  ==> x.__add__(y)
        assert len(self) == len(other)
        return Vector(*(i + j for i, j in zip(self, other)))

    def __sub__(self, other):
        # x - y  ==> x.__sub__(y)
        return self + (other * -1)

    def __mul__(self, other):
        # x * y  ==> x.__mul__(y)
        assert isinstance(other, (int, float))
        return Vector(*(i * other for i in self))

    def __truediv__(self, other):
        # x / y  ==> x.__truediv__(y)
        assert isinstance(other, (int, float))
        return self * (1 / other)

    def __repr__(self):
        # Python-readable representation
        # repr(x)  ==>  x.__repr__()
        return f"Vector({', '.join(str(i) for i in self.coords)})"

    def __str__(self):
        # human-readable representation
        # str(x)  ==> x.__str__()
        # print(x)  ==>  print(x.__str__())
        return f"'({' '.join(str(i) for i in self.coords)})"


class Body:
    G = 6.67e-11

    def __init__(self, mass, position, initial_velocity=None):
        self.mass = mass
        self.position = position
        self.velocity = initial_velocity or Vector(0, 0)

    def force_from(self, other):
        delta = other.position - self.position
        dist = abs(delta)
        direction = delta.normalize()
        magnitude = (self.G * self.mass * other.mass) / (dist * dist)
        return direction * magnitude

    def move(self, f, dt):
        acceleration = f / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt


class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies

    def step(self, dt):
        fs = [
            sum((b1.force_from(b2) for b2 in self.bodies if b1 != b2), Vector(0, 0))
            for b1 in self.bodies
        ]

        for b, f in zip(self.bodies, fs):
            b.move(f, dt)


class GraphicalSimulation(Simulation):
    """
    Like the simulation, but also displays things to the screen
    """

    size = 1024
    colors = [
        (255, 0, 0),
        (0, 0, 255),
        (66, 52, 0),
        (152, 152, 152),
        (0, 255, 255),
        (255, 150, 0),
        (255, 0, 255),
    ]

    def __init__(self, bodies, screen_limit):
        Simulation.__init__(self, bodies)
        self.screen_limit = screen_limit
        self.screen = pygame.display.set_mode((self.size, self.size))

    def draw(self):
        self.screen.fill("white")
        for b, c in zip(self.bodies, self.colors):
            x = self.size // 2 + (b.position[0] / self.screen_limit) * self.size // 2
            y = self.size // 2 + (b.position[1] / self.screen_limit) * self.size // 2
            pygame.draw.circle(self.screen, c, (x, y), 10)
        pygame.display.flip()

    def step(self, dt):
        Simulation.step(self, dt)
        self.draw()


if __name__ == "__main__":
    import sys
    import time
    import pygame

    dt = 2000

    ## 2 body, stable orbit...
    sim = GraphicalSimulation(
        [
            Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
        ],
        2e9,
    )

    ## 2 body, more erratic
    # sim = GraphicalSimulation([
    #    Body(1e25, Vector(0,0.91e9), Vector(200, 0)),
    #    Body(1e25, Vector(0,-0.91e9), Vector(-200, 0)),
    # ], 2e9)

    ## 3 body, interesting
    # sim = GraphicalSimulation([
    #    Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
    #    Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
    #    Body(5e8, Vector(0,0), Vector(25, 0)),
    # ], 2e9)

    ## 4 body?  same-ish, but still cool
    # sim = GeaphicalSimulation([
    #    Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
    #    Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
    #    Body(5e8, Vector(50,0), Vector(25, 0)),
    #    Body(5e8, Vector(-50,0), Vector(-25, 0)),
    # ], 2e9)

    ## 7 body?  same-ish, but still cool
    # sim = GraphicalSimulation([
    #    Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
    #    Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
    #    Body(5e8, Vector(1e5,0), Vector(25, 25)),
    #    Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
    #    Body(1e20, Vector(1e8,1e8), Vector(0, 100)),
    #    Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
    #    Body(1e10, Vector(0,0), Vector(0, 0)),
    # ], 2e9)

    ## 7 body, break symmetry
    # sim = GraphicalSimulation([
    #    Body(1e25, Vector(0,0.91e9), Vector(400, 0)),
    #    Body(1e25, Vector(0,-0.91e9), Vector(-400, 0)),
    #    Body(5e8, Vector(1e5,0), Vector(25, 25)),
    #    Body(5e8, Vector(-1e5,0), Vector(-25, -25)),
    #    Body(1e20, Vector(1e8,1e8), Vector(0, 150)),
    #    Body(1e20, Vector(-1e8,-1e8), Vector(0, -100)),
    #    Body(1e10, Vector(0,0), Vector(0, 0)),
    # ], 2e9)

    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        sim.step(dt)