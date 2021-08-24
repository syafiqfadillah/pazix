import os

import pygame


def search_png(path):
    return [img for img in os.listdir(path) if img.endswith(".png")]

def load_image(path, width, height):
    image = pygame.image.load(path)
    trans = pygame.transform.scale(image, (width, height))

    return trans



