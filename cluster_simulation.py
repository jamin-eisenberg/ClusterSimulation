import pygame
import sys
import RPi.GPIO as GPIO
import time

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<name>")
def hello(name):
    global label
    label = name
    return f"Hello, {escape(name)}!"


def read_distance():
    try:
      GPIO.setmode(GPIO.BOARD)

      PIN_TRIGGER = 16
      PIN_ECHO = 18

      GPIO.setup(PIN_TRIGGER, GPIO.OUT)
      GPIO.setup(PIN_ECHO, GPIO.IN)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      time.sleep(0.2)

      GPIO.output(PIN_TRIGGER, GPIO.HIGH)

      time.sleep(0.00001)

      GPIO.output(PIN_TRIGGER, GPIO.LOW)

      pulse_start_time = time.time()
      while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()

      pulse_end_time = time.time()
      while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

      pulse_duration = pulse_end_time - pulse_start_time
      return round(pulse_duration * 17150, 2)

    finally:
      GPIO.cleanup()

pygame.init()
pygame.font.init()

my_font = pygame.font.SysFont('Comic Sans MS', 30)

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
width, height = screen.get_size()

pygame.display.set_caption("Hello World")
while True:
    screen.fill((255, 0, 0))
    dist = read_distance()
    text_surface = my_font.render(f'Distance {label}: {dist}', False, (0, 0, 0))
    screen.blit(text_surface, (width / 2, height / 2))

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
