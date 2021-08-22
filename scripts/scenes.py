import sys

import pygame

import map
import camera

import utility as u
import game_object as go


pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((400, 400))

FPS = 60

BLACK = (0, 0, 0)


class Game:
    def __init__(self):
        self.level = 1  
        self.game = self._reload_level(self.level)

    def _reload_level(self, level):
        path = f"../level/level{level}.json"
        load = u.load_json(path)

        self.camera = camera.Camera(-600, 600)

        tiles_path = "../assets/floor"
        map_parse = u.json_to_charlist(load, "tilemap")
        self.map_level = map.Tilemap(map_parse, tiles_path)

        puzzle_path = "../assets/puzzles"
        padlock_path = "../assets/padlock/padlock_0.png"

        # key(str) = [value(puzzle), [value(padlock)]]
        self.lock = {}
        self.unlock = []

        self.index = 0

        for key in load["puzzles"]:
            try:
                self.lock[key] = [go.Puzzle(puzzle_path, load["puzzles"][key][0]),  [go.Padlock(padlock_path, load["puzzles"][key][1][val]) for val in load["puzzles"][key][1]]]
            except TypeError:
                self.unlock.append(go.Puzzle(puzzle_path, load["puzzles"][key][0]))

        self.opn = 0

    def _input_handle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    if (self.index + 1) < len(self.unlock):
                        self.index += 1
                    else:
                        self.index = 0 
        
        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_RIGHT]:
            self.unlock[self.index].move(right=True)
        if key_pressed[pygame.K_LEFT]:
            self.unlock[self.index].move(left=True)
        if key_pressed[pygame.K_DOWN]:
            self.unlock[self.index].move(down=True)
        if key_pressed[pygame.K_UP]:
            self.unlock[self.index].move(up=True)

    def _logic(self):
        for key in self.lock.copy():
            if False not in [value.unlock(self.unlock) for value in self.lock[key][1]]:
                self.unlock.append(self.lock[key][0])
                del self.lock[key]

    def _update(self):
        self.camera.focus(self.unlock[self.index])

        self.map_level.set_scroll(self.camera.get_scroll())

        for puzzle in self.unlock:
            puzzle.set_scroll(self.camera.get_scroll())
            puzzle.update()

        for lock in self.lock:
            for lck in [self.lock[lock][0], *self.lock[lock][1]]:
                lck.set_scroll(self.camera.get_scroll())
                lck.update()

    def _draw(self):
        screen.fill(BLACK)

        self.map_level.draw(screen)

        for puzzle in self.unlock:
            puzzle.draw(screen)

        for lock in self.lock:
            for lck in [self.lock[lock][0], *self.lock[lock][1]]:
                lck.draw(screen)

    def play(self):
        while True:
            clock.tick(FPS)

            self._input_handle()

            self._logic()

            self._update()

            self._draw()

            pygame.display.update()


