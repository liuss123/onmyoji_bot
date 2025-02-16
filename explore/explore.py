from gameLib.fighter import Fighter, ut
from tools.game_pos import TansuoPos

import random


class ExploreFight(Fighter):
    def __init__(self):
        # 初始化
        Fighter.__init__(self)

    def next_scene(self):
        '''
        移动至下一个场景，每次移动400像素
        '''
        x0 = random.randint(510, 1126)
        x1 = x0 - 500
        y0 = random.randint(110, 210)
        y1 = random.randint(110, 210)
        self.yys.mouse_drag_bg((x0, y0), (x1, y1))
        # self.yys.mouse_drag_bg((1130,118),(20,118))

    def check_exp_full(self):
        '''
        检查狗粮经验，并自动换狗粮
        '''
        # 狗粮经验判断, gouliang1是中间狗粮，gouliang2是右边狗粮
        gouliang1 = self.yys.find_game_img(
            'img\\MAN1.png', 1, (397, 258), (461, 349), 1)
        gouliang2 = self.yys.find_game_img(
            'img\\MAN2.png', 1, (628, 333), (693, 430), 1)

        # print(gouliang1)
        # print(gouliang2)

        # 如果都没满则退出
        if not gouliang1 and not gouliang2:
            return

        # 开始换狗粮
        while True:
            # 点击狗粮位置
            self.yys.mouse_click_bg(
                TansuoPos.change_monster.pos, TansuoPos.change_monster.pos_end)
            if self.yys.wait_game_img('img\\QUAN-BU.png', 3, False):
                break
        ut.time.sleep(1)

        # 点击“全部”选项
        self.yys.mouse_click_bg(TansuoPos.quanbu_btn.pos,
                                TansuoPos.quanbu_btn.pos_end)
        ut.time.sleep(1)

        # 点击“N”卡
        self.yys.mouse_click_bg(TansuoPos.n_tab_btn.pos,
                                TansuoPos.n_tab_btn.pos_end)
        ut.time.sleep(1)

        # 更换狗粮
        if gouliang1:
            self.yys.mouse_drag_bg((309, 520), (554, 315))
        if gouliang2:
            ut.time.sleep(1)
            self.yys.mouse_drag_bg((191, 520), (187, 315))

    def find_exp_moster(self):
        '''
        寻找经验怪
            return: 成功返回经验怪的攻打图标位置；失败返回-1
        '''
        # 查找经验图标
        exp_pos = self.yys.find_color(
            ((2, 205), (1127, 545)), (140, 122, 44), 2)
        if exp_pos == -1:
            return -1

        # 查找经验怪攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\FIGHT.png', 1, (exp_pos[0]-150, exp_pos[1]-250), (exp_pos[0]+150, exp_pos[1]-50))
        if not find_pos:
            return -1

        # 返回经验怪攻打图标位置
        fight_pos = ((find_pos[0]+exp_pos[0]-150),
                     (find_pos[1]+exp_pos[1]-250))
        return fight_pos

    def find_boss(self):
        '''
        寻找BOSS
            :return: 成功返回BOSS的攻打图标位置；失败返回-1
        '''
        # 查找BOSS攻打图标位置
        find_pos = self.yys.find_game_img(
            'img\\BOSS.png', 1, (2, 205), (1127, 545))
        if not find_pos:
            return -1

        # 返回BOSS攻打图标位置
        fight_pos = ((find_pos[0]+2), (find_pos[1]+205))
        return fight_pos

    def fight_moster(self, mood1, mood2):
        '''
        打经验怪
            :return: 打完返回True；未找到经验怪返回False
        '''
        while True:
            mood1.moodsleep()
            # 查看是否进入探索界面
            self.yys.wait_game_img('img\\YING-BING.png')
            self.log.writeinfo('In tan-suo field')

            # 寻找经验怪，未找到则寻找boss，再未找到则退出
            fight_pos = self.find_exp_moster()
            if fight_pos == -1:
                fight_pos = self.find_boss()
                if fight_pos == -1:
                    self.log.writeinfo('Monster not found')
                    return False

            # 攻击怪
            self.yys.mouse_click_bg(fight_pos)
            if not self.yys.wait_game_img('img\\ZHUN-BEI.png', 3, False):
                break
            self.log.writeinfo('Already in battle')
            ut.time.sleep(1)

            # 检查狗粮经验
            self.check_exp_full()

            # 点击准备
            self.yys.mouse_click_bg(
                TansuoPos.ready_btn.pos, TansuoPos.ready_btn.pos_end)
            self.log.writeinfo('Clicked ready')

            # 检查是否打完
            self.check_end()
            mood1.moodsleep()

            # 在战斗结算页面
            self.yys.mouse_click_bg(ut.firstposition())
            start_time = ut.time.time()
            while ut.time.time() - start_time <= 10:
                if(self.yys.wait_game_img('img\\YING-BING.png', mood2.get1mood()/1000, False)):
                    return True

                # 点击结算
                self.yys.mouse_click_bg(ut.secondposition())

                # 如果没有成功结算，切到主界面提醒玩家
                if ut.time.time() - start_time > 10:
                    self.yys.activate_window()

    def start(self):
        '''单人探索主循环'''
        mood1 = ut.Mood(1)
        mood2 = ut.Mood()
        while True:
            # 点击挑战按钮
            self.yys.wait_game_img('img\\TAN-SUO.png')
            self.yys.mouse_click_bg((785, 456), (894, 502))

            # 开始打怪
            i = 0
            while i < 4:
                result = self.fight_moster(mood1, mood2)
                if result:
                    continue
                else:
                    self.log.writeinfo('Going to next scene')
                    self.next_scene()
                    i += 1

            # 退出探索
            while True:
                self.yys.mouse_click_bg(
                    TansuoPos.quit_btn.pos, TansuoPos.quit_btn.pos_end)
                if self.yys.wait_game_img('img\\QUE-REN.png', 3, False):
                    break
            self.yys.mouse_click_bg(
                TansuoPos.confirm_btn.pos, TansuoPos.confirm_btn.pos_end)
            self.log.writeinfo('Quit this cycle')
