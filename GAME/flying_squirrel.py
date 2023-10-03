from cocos.sprite import Sprite
from time import sleep
from pygame.mixer import Sound, music
from resource import flying_squirrel, flying_squirrel_flying, rush, die, jump

class Flying_squirrel(Sprite):
    def __init__(self, game):
        self.image1 = flying_squirrel
        self.image2 = flying_squirrel_flying
        super(Flying_squirrel, self).__init__(self.image1)

        self.sound_rush = Sound(rush)
        self.sound_die = Sound(die)
        self.sound_jump = Sound(jump)

        self.game = game
        self.reset()
        self.schedule(self.update)

    def reset(self):
        self.dead = False
        self.can_jump = False
        self.speed = 0
        self.rush_time = 0
        self.big_time = 0
        self.velocity = 0
        self.image_anchor = 0, 0
        self.position = 100, 300
        self.image = self.image1

    def jump(self, h):
        if not(self.dead) and self.can_jump:
            self.y += 3
            self.speed -= max(min(h, 350), 200)
            self.speed = max(-450, self.speed)
            self.can_jump = False
            self.sound_jump.play()

    def land(self, y):
        if not(self.dead) and self.y > y - 30:
            self.can_jump = True
            self.speed = 0
            self.y = y

    def update(self, dt):
        if not(self.dead):
            self.speed += 300 * dt
            self.y -= self.speed * dt
            if self.rush_time > 0:
                self.rush_time -= dt
                if self.y < 10:
                    self.can_jump = True
                    if self.jump and self.y > 13:
                        self.can_jump = False
                if self.speed > 0:
                    self.speed -= 20 * dt

                if self.rush_time <= 0:
                    self.velocity = 0
                    self.image = self.image1
                    
            if self.big_time > 0:
                self.big_time -= dt
                if self.jump:
                    if self.can_jump:
                        self.y -= 1
                if self.big_time <= 0:
                    self.image = self.image1
                    self.image_anchor = 1.5, 1.5
                    self.can_jump = True

            if self.y < -150:
                self.die()

    def die(self):
        music.stop()
        self.sound_die.play()
        sleep(2.7)
        self.speed = 0
        self.dead = True
        self.game.end_game()

    def rush(self):
        self.sound_rush.play()
        self.image = self.image1
        self.velocity = 400
        self.rush_time = 5
        self.sound_rush.play()
    
    def big(self):
        self.sound_rush.play()  # 共用音效
        self.image_anchor = 1.5, 1.5
        self.image = self.image2
        self.big_time = 5
        self.sound_rush.play()
