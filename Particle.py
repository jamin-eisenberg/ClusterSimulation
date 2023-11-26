import pygame.draw

PARTICLE_RADIUS = 10
INTERACTION_RADIUS = 100
FRICTION_COEFFICIENT = 0.97
COLOR_NUMBER_LOOKUP = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)]
COLOR_INTERACTIONS = [[-0.01, 0.01], [0.01, -0.01]]


class Particle:
    def __init__(self, pos, color):
        self.pos = pos
        self.vel = (0, 0)
        self.color = color

    def update(self, w, h):
        self.pos = ((self.pos[0] + self.vel[0]) % w, (self.pos[1] + self.vel[1]) % h)
        self.vel = (self.vel[0] * FRICTION_COEFFICIENT, self.vel[1] * FRICTION_COEFFICIENT)

    def interact(self, other):
        dist_sq = (other.pos[0] - self.pos[0]) ** 2 + (other.pos[1] - self.pos[1]) ** 2
        if dist_sq < (INTERACTION_RADIUS ** 2):
            force_dir = (other.pos[0] - self.pos[0], other.pos[1] - self.pos[1])
            force_mod = COLOR_INTERACTIONS[self.color][other.color]
            force = (force_dir[0] * force_mod, force_dir[1] * force_mod)
            self.vel = (self.vel[0] + force[0], self.vel[1] + force[1])

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_NUMBER_LOOKUP[self.color], self.pos, PARTICLE_RADIUS)