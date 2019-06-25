import win32com.client 
import sys 
import os
import ctypes
import threading

import fighter_driver
import fighter_passenger
import logsystem
import single_fight

# 设置
global mode
global emyc
global done

#初始化对象
log = logsystem.WriteLog()

def init():
    global mode
    global emyc
    global done
    
    try:
        # 模式选择
        mode=int(input('\n选择游戏模式(Ctrl-C跳过并单刷)：\n0-单刷\n2-组队司机\n3-组队打手\n'))
        if(mode==1):
            log.writewarning('未开发，告辞！')
            os._exit(0)
        elif(mode != 2 and mode != 0 and mode != 3):
            mode=0
        
        # 点怪设置
        # emyc=int(input('\n是否点怪？\n0-不点怪\n1-点中间怪\n2-点右边怪\n'))
        # if((emyc!=0) and (emyc!=1) and (emyc!=2)):
        #     emyc=0
        
        # 结束设置
        # done=int(input('\n结束后如何处理？\n0-退出\n1-关机\n'))
        # if not ((done == 0) or (done == 1)):
        #     done = 0
        log.writeinfo('Mode = %d',mode)
        # log.writeinfo('Emyc = %d',emyc)
        # log.writeinfo('Postoperation = %d',done)
    except:
        mode=0
        emyc=0
        done=1
        log.writeinfo('Use default parameters')

def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def yuhun():
    '''御魂战斗'''
    if mode == 0:
        # 单刷
        fight = single_fight.SingleFight()
        fight.start()
    
    if mode == 2:
        # 司机
        fight = fighter_driver.DriverFighter()
        fight.start()
    
    if mode == 3:
        # 乘客
        fight = fighter_passenger.FighterPassenger()        
        fight.start()    

if __name__ == "__main__":    
    log.writeinfo('python version: %s', sys.version)
    
    try:
        # 检测管理员权限
        if is_admin():
            # 注册插件，获取权限
            log.writeinfo('UAC pass')            

            # 设置战斗参数
            init()

            # 开始战斗              
            yuhun()

        else:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)       
    except KeyboardInterrupt:        
        log.writeinfo('terminated')
        os._exit(0)
    else:
        pass