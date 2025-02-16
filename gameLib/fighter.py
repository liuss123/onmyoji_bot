from gameLib.game_ctl import GameControl
import tools.utilities as ut
from tools.logsystem import WriteLog


class Fighter:

    def __init__(self, name='', emyc=0):
        # 初始参数
        self.emyc = emyc
        self.name = name

        # 启动日志
        self.log = WriteLog()

        # 绑定窗口
        self.yys = GameControl(u'阴阳师-网易游戏')
        self.log.writeinfo(self.name + 'Registration successful')

        # 激活窗口
        self.yys.activate_window()
        self.log.writeinfo(self.name + 'Activation successful')
        ut.mysleep(500)

    def check_battle(self):
        # 检测是否进入战斗
        self.yys.wait_game_img('img\\ZI-DONG.png')
        self.log.writeinfo(self.name + 'Already in battle')

    def check_end(self):
        # 检测是否打完
        self.yys.wait_game_img('img\\JIE-SU.png')
        self.log.writeinfo(self.name + "Battle finished")

    def click_monster(self):
        # 点击怪物
        pass
