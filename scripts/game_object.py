import pygame

from . import animations as a
from . import helper_func as hf


class GameObject:
    def __init__(self, image, position):
        self.image = image
        self.position = position
        self.rect = self.image.get_rect(center=self.position)
    
    def set_scroll(self, scroll):
        self.scroll = scroll
    
    def update(self):
        self.position = (self.rect.x - self.scroll[0], self.rect.y - self.scroll[1])
    
    def draw(self, screen):
        screen.blit(self.image, self.position)


class Puzzle(GameObject):
    def __init__(self, image, position):
        self.anim = a.Animations()
        self.anim.load_animations("ready", f"{image}/ready", 1, loop=False)
        self.anim.load_animations("rotate", f"{image}/rotate", 15, loop=False)
        self.anim.set_state("ready")

        super().__init__(self.anim.get_frame(), position)

    def rotate(self):
        self.anim.set_state("rotate")

    def move(self, up=False, down=False, left=False, right=False):
        if self.anim.get_state() == "rotate" and self.anim.end_frame():
            self.movement = [0, 0]

            if up:
                self.movement[1] = -2
            elif down:
                self.movement[1] = 2
            elif left:
                self.movement[0] = -2
            elif right:
                self.movement[0] = 2
            
            self.rect.x += self.movement[0]
            self.rect.y += self.movement[1]
        
    def collision(self, rects):
        for rect in rects:
            if self.rect.collidrect(self.rect, rect):
                if self.movement[1] < 0:
                    self.rect.top = rect.bottom
                elif self.movement[1] > 0:
                    self.rect.bottom = rect.top
                elif self.movement[0] < 0:
                    self.rect.left = rect.right
                elif self.movement[0] > 0:
                    self.rect.right = rect.left
    
    def draw(self, screen):
        self.anim.play(screen, self.position)


class Padlock(GameObject):
    def __init__(self, image, position):
        super().__init__(hf.load_image(image, 80, 80), position)

    def unlock(self, puzzles):
        # so that every puzzle in the unlock list can unlock the padlock
        puzzles_x = [puzzle.rect.x for puzzle in puzzles]
        puzzles_y = [puzzle.rect.y for puzzle in puzzles]
        return (self.rect.x in puzzles_x and self.rect.y in puzzles_y)