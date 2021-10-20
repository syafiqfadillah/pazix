from . import helper_func as hf


class Animations:
    def __init__(self):
        self.frame = 0
        self.animations_loop = []
        self.animations_db = {}

    def load_animations(self, name, images, frame_durations, loop=True):
        images = hf.load_images(images)

        if loop:
            self.animations_loop.append(name)

        data = []
        for image in range(len(images)):
            for _ in range(frame_durations):
                data.append(images[image])

        self.animations_db[name] = data
    
    def get_frame(self):
        return self.animations_db[self.state][self.frame - 1]

    def set_state(self, new_state):
        self.state = new_state

    def get_state(self):
        return self.state
    
    def end_frame(self):
        return self.frame >= len(self.animations_db[self.state])

    def frame_control(self):
        if self.end_frame():
            self.frame = 0 if self.state in self.animations_loop else len(self.animations_db[self.state])

    def frame_increase(self):
        self.frame += 1

    def play(self, screen, position):
        self.frame_increase()
        self.frame_control()
        screen.blit(self.get_frame(), position)
