import os
import json

import pygame


def search_png(path):
    return [img for img in os.listdir(path) if img.endswith(".png")]

def load_image(path, width, height):
    image = pygame.image.load(path)
    trans = pygame.transform.scale(image, (width, height))

    return trans

def load_images(path):
    images = []
    
    images_dir = search_png(path)
    for image in images_dir:
        load = load_image(f"{path}/{image}", 80, 80)

        images.append(load)

    return images

def load_json(path):
    with open(path, "r") as f:
        file = json.load(f)
        return file

def json_to_charlist(file, key):
    return [char.split(",") for row in file[key] for char in row]

def generate_key(images):
    return "".join(char for char in images if char.isdecimal())
