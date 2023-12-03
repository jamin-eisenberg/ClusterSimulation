import threading


PARTICLE_RADIUS_INDEX = 0
INTERACTION_RADIUS_INDEX = 1
FRICTION_COEFFICIENT_INDEX = 2
DISTANCE_INDEX = 3
COLOR_NUMBER_LOOKUP_START_INDEX = 4
COLOR_NUMBER_LOOKUP_ROW_LENGTH = 3
COLOR_INTERACTIONS_START_INDEX = 16
COLOR_INTERACTIONS_ROW_LENGTH = 4


def slice_sl(sl, start, end, step=1):
    return sl[start:end:step]


def slice_real_sl(sl, start, end, step=1):
    return [sl[i] for i in range(start, end, step)]


class SharedState:
    def __init__(self):
        self.state = {
            "particle_radius": 5,
            "interaction_radius": 70,
            "friction_coefficient": 0.99,
            "distance": 0,
            "color_number_lookup": [
                (255, 0, 0),
                (0, 255, 0),
                (0, 0, 255),
                (255, 255, 0),
            ],
            "color_interactions": [
                [-0.01, 0.01, 0, 0],
                [0.01, -0.01, 0, 0],
                [-0.01, -0.01, -0.01, -0.01],
                [0.01, 0.01, 0.01, 0.01],
            ],
        }

    def get(self, key):
        return self.state.get(key)

    def set(self, key, value):
        self.state[key] = value
