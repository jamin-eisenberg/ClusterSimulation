import pygame.draw


class Particle:
    def __init__(self, pos, color, state):
        self.pos = pos
        self.vel = (0, 0)
        self.color = color
        self.state = state

    def update(self, w, h):
        friction_coefficient = self.state.get("friction_coefficient")
        self.pos = ((self.pos[0] + self.vel[0]) % w, (self.pos[1] + self.vel[1]) % h)
        self.vel = (self.vel[0] * friction_coefficient, self.vel[1] * friction_coefficient)

    def interact(self, other):
        interaction_radius = self.state.get("interaction_radius")
        color_interactions = self.state.get("color_interactions")
        dist_sq = (other.pos[0] - self.pos[0]) ** 2 + (other.pos[1] - self.pos[1]) ** 2
        if dist_sq < (interaction_radius ** 2):
            force_dir = (other.pos[0] - self.pos[0], other.pos[1] - self.pos[1])
            force_mod = color_interactions[self.color][other.color]
            force = (force_dir[0] * force_mod, force_dir[1] * force_mod)
            self.vel = (self.vel[0] + force[0], self.vel[1] + force[1])

    def draw(self, surface):
        color_number_lookup = self.state.get("color_number_lookup")
        particle_radius = self.state.get("particle_radius")
        pygame.draw.circle(surface, color_number_lookup[self.color], self.pos, particle_radius)