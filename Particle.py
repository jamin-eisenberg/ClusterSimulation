import pygame.draw
from pygame import gfxdraw

from constants import (
    COLOR_NUMBER_LOOKUP_ROW_LENGTH,
    COLOR_INTERACTIONS_ROW_LENGTH,
)


def draw_circle(surface, x, y, radius, color):
    x, y = int(x), int(y)
    gfxdraw.aacircle(surface, x, y, radius, color)
    gfxdraw.filled_circle(surface, x, y, radius, color)


class Particle:
    def __init__(self, pos, color):
        self.pos = pos
        self.vel = (0, 0)
        self.color = color

    def update(self, w, h, friction_coefficient):
        self.pos = ((self.pos[0] + self.vel[0]) % w, (self.pos[1] + self.vel[1]) % h)
        self.vel = (
            self.vel[0] * friction_coefficient,
            self.vel[1] * friction_coefficient,
        )

    def interact(self, other, interaction_radius, color_interactions):
        dist_sq = (other.pos[0] - self.pos[0]) ** 2 + (other.pos[1] - self.pos[1]) ** 2
        if dist_sq < (interaction_radius**2):
            force_dir = (other.pos[0] - self.pos[0], other.pos[1] - self.pos[1])
            force_mod = color_interactions[
                self.color * COLOR_INTERACTIONS_ROW_LENGTH + other.color
            ] / 10000
            force = (force_dir[0] * force_mod, force_dir[1] * force_mod)
            self.vel = (self.vel[0] + force[0], self.vel[1] + force[1])

    def draw(self, surface, color_number_lookup, particle_radius):
        color = color_number_lookup[
            self.color
            * COLOR_NUMBER_LOOKUP_ROW_LENGTH : self.color
            * COLOR_NUMBER_LOOKUP_ROW_LENGTH
            + 3
        ]
        draw_circle(surface, *self.pos, particle_radius, color)
