import threading


class SharedState:
    def __init__(self):
        self.state = {
            "particle_radius": 5,
            "interaction_radius": 70,
            "friction_coefficient": 0.97,
            "color_number_lookup": [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)],
            "color_interactions": [[-0.01, 0.01, 0, 0], [0.01, -0.01, 0, 0], [-0.01, -0.01, -0.01, -0.01], [0.01, 0.01, 0.01, 0.01]]
        }

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value
