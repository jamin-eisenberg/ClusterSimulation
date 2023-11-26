import random
from html import escape

import pygame
import sys
# import RPi.GPIO as GPIO TODO gpio
import time

from flask import Flask

from Particle import Particle

# TODO serve with gunicorn
# TODO ensure server works with sim
# TODO update script to run server

app = Flask(__name__)

label = "label"


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/<name>")
def hello(name):
    global label
    label = name
    return f"Hello, {escape(name)}!"

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


pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

particles = [Particle((random.randint(0, width), random.randint(0, height)), i % 2) for i in range(100)]

pygame.display.set_caption("Hello World")
while True:
    screen.fill((0, 0, 0))
    # dist = read_distance()
    # text_surface = my_font.render(f'Distance {label}: {dist}', False, (0, 0, 0))
    # screen.blit(text_surface, (width / 2, height / 2))

    for particle in particles:
        for other in particles:
            if particle != other:
                particle.interact(other)
        particle.update(width, height)
        particle.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
