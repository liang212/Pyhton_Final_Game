from cocos.layer import ColorLayer
from cocos.text import Label
from cocos.menu import Menu, MenuItem

class Gameover(ColorLayer):
    def __init__(self, game):
        super(Gameover, self).__init__(0, 0, 0, 255)
        self.game = game
        self.score = Label('得分：%d' % self.game.score,
                                      font_name='微軟正黑體',
                                      font_size=32, position = (240, 180))
        self.add(self.score)

        message = Menu('胖到飛不起來了(˘•ω•˘)')
        message.font_title['font_size'] = 32
        message.font_item['font_size'] = 24
        message.font_title['font_name'] = '微軟正黑體'
        message.font_item['font_name'] = '微軟正黑體'
        message.font_item_selected['font_name'] = '微軟正黑體'      
        replay = MenuItem('再飛一次', self.replay)  # 模擬按鍵
        replay.y = -100
        message.create_menu([replay])
        self.add(message)

    def replay(self):
        self.game.reset()
