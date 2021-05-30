#!/usr/bin/python
#-*- coding:utf-8 -*-
import sys
sys.path.append("../")
import ai
import file,tool,cvhelp,time
import same

# icbc 自动化 定时登录刷新session
class Auto:
    def __init__(self, name="Test", path='td', img_channels_rgb=3, widthHeight=None, test_all=True, tempDir='./__pycache__'):
        self.name = name
        self.tempDir = tempDir
        self.tempDirCapture = self.tempDir + '/' + self.name
        file.mkdir(self.tempDirCapture + "/test.png")
        self.data, self.mapp, self.keys = ai.loadAutoImg(dirpath='./td')
        tool.out(self.keys)
        self.now = None
        self.dealtaMax = 1600
        self.lastAction = ''
        return
    # 日志输出
    def out(self, obj):
        tool.out(obj)
        return
    # 实时控制帮助
    def help(self):
        self.out(dir(self))
        return
    # doMethod([methodName arg1 arg2]) -> methodName(arg1,arg2)
    def doMethod(self, listArgs):
        size = len(listArgs)
        res = None
        if(size > 0):
            if(hasattr(self, listArgs[0])):
                method = getattr(self, listArgs[0])
                if(callable(method)):
                    if(size == 2):
                        res = method(listArgs[1])
                    elif(size == 3):
                        res = method(listArgs[1], listArgs[2])
                    elif(size == 4):
                        res = method(listArgs[1], listArgs[2], listArgs[3])
                    elif(size == 5):
                        res = method(listArgs[1], listArgs[2], listArgs[3], listArgs[4])
                    else:
                        res = method()
                else:
                    self.out(method)
        return res
    # 手动命令监控
    def inputHello(self):
        self.out("开启输入监控！")
        self.help()
        while(True):
            tool.sleep(1)
            try:
                cmd=input("")
                if(cmd != ""):
                    if(not self.doMethod(cmd.split(" "))):
                        self.doCmd(cmd)
                        tool.sleep(1)
            except Exception as e:
                self.out(repr(e))
        return
    # 测试用
    def test(self):
        # 输入监控线程
        tool.ThreadRun("InputHello." + str(self.name), self.inputHello).start()
        tool.ThreadRun("Action." + str(self.name), self.action).start()
        while True:
            tool.sleep(1000)
        return
    # 非函数调用 属性变量查看 其他的指令控制
    def doCmd(self, cmd):
        self.out("其他指令." + str(cmd))
        eval(cmd)
        return
    def action(self):
        if(self.now == None):
            self.now = '1home'

        if(self.now == '6make'):
            self.mapRunStart()


        dealta2, tocenter = self.checkNowOk(self.now, filepath=None)
        if (dealta2 < self.dealtaMax):  # 命中
            tool.mouseClickKeep(tocenter[0], tocenter[1])
            tool.out("命中", self.now)
            self.now = self.keys[int((self.keys.index(self.now) + 1) % len(self.keys))]
        else:
            tool.out("无效识别", self.now)
            if(tool.getRandom(1, 10) > 5):
                self.now = self.keys[int((self.keys.index(self.now) + 1) % len(self.keys))]
        self.action()
    def getBack(self, direct):
        if (direct == 0):
            directBack = 2
        if (direct == 1):
            directBack = 3
        if (direct == 2):
            directBack = 0
        if (direct == 3):
            directBack = 1
        return directBack
    def move(self, direct=0 ):
        # 尝试移动重复的不再走
        xy = (self.xy[0] + self.directs[direct][0], self.xy[1] + self.directs[direct][1]) #移动成功时的坐标
        if (self.mapAll[xy[0]][xy[1]] > 0):
            tool.out("已经走过!!!", direct, self.mapAll[xy[0]][xy[1]])
            return

        tool.mouseClickMoveToKeep(720 / 2, 1280 / 2, self.directs[direct][0]*40, self.directs[direct][1]*40, 0.2)
        tool.sleep(0.2)
        tool.out('mouseMove', self.directs[direct])

        # 检测结果
        imgStatus, filepath = self.getStatusImg()
        sames = same.sameCompare(self.imgStatusLast, imgStatus)
        self.imgStatusLast = imgStatus

        tool.out(sames)
        # 2021-03-28 18:02:44 ((array([0.9997676], dtype=float32), array([0.99984497], dtype=float32), 0, 0),)
        # 2021-03-28 18:05:14 ((array([0.92578685], dtype=float32), array([0.91144425], dtype=float32), 3, 9),)
        if (sames[2] == 0 and sames[3] == 0):  # 相同 没走  tool.getRandom(0, 10) > 5
            # 走失败了
            # 是否是在打怪 则等一会儿 否则转方向
            dealta2, tocenter = self.checkNowOk('6make-back', filepath=filepath)
            if (dealta2 < self.dealtaMax):  # 打怪中
                # tool.mouseClickKeep(tocenter[0], tocenter[1])
                tool.out("行走失败 打怪 等待 打怪完毕 可释放技能")
                # self.mapAll[xy[0]][xy[1]] = 168 #怪标记

                while True:
                    tool.sleep(3)
                    dealta2, tocenter = self.checkNowOk('6make-back', filepath=filepath)
                    if (dealta2 < self.dealtaMax):  # 有效操作
                        tool.out("行走失败 打怪 等待 打怪完毕 可释放技能1")
                    else:
                        tool.out("打完怪了")
                        break
                self.move(direct) #重走？
            else: #非打怪则不懂就是撞墙
                tool.out("行走失败 撞墙了")
                self.mapAll[xy[0]][xy[1]] = 256 #墙标记
                return
        else: # 不同 成功的迈出了一步
            self.stack.append(direct)
            #     有效移动 记录地图
            directBack = self.getBack(direct)
            self.xy = xy
            self.mapAll[xy[0]][xy[1]] = 128  # 空位置标记
            dealta2, tocenter = self.checkNowOk('ok', filepath=filepath)
            if (dealta2 < self.dealtaMax):
                tool.mouseClickKeep(tocenter[0], tocenter[1])
                tool.out("确认进入下一楼")
                self.mapAll[xy[0]][xy[1]] = 200  # 标记出口
                tool.out("保存地图?")
                # cvhelp.save(self.mapAll,  self.tempDirCapture + '/map-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.png')
                tool.sleep(5)
                self.flag = True
            else:
                tool.out("行走成功,先继续走", direct)
                self.move(direct)

                for nd in range(len(self.directs)):
                    directNew = int((direct + nd) % len(self.directs))
                    if (self.flag):
                        break
                    if (directNew != direct and directNew != directBack):  # 不是走过的 和回头走过的
                        xy = (self.xy[0] + self.directs[directNew][0], self.xy[1] + self.directs[directNew][1])
                        if(self.mapAll[xy[0]][xy[1]] > 0 ):
                            tool.out("已经走过 行走支路取消", directNew, 'not', direct, directBack)
                        else:
                            tool.out("行走支路", directNew, 'not', direct, directBack)
                            self.move(directNew)

                if (not self.flag): #每次成功后一定有回退
                    last = self.stack.pop()
                    lastBack = self.getBack(last)
                    tool.out("出栈 回退移动", last, '->', lastBack, '=?=', directBack, 'of', self.stack)
                    # self.move(directBack)
                    # 尝试移动 一定成功
                    tool.mouseClickMoveToKeep(720 / 2, 1280 / 2, self.directs[lastBack][0] * 40,
                                              self.directs[lastBack][1] * 40, 0.2)
                    xy = (self.xy[0] + self.directs[lastBack][0], self.xy[1] + self.directs[lastBack][1])
                    self.xy = xy
                    tool.sleep(0.2)
                    tool.out('mouseMoveBack', self.directs[lastBack])

    def getStatusImg(self):
        statusRect = self.mapp['6make-map-status']['rects'][0]  # 状态矩形框
        filepath = tool.screenCapture(
            self.tempDirCapture + '/' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.png')
        cvhelp.save(filepath, cvhelp.totateClockWise90ByNumpy(cvhelp.open(filepath)))
        imgStatus = cvhelp.open(filepath)[statusRect[1]:statusRect[3], statusRect[0]:statusRect[2]]
        return imgStatus, filepath
    #
    def mapRunStart(self):
        tool.out('开始地图算法')
        # 清空堆积递归
        # 记录第一次的状态
        self.flag = False
        self.stack = []
        self.imgStatusLast, filepath = self.getStatusImg()
        self.directs = [
              (1, 0)
            , (0, 1)
            , (-1, 0)
            , (0, -1)
        ]
        w = 1000
        h = 1000
        import numpy as np
        self.mapAll =  np.zeros((w, h)) # cvhelp.getBinary(cvhelp.createImage(width=w, height=h, rgb=(0,0,0)))
        # 使用随机生成黑森林，定位于中心，每位于一个点 递归实现右上下左移动，遇墙跳过
        self.xy = (int(w/2), int(h/2))
        self.mapAll[self.xy[0]][self.xy[1]] = 16  # 标记七点

        for nd in range(len(self.directs)):
            if(self.flag):
                break
            self.move(nd)
        self.mapRunStart()
        # cvhelp.save(self.mapAll, self.tempDirCapture + '/map.' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.png' )
    # 返回距离小于1异常 目标中心
    def checkNowOk(self, now='home1', filepath=None):
        if(filepath == None):
            filepath = tool.screenCapture(
                self.tempDirCapture + '/' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.png')
            cvhelp.save(filepath, cvhelp.totateClockWise90ByNumpy(cvhelp.open(filepath)))
            # tool.out("capture", filepath)
        fromrect = self.mapp[now]['rects'][0]
        fromcenter = ((fromrect[0] + fromrect[2]) / 2, (fromrect[1] + fromrect[3]) / 2)
        torect = cvhelp.findImg(cvhelp.open(filepath), self.mapp[now]['imgs'][0], text=now, tempFile=filepath)
        torect = torect[0] if len(torect) > 0 else [0, 0, 0, 0]
        tocenter = ((torect[0] + torect[2]) / 2, (torect[1] + torect[3]) / 2)
        #         矩形相似距离阈值
        dealta2 = (tocenter[0] - fromcenter[0]) * (tocenter[0] - fromcenter[0]) + (tocenter[1] - fromcenter[1]) * (
                    tocenter[1] - fromcenter[1])
        tool.out(now, fromrect, 'torect', torect, 'dealta', dealta2, 'file', self.mapp[now]['filepath'])
        if (torect[0] == 0 and torect[1] == 0 and torect[2] == 0):
            tool.out("error ? ")
            dealta2 = -1
        return dealta2, tocenter

if __name__ == '__main__':
    obj = Auto("Test")
    # obj.test()
    obj.mapRunStart()
