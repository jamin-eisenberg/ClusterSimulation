import json
import random
import multiprocessing

# import RPi.GPIO as GPIO TODO gpio
import time
from multiprocessing.managers import SharedMemoryManager

import pygame
from flask import Flask, request
from pynput.mouse import Controller

from Particle import Particle
from SpatialHash import SpatialHash
from constants import (
    COLOR_INTERACTIONS_START_INDEX,
    COLOR_INTERACTIONS_ROW_LENGTH,
    DISTANCE_INDEX,
    INTERACTION_RADIUS_INDEX,
    FRICTION_COEFFICIENT_INDEX,
    COLOR_NUMBER_LOOKUP_START_INDEX,
    COLOR_NUMBER_LOOKUP_ROW_LENGTH,
    PARTICLE_RADIUS_INDEX,
    PREVIOUS_DISTANCE_INDEX,
    DISTURBANCE_AMOUNT_INDEX,
    DISTURBANCE_DERIVATIVE_THRESHOLD_INDEX,
    DISTANCE_READ_PERIOD_INDEX,
    DESIRED_PARTICLE_COUNT_INDEX,
)

app = Flask(__name__)

INITIAL_STATE = [
    5,  # particle radius
    70,  # interaction radius
    0.97,  # friction
    0,  # distance
    0,  # previous distance
    -0.1,  # disturbance amount
    10,  # disturbance derivative threshold
    0.1,  # distance read period
    50,  # desired number of particles
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
    sl[
        COLOR_INTERACTIONS_START_INDEX
        + int(color1) * COLOR_INTERACTIONS_ROW_LENGTH
        + int(color2)
    ] = float(new_attraction)

    return ""


@app.route("/particle-count/<new_count>", methods=["PATCH"])
def change_particle_count(new_count):
    sl = app.config["STATE"]
    sl[DESIRED_PARTICLE_COUNT_INDEX] = int(new_count)

    return ""


def read_distance(sl):
    while True:
        time.sleep(sl[DISTANCE_READ_PERIOD_INDEX])
        mouse = Controller()
        sl[PREVIOUS_DISTANCE_INDEX] = sl[DISTANCE_INDEX]
        sl[DISTANCE_INDEX] = mouse.position[0]
        # print(pygame.key.get_pressed()[pygame.K_SPACE])


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


def run_sim(sl):
    pygame.init()

    screen = pygame.display.set_mode(
        (640, 480), pygame.DOUBLEBUF, 8
    )  # TODO revert  pygame.FULLSCREEN)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    width, height = screen.get_size()

    next_color_to_generate = 0
    particles = []

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

        previous_dist = shared_list_copy[PREVIOUS_DISTANCE_INDEX]
        dist = shared_list_copy[DISTANCE_INDEX]
        if (
            dist - previous_dist
            > shared_list_copy[DISTURBANCE_DERIVATIVE_THRESHOLD_INDEX]
        ):
            shared_list_copy[
                COLOR_INTERACTIONS_START_INDEX : COLOR_INTERACTIONS_START_INDEX
                + COLOR_INTERACTIONS_ROW_LENGTH * 4
            ] = [
                shared_list_copy[DISTURBANCE_AMOUNT_INDEX]
                for _ in range(COLOR_INTERACTIONS_ROW_LENGTH * 4)
            ]

        if len(particles) > shared_list_copy[DESIRED_PARTICLE_COUNT_INDEX]:
            particles.pop(0)
        elif len(particles) < shared_list_copy[DESIRED_PARTICLE_COUNT_INDEX]:
            particles.append(
                Particle(
                    (random.randint(0, width), random.randint(0, height)),
                    next_color_to_generate,
                )
            )
            next_color_to_generate = (next_color_to_generate + 1) % 4

        interaction_radius = shared_list_copy[INTERACTION_RADIUS_INDEX]
        color_interactions = shared_list_copy[
            COLOR_INTERACTIONS_START_INDEX : COLOR_INTERACTIONS_START_INDEX
            + COLOR_INTERACTIONS_ROW_LENGTH * 4
        ]
        color_number_lookup = shared_list_copy[
            COLOR_NUMBER_LOOKUP_START_INDEX : COLOR_NUMBER_LOOKUP_START_INDEX
            + COLOR_NUMBER_LOOKUP_ROW_LENGTH * 4
        ]
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
        with open('data.json') as f:
            sl = smm.ShareableList(json.load(f))

        web_thread = multiprocessing.Process(target=webserver, args=(sl,))
        web_thread.start()

        sim_thread = multiprocessing.Process(target=run_sim, args=(sl,))
        sim_thread.start()

        dist_thread = multiprocessing.Process(target=read_distance, args=(sl,))
        dist_thread.start()

        sim_thread.join()
        web_thread.terminate()
        web_thread.join()
        dist_thread.terminate()
        dist_thread.join()

        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump([e for e in sl], f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
