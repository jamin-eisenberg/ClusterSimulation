import json
import os
import random
import multiprocessing
import socket

import time
import webbrowser
from multiprocessing.managers import SharedMemoryManager

import flask
import pygame
from flask import Flask, request, send_from_directory, send_file, render_template
from flask_cors import CORS
from pynput.mouse import Controller
from werkzeug.serving import get_interface_ip

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

app = Flask(__name__, static_folder="cluster-simulation/build", template_folder="cluster-simulation/build")
CORS(app)

lock = multiprocessing.Lock()

def str_response(s):
    response = flask.make_response(s)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve(path):
    if path != "" and os.path.exists(app.static_folder + "/" + path):
        return send_from_directory(app.static_folder, path)
    elif path == "":
        return render_template("index.html", myip=request.host)


def verify_num(n, min, max, should_be_int=False):
    try:
        converted = (int if should_be_int else float)(n)
        return min <= converted <= max
    except ValueError:
        return False


@app.route("/<color1>/to/<color2>/<new_attraction>", methods=["PATCH"])
def change_color_relationship(color1, color2, new_attraction):
    verify_num(color1, 0, 3, True)
    verify_num(color2, 0, 3, True)
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[
            COLOR_INTERACTIONS_START_INDEX
            + int(color1) * COLOR_INTERACTIONS_ROW_LENGTH
            + int(color2)
        ] = 0 if new_attraction.strip() == "" or new_attraction.strip() == "NaN" else float(new_attraction)
    return str_response("")


@app.route("/particle-radius/<new_radius>", methods=["PATCH"])
def change_particle_radius(new_radius):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[PARTICLE_RADIUS_INDEX] = int(new_radius)
    return str_response("")

@app.route("/particle-interaction-radius/<new_interaction_radius>", methods=["PATCH"])
def change_particle_interaction_radius(new_interaction_radius):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[INTERACTION_RADIUS_INDEX] = int(new_interaction_radius)
    return str_response("")


@app.route("/particle-count/<new_count>", methods=["PATCH"])
def change_particle_count(new_count):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[DESIRED_PARTICLE_COUNT_INDEX] = int(new_count)
    return str_response("")


@app.route("/friction-coefficient/<new_friction_coefficient>", methods=["PATCH"])
def change_friction_coefficient(new_friction_coefficient):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[FRICTION_COEFFICIENT_INDEX] = float(new_friction_coefficient)
    return str_response("")


# TODO type and index validation for methods, put error in response (put success message in non-fails?)
@app.route("/state", methods=["GET"])
def get_state():
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        return [e for e in sl]


@app.route("/disturbance/<new_disturbance_amount>", methods=["PATCH"])
def change_disturbance_amount(new_disturbance_amount):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[DISTURBANCE_AMOUNT_INDEX] = float(new_disturbance_amount)
    return str_response("")


@app.route("/disturbance-derivative/<new_disturbance_derivative>", methods=["PATCH"])
def change_disturbance_derivative_amount(new_disturbance_derivative):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[DISTURBANCE_DERIVATIVE_THRESHOLD_INDEX] = int(new_disturbance_derivative)
    return str_response("")


@app.route("/distance-read-period/<new_distance_read_period>", methods=["PATCH"])
def change_distance_read_period(new_distance_read_period):
    sl = app.config["STATE"]
    with app.config["LOCK"]:
        sl[DISTANCE_READ_PERIOD_INDEX] = float(new_distance_read_period)
    return str_response("")


@app.route("/color/<to_change>/to/<r>/<g>/<b>", methods=["PATCH"])
def change_color(to_change, r, g, b):
    sl = app.config["STATE"]
    color_index = (
        COLOR_NUMBER_LOOKUP_START_INDEX + int(to_change) * COLOR_NUMBER_LOOKUP_ROW_LENGTH
    )
    with app.config["LOCK"]:
        sl[color_index] = int(r)
        sl[color_index + 1] = int(g)
        sl[color_index + 2] = int(b)
    return str_response("")


def webserver(sl, lock):
    app.config["STATE"] = sl
    app.config["LOCK"] = lock
    app.run(host="0.0.0.0", port=80, use_reloader=False, debug=True)


def run_sim(sl, lock):
    pygame.init()

    icon = pygame.image.load('cake_icon.png')
    pygame.display.set_icon(icon)

    monitor_info = pygame.display.Info()
    screen = pygame.display.set_mode(
        (monitor_info.current_w, monitor_info.current_h), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.FULLSCREEN, 8
    )
    pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

    width, height = screen.get_size()

    next_color_to_generate = 0
    particles = []

    clock = pygame.time.Clock()

    pygame.display.set_caption("Cluster Simulation")

    space_pressed = False

    while True:
        try:
            with lock:
                shared_list_copy = [e for e in sl]

            clock.tick(30)

            screen.fill((0, 0, 0))
            # print(clock.get_fps())

            previous_dist = shared_list_copy[PREVIOUS_DISTANCE_INDEX]
            dist = shared_list_copy[DISTANCE_INDEX]
            # if (
            #     previous_dist - dist
            #     > shared_list_copy[DISTURBANCE_DERIVATIVE_THRESHOLD_INDEX]
            # ):
            if space_pressed:
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

            spatial_hash = SpatialHash(
                shared_list_copy[INTERACTION_RADIUS_INDEX], width, height
            )
            for particle in particles:
                spatial_hash.insert_particle(particle)

            for particle in particles:
                for other in spatial_hash.neighbor_particles(particle):
                    if particle != other:
                        particle.interact(other, interaction_radius, color_interactions)
                particle.update(width, height, shared_list_copy[FRICTION_COEFFICIENT_INDEX])
                particle.draw(screen, color_number_lookup, particle_radius)
        except Exception as e:
            print(e)
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F12:
                    pygame.display.toggle_fullscreen()
                elif event.key == pygame.K_SPACE:
                    space_pressed = True
            elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                space_pressed = False

        pygame.display.update()


def main():
    with SharedMemoryManager() as smm:
        try:
            global lock
            filename = "data.json" if os.path.isfile("data.json") else "initial_state.json"
            with open(filename) as f:
                sl = smm.ShareableList(json.load(f))

            ip = get_interface_ip(socket.AF_INET)
            webbrowser.open_new_tab('http://' + ip)

            web_thread = multiprocessing.Process(target=webserver, args=(sl, lock))
            web_thread.start()

            sim_thread = multiprocessing.Process(target=run_sim, args=(sl, lock))
            sim_thread.start()

            sim_thread.join()
            web_thread.terminate()
            web_thread.join()

        finally:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump([e for e in sl], f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
