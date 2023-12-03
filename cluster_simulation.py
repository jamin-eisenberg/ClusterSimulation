import random
import multiprocessing

# import RPi.GPIO as GPIO TODO gpio
import time
from multiprocessing.managers import SharedMemoryManager

import pygame
from flask import Flask, request

from Particle import Particle
from SpatialHash import SpatialHash
from State import (
    COLOR_INTERACTIONS_START_INDEX,
    COLOR_INTERACTIONS_ROW_LENGTH,
    DISTANCE_INDEX,
    INTERACTION_RADIUS_INDEX,
    slice_sl,
    FRICTION_COEFFICIENT_INDEX,
    COLOR_NUMBER_LOOKUP_START_INDEX,
    COLOR_NUMBER_LOOKUP_ROW_LENGTH,
    PARTICLE_RADIUS_INDEX,
    slice_real_sl,
)

# TODO serve with gunicorn
# TODO ensure server works with sim
# TODO update script to run server

app = Flask(__name__)


INITIAL_STATE = [
    5,  # particle radius
    70,  # interaction radius
    0.97,  # friction
    0,  # distance
    255,  # colors
    0,
    0,
    0,
    255,
    0,
    0,
    0,
    255,
    255,
    255,
    0,
    -0.01,  # interactions
    0.01,
    0,
    0,
    0.01,
    -0.01,
    0,
    0,
    -0.01,
    -0.01,
    -0.01,
    -0.01,
    0.01,
    0.01,
    0.01,
    0.01,
]

# TODO save sim params to file
@app.route("/<color1>/to/<color2>", methods=["PATCH"])
def change_color_relationship(color1, color2):
    sl = app.config["STATE"]
    new_attraction = request.args.get("attraction")
    print(2)
    # curr_interactions = slice_real_sl(
    #     sl,
    #     COLOR_INTERACTIONS_START_INDEX,
    #     COLOR_INTERACTIONS_START_INDEX + COLOR_INTERACTIONS_ROW_LENGTH * 4,
    # )
    sl[
        COLOR_INTERACTIONS_START_INDEX + int(color1) * COLOR_INTERACTIONS_ROW_LENGTH + int(color2)
    ] = float(new_attraction)

    return ""


# TODO concurrent
def read_distance(sl):
    while True:
        time.sleep(1)
        sl[DISTANCE_INDEX] = pygame.key.get_pressed()[pygame.K_SPACE] * 50
        print(pygame.key.get_pressed()[pygame.K_SPACE])


# def read_distance():  TODO gpio
#     try:
#         GPIO.setmode(GPIO.BOARD)
#
#         PIN_TRIGGER = 16
#         PIN_ECHO = 18
#
#         GPIO.setup(PIN_TRIGGER, GPIO.OUT)
#         GPIO.setup(PIN_ECHO, GPIO.IN)
#
#         GPIO.output(PIN_TRIGGER, GPIO.LOW)
#
#         time.sleep(0.2)
#
#         GPIO.output(PIN_TRIGGER, GPIO.HIGH)
#
#         time.sleep(0.00001)
#
#         GPIO.output(PIN_TRIGGER, GPIO.LOW)
#
#         pulse_start_time = time.time()
#         while GPIO.input(PIN_ECHO) == 0:
#             pulse_start_time = time.time()
#
#         pulse_end_time = time.time()
#         while GPIO.input(PIN_ECHO) == 1:
#             pulse_end_time = time.time()
#
#         pulse_duration = pulse_end_time - pulse_start_time
#         return round(pulse_duration * 17150, 2)
#
#     finally:
#         GPIO.cleanup()


def webserver(sl):
    app.config["STATE"] = sl
    app.run(host="0.0.0.0", use_reloader=False, debug=True)


# TODO need to be in the same module to share state?
# TODO shared memory? https://stackoverflow.com/questions/14124588/shared-memory-in-multiprocessing


def run_sim(sl):
    pygame.init()

    screen = pygame.display.set_mode(
        (640, 480), pygame.DOUBLEBUF, 8
    )  # TODO revert  pygame.FULLSCREEN)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    width, height = screen.get_size()

    # TODO parametrize num particles
    particles = [
        Particle((random.randint(0, width), random.randint(0, height)), i % 4)
        for i in range(50)
    ]

    clock = pygame.time.Clock()

    pygame.display.set_caption("Cluster Simulation")
    while True:
        shared_list_copy = [e for e in sl]
        spatial_hash = SpatialHash(
            shared_list_copy[INTERACTION_RADIUS_INDEX], width, height
        )
        clock.tick(30)
        for particle in particles:
            spatial_hash.insert_particle(particle)

        screen.fill((0, 0, 0))
        # print(clock.get_fps())

        dist = shared_list_copy[DISTANCE_INDEX]
        # print(dist)

        interaction_radius = shared_list_copy[INTERACTION_RADIUS_INDEX]
        # TODO redo slice_sl
        color_interactions = slice_sl(
            shared_list_copy,
            COLOR_INTERACTIONS_START_INDEX,
            COLOR_INTERACTIONS_START_INDEX + COLOR_INTERACTIONS_ROW_LENGTH * 4,
        )
        print(color_interactions)
        color_number_lookup = slice_sl(
            shared_list_copy,
            COLOR_NUMBER_LOOKUP_START_INDEX,
            COLOR_NUMBER_LOOKUP_START_INDEX + COLOR_NUMBER_LOOKUP_ROW_LENGTH * 4,
        )
        particle_radius = shared_list_copy[PARTICLE_RADIUS_INDEX]

        for particle in particles:
            for other in spatial_hash.neighbor_particles(particle):
                if particle != other:
                    particle.interact(other, interaction_radius, color_interactions)
            particle.update(width, height, shared_list_copy[FRICTION_COEFFICIENT_INDEX])
            particle.draw(screen, color_number_lookup, particle_radius)
            # quit()

        for event in pygame.event.get():
            if (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_ESCAPE
                or event.type == pygame.QUIT
            ):
                pygame.quit()
                return

        pygame.display.update()


def main():
    with SharedMemoryManager() as smm:
        sl = smm.ShareableList(INITIAL_STATE)

        web_thread = multiprocessing.Process(target=webserver, args=(sl,))
        web_thread.start()

        sim_thread = multiprocessing.Process(target=run_sim, args=(sl,))
        sim_thread.start()

        # dist_thread = multiprocessing.Process(target=read_distance, args=(sl,))
        # dist_thread.start()

        sim_thread.join()
        web_thread.terminate()
        web_thread.join()


if __name__ == "__main__":
    main()
