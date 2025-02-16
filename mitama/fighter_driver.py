from gameLib.fighter import Fighter, ut


class DriverFighter(Fighter):
    '''御魂战斗司机程序，参数mode, emyc'''

    def __init__(self, done=1, emyc=0):
        # 初始化
        Fighter.__init__(self, 'Driver: ', emyc)

    def start(self):
        '''单人御魂司机'''
        # 设定点击疲劳度
        mood1 = ut.Mood()
        mood2 = ut.Mood()
        mood3 = ut.Mood(3)

        # 战斗主循环
        self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png')
        while True:
            # 司机点击开始战斗，需要锁定御魂阵容
            mood1.moodsleep()
            self.yys.mouse_click_bg((857, 515), (998, 556))
            self.log.writeinfo('Driver: clicked KAI-SHI-ZHAN-DOU!')

            # 检测是否进入战斗
            start_time = ut.time.time()
            while ut.time.time() - start_time <= 10:
                if self.yys.find_game_img('img\\ZI-DONG.png'):
                    self.log.writeinfo(self.name + 'Already in battle')
                    break
                else:
                    self.yys.mouse_click_bg((857, 515), (998, 556))
                mood2.moodsleep()

            # 已经进入战斗，司机自动点怪
            self.click_monster()

            # 检测是否打完
            self.check_end()
            mood2.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            start_time = ut.time.time()
            while ut.time.time() - start_time <= 10:
                if(self.yys.wait_game_img('img\\KAI-SHI-ZHAN-DOU.png', mood3.get1mood()/1000, False)):
                    self.log.writeinfo('Driver: in team')
                    break

                # 点击结算
                if (not self.yys.find_game_img('img\\MAIL.png')):
                    self.yys.mouse_click_bg(ut.secondposition())

                # 点击默认邀请
                if self.yys.find_game_img('img\\ZI-DONG-YAO-QING.png'):
                    self.yys.mouse_click_bg((497, 319))
                    ut.time.sleep(0.2)
                    self.yys.mouse_click_bg((674, 384))
                    self.log.writeinfo('Driver: auto invited')
