import pygame

import animations as a
import utility as u


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
        self.anim.load_animations("ready", image, 6)
        self.anim.set_state("ready")

        super().__init__(self.anim.get_frame(), position)

    def move(self, up=False, down=False, left=False, right=False):
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
        super().__init__(u.load_image(image, 80, 80), position)

    def unlock(self, puzzles):
        puzzles_x = [puzzle.rect.x for puzzle in puzzles]
        puzzles_y = [puzzle.rect.y for puzzle in puzzles]
        return (self.rect.x in puzzles_x and self.rect.y in puzzles_y)