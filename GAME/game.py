from cocos.layer import ScrollableLayer
from cocos.director import director
from cocos.sprite import Sprite
from cocos.text import Label
from cocos.cocosnode import CocosNode
from cocos.scene import Scene
from pyaudio import PyAudio, paInt16
from pygame.mixer import init, music
from struct import unpack
from flying_squirrel import Flying_squirrel
from block import Block
from gameover import Gameover
from resource import bg, bgm, bgm2, volume

class VoiceGame(ScrollableLayer):
    is_event_handler = True

    def __init__(self):
        super(VoiceGame, self).__init__()
    
        self.width, self.height = director.get_window_size()
        self.bg = Sprite(bg, position = (640, 240))
        self.add(self.bg)

        init()  #pygame.mixer

        self.gameover = None

        self.score = 0  #紀錄得分
        self.txt_score = Label('得分：0',
                                font_name='微軟正黑體',
                                font_size=24,
                                color=(0, 0, 0, 255),
                                position = (500, 440))
        self.add(self.txt_score, 99999)

        # init voice
        self.NUM_SAMPLES = 2048  # pyAudio内部緩存的大小
        self.LEVEL = 1500  # 聲音保存的閾值

        self.voicebar = Sprite(volume, color=(255, 255, 255), position = (20, 450), anchor = (0, 0))
        self.voicebar.scale_y = 0.1
        self.add(self.voicebar)

        self.flying_squirrel = Flying_squirrel(self)
        self.add(self.flying_squirrel)

        self.floor = CocosNode()
        self.add(self.floor)
        self.last_block = 0, 100
        for i in range(5):
            b = Block(self)
            self.floor.add(b)
            pos = b.x + b.width, b.height

        # 開啟聲音輸入
        pa = PyAudio()
        SAMPLING_RATE = int(pa.get_device_info_by_index(0)['defaultSampleRate'])
        self.stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True, frames_per_buffer=self.NUM_SAMPLES)
        self.stream.stop_stream()
        self.BGM2 = False
        music.load(bgm2)
        music.play(-1)

        music.load(bgm)
        music.play(-1)

        self.schedule(self.update)

    def collide(self):
        px = self.flying_squirrel.x - self.floor.x
        for b in self.floor.get_children():
            if b.x <= px + self.flying_squirrel.width * 0.8 and px + self.flying_squirrel.width * 0.2 <= b.x + b.width:
                if self.flying_squirrel.y < b.height:
                    self.flying_squirrel.land(b.height)
                    break

    def update(self, dt):
        # 讀進NUM_SAMPLES取樣
        if self.stream.is_stopped():
            self.stream.start_stream()
        string_audio_data = self.stream.read(self.NUM_SAMPLES)
        k = max(unpack('2048h', string_audio_data))
        self.voicebar.scale_x = k / 10000.0
        if k > 3000:
            if not self.flying_squirrel.dead:
                self.floor.x -= min((k / 20.0), 150) * dt
        if k > 8000:
            self.flying_squirrel.jump((k - 8000) / 25.0)
        self.floor.x -= self.flying_squirrel.velocity * dt
        self.collide()

    def reset(self):
        self.floor.x = 0
        self.last_block = 0, 100
        for b in self.floor.get_children():
            b.reset()
        self.score = 0
        self.txt_score.element.text = '得分：0'
        self.flying_squirrel.reset()
        self.bg.position = 640,240
        music.load(bgm)
        music.play(-1)
        if self.gameover:
            self.remove(self.gameover)
            self.gameover = None
        self.stream.start_stream()
        self.resume_scheduler()
        music.play(-1)

    def end_game(self):
        self.stream.stop_stream()
        self.pause_scheduler()
        self.gameover = Gameover(self)
        self.BGM2 = False
        self.add(self.gameover, 100000)

    def add_score(self):
        self.score += 1
        self.txt_score.element.text = '得分：%d' % self.score
        if self.score > 10 and not self.BGM2:
        # 切換成第二關背景音樂
            music.load(bgm2)
            music.play(-1)
            self.BGM2=True
            self.bg.position = 0,240


director.init(caption="飛吧！鼠哥！")
director.run(Scene(VoiceGame()))

