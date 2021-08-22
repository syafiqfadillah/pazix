import json

import pygame

import utility as u


class Tilemap:
    def __init__(self, map, images):
        self.tile_width = 80
        self.tile_height = 80
        self.map = map
        self.images = self.load_images(images)
        self.blit = {}

    @staticmethod
    def generate_key(images):
        return "".join(char for char in images if char.isdecimal())

    def load_images(self, path):
        data = {}
        images = u.search_png(path)
        for image in images:
            key = self.generate_key(image)

            data[key] = u.load_image(f"{path}/{image}", self.tile_width, self.tile_height)

        return data
    
    def set_scroll(self, scroll):
        self.scroll = scroll
    
    def draw(self, screen):
        y = -600
        for row in self.map:
            x = -600
            for tile in row:
                screen.blit(self.images[tile], (x - self.scroll[0], y - self.scroll[1]))

                x += self.tile_width
            
            y += self.tile_height