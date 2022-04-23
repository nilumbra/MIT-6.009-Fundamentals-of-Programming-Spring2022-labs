class Vector:
    def __init__(self, *coords):
        self.coords = coords
        self.dimension = len(coords)


class Body:
    def __init__(self, mass, position, initial_velocity):
        self.mass = mass
        self.position = position
        self.velocity = initial_velocity


class Simulation:
    def __init__(self, bodies):
        self.bodies = bodies


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

    # 2 body, stable orbit...
    sim = GraphicalSimulation(
        [
            Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
            Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
        ],
        2e9,
    )

    ## 2 body, more erratic
    #sim = GraphicalSimulation(
    #    [
    #        Body(1e25, Vector(0, 0.91e9), Vector(200, 0)),
    #        Body(1e25, Vector(0, -0.91e9), Vector(-200, 0)),
    #    ],
    #    2e9,
    #)

    ## 3 body, interesting
    #sim = GraphicalSimulation(
    #    [
    #        Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
    #        Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
    #        Body(5e8, Vector(0, 0), Vector(25, 0)),
    #    ],
    #    2e9,
    #)

    ## 4 body?  same-ish, but still cool
    #sim = GeaphicalSimulation(
    #    [
    #        Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
    #        Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
    #        Body(5e8, Vector(50, 0), Vector(25, 0)),
    #        Body(5e8, Vector(-50, 0), Vector(-25, 0)),
    #    ],
    #    2e9,
    #)

    ## 7 body?  same-ish, but still cool
    #sim = GraphicalSimulation(
    #    [
    #        Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
    #        Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
    #        Body(5e8, Vector(1e5, 0), Vector(25, 25)),
    #        Body(5e8, Vector(-1e5, 0), Vector(-25, -25)),
    #        Body(1e20, Vector(1e8, 1e8), Vector(0, 100)),
    #        Body(1e20, Vector(-1e8, -1e8), Vector(0, -100)),
    #        Body(1e10, Vector(0, 0), Vector(0, 0)),
    #    ],
    #    2e9,
    #)

    ## 7 body, break symmetry
    #sim = GraphicalSimulation(
    #    [
    #        Body(1e25, Vector(0, 0.91e9), Vector(400, 0)),
    #        Body(1e25, Vector(0, -0.91e9), Vector(-400, 0)),
    #        Body(5e8, Vector(1e5, 0), Vector(25, 25)),
    #        Body(5e8, Vector(-1e5, 0), Vector(-25, -25)),
    #        Body(1e20, Vector(1e8, 1e8), Vector(0, 150)),
    #        Body(1e20, Vector(-1e8, -1e8), Vector(0, -100)),
    #        Body(1e10, Vector(0, 0), Vector(0, 0)),
    #    ],
    #    2e9,
    #)

    pygame.init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
        sim.step(dt)