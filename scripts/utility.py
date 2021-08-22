import os
import json

import pygame


def search_png(path):
    return [img for img in os.listdir(path) if img.endswith(".png")]

def load_image(path, width, height):
    image = pygame.image.load(path)
    trans = pygame.transform.scale(image, (width, height))

    return trans

def load_json(path):
    with open(path, "r") as f:
        file = json.load(f)
        return file

def json_to_charlist(file, key):
    return [char.split(",") for row in file[key] for char in row]


