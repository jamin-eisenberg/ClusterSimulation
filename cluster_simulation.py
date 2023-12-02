import random
import sys
import multiprocessing
# import RPi.GPIO as GPIO TODO gpio
import time
import threading

import pygame
from flask import Flask, request

from Particle import Particle
from SpatialHash import SpatialHash
from State import SharedState

# TODO serve with gunicorn
# TODO ensure server works with sim
# TODO update script to run server

app = Flask(__name__)

label = "label"

state = SharedState()


@app.route("/<color1>/to/<color2>", methods=["PATCH"])
def change_color_relationship(color1, color2):
    state = app.config['STATE']
    new_attraction = request.args.get("attraction")

    curr_interactions = state.get("color_interactions")
    curr_interactions[int(color1)][int(color2)] = float(new_attraction)
    state.set("color_interactions", curr_interactions)

    return ""


# TODO concurrent
def read_distance():
    time.sleep(1)
    return random.randint(0, 100)


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

def webserver(state):
    app.config['STATE'] = state
    app.run(host='0.0.0.0', use_reloader=False, debug=True)


def run_sim():
    global state
    pygame.init()
    pygame.font.init()

    my_font = pygame.font.SysFont('Comic Sans MS', 30)

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF, 8)  # TODO revert  pygame.FULLSCREEN)
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN])

    width, height = screen.get_size()

    particles = [Particle((random.randint(0, width), random.randint(0, height)), i % 4, state) for i in range(300)]

    clock = pygame.time.Clock()


    pygame.display.set_caption("Cluster Simulation")
    while True:
        spatial_hash = SpatialHash(state.get("interaction_radius"), width, height)
        dt = clock.tick(30)
        for particle in particles:
            spatial_hash.insert_particle(particle)

        clock.tick()
        print(clock.get_fps())
        screen.fill((0, 0, 0))
        # dist = read_distance()
        # text_surface = my_font.render(f'Distance {label}: {dist}', False, (0, 0, 0))
        # screen.blit(text_surface, (width / 2, height / 2))

        # with state_lock:
        for particle in particles:
            for other in spatial_hash.neighbor_particles(particle):
                if particle != other:
                    particle.interact(other)
            particle.update(width, height)
            particle.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE or event.type == pygame.QUIT:
                pygame.quit()
                return

        pygame.display.update()


def main():
    web_thread = multiprocessing.Process(target=webserver, args=(state,))
    web_thread.start()
    sim_thread = multiprocessing.Process(target=run_sim)
    sim_thread.start()
    sim_thread.join()
    web_thread.terminate()
    web_thread.join()


if __name__ == '__main__':
    main()
