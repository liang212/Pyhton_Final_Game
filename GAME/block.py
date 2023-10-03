from random import random
from cocos.sprite import Sprite
from nut import Nut
from resource import block

class Block(Sprite):
    def __init__(self, game):
        super(Block, self).__init__(block)

        self.game = game
        self.flying_squirrel = game.flying_squirrel
        self.floor = game.floor
        self.active = True
        self.image_anchor = 0, 0
        self.reset()

        self.schedule(self.update)

    def update(self, dt):
        if self.active and self.x < self.flying_squirrel.x - self.floor.x:
            self.active = False
            self.game.add_score()
        if self.x + self.width + self.game.floor.x < -10:
            self.reset()

    def reset(self):
        x, y = self.game.last_block
        if x == 0:
            self.scale_x = 5
            self.scale_y = 1
            self.position = 0, 0
            self.active = False
        else:
            self.scale_x = 0.75 + random() * 2
            self.scale_y = min(max(y - 50 + random() * 100, 50), 300) / 100.0
            self.position = x + 80 + random() * 100, 0
            self.active = True
            # 隨機生成堅果、花生（統一用 Nut，配合引數分辨是堅果還是花生）
            if self.x < 500:
                self.floor.add(Nut(self, 'nut'))
            elif self.x < 1000:
                self.floor.add(Nut(self, 'peanut'))
            else:
                rand = random()
                if 0.6 <= rand < 0.8:
                    self.floor.add(Nut(self, 'peanut'))
                if 0.8 <= rand <1:
                    self.floor.add(Nut(self, 'nut'))
        self.game.last_block = self.x + self.width, self.height
