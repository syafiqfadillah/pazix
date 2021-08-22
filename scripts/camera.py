class Camera:
    def __init__(self, border_min, border_max):
        self.true_scroll = [0, 0]
        self.border_min = border_min
        self.border_max = border_max
    
    def focus(self, position):
        self.true_scroll[0] += (position.rect.x - self.true_scroll[0] - 150) / 20
        self.true_scroll[1] += (position.rect.y - self.true_scroll[1] - 150) / 20
        self.scroll = self.true_scroll.copy()
        self.scroll[0] = max(self.border_min, int(self.scroll[0]))
        self.scroll[0] = min(self.scroll[0], self.border_max - 300)
        self.scroll[1] = max(self.border_min, int(self.scroll[1]))
        self.scroll[1] = min(self.scroll[1], self.border_max - 300)

    def get_scroll(self):
        return self.scroll