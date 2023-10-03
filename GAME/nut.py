from cocos.sprite import Sprite
from resource import nut, peanut

class Nut(Sprite):
    def __init__(self, block, type):
        image = nut if (type == 'nut') else peanut
        super(Nut, self).__init__(image)
        self.game = block.game
        self.flying_squirrel = block.game.flying_squirrel
        self.floor = block.floor
        self.position = (block.x + block.width / 2), (block.height + 100)
        self.type = type

        self.schedule(self.update)

    def update(self, dt):
        px = self.flying_squirrel.x + self.flying_squirrel.width / 2 - self.floor.x
        py = self.flying_squirrel.y + self.flying_squirrel.height / 2

        if abs(px - self.x) < 50 and abs(py - self.y) < 50:
            # 吃到堅果
            self.parent.remove(self)
            self.flying_squirrel.big() if (self.type == 'nut') else self.flying_squirrel.rush()

    def reset(self):
        self.parent.remove(self)
