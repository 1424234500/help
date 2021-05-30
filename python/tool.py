#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json
import os
import subprocess
import re
import sys
import time
import traceback
import uuid
import threading
import random
import tempfile

import numpy as np

# from self import s
# sys.path.append("../opencv/")
# from filename import classname

"""
	python基本语法及其工具汇总测试 仅依赖基础env
	规范语法 3.7优先 尽量兼容
	4个空格 \t
"""

# 全局常量 大写
PI = 3.14159


def test():
	testData()
	testFun()


def evalWithPrint(code, *objs):
	print(str(objs[0]) + ' eg: \t' + code + '\t -> \t' + str(eval(code)))


def testFun():  # 函数
	"""
	函数式编程 函数指针参数传递
	常用函数
	"""
	out("函数")
	abcSelf = abs
	print("函数指针参数传递", abcSelf(-1))
	print("装饰器测试2 注解", aopLogTestDevide(a=2, b=4))
	print("装饰器测试1 注解", aopLogTestDevide(a=1, b=0))
	evalWithPrint("isinstance('abc', str)", '反射 类型判断')
	out('动态参数 fun(*objs, **kwargs) ', config01=1, config02=2)


def testData():  # 数据结构 dict list 分支循环 if for while
	"""
	动态类型 任意整数 可_分隔可视化 r''强字符串
	"""

	out("数据定义 str() int() ")
	aint = - 1_000_000.02e-9 + 0X23 + 0x12
	aintn = int('12345', base=8)
	bstr = 'I\'m " ok ' + "so \n you're \" ok" + r" \a ti'm ok\n " + '''
		line1
		line2
	'''
	cbool = True and False or not 1 > 0
	dbyte = b'abc'  # ascii 中文超范围异常

	print(aint, aintn, bstr, cbool, dbyte)

	out("数学运算")
	evalWithPrint(r'10 / 3', '浮点/')
	evalWithPrint(r'10 // 3', '地板除floar')
	evalWithPrint(r'10 % 3', '%')
	evalWithPrint(r'2 & 3', '&')
	evalWithPrint(r'2 ^ 3', '^')
	evalWithPrint(r'hex(5)', '&')

	out("字符串 +需转换str")
	evalWithPrint("ord('中')", '编码 十六进制写中文\u4e2d ')
	evalWithPrint("chr(20013)", '解码')
	evalWithPrint("'abc'.encode('ascii')", 'encode ascii')
	evalWithPrint("'中文'.encode('utf-8')", 'encode utf-8')
	evalWithPrint("'中文'.encode('gb2312')", 'encode gb2312')
	out("字符串占位符替换 %d,  %f %%, %s, %x, %s" % (1, 2.3, 'str', 4, True))

	evalWithPrint("' a '.strip()", 'str.strip')
	evalWithPrint("'abc'.find('b')", 'str.find')
	evalWithPrint("'abc'.replace('b', 'x')", 'str.replace')
	evalWithPrint("'abc'.index('b')", 'str.index ')

	evalWithPrint("re.search(r'\d+','a12b34c').group()", 'str.regex')
	evalWithPrint("re.findall(r'\d+','a12b34c')", 'str.regex')
	evalWithPrint("re.split(r'b','b2b3b')", 'str.split')

	out("集合")
	evalWithPrint(" [x * x if x > 0 else -1 for x in range(1,4) if x < 4] ", '简写生成 序列 后置过滤 前置三目 [1,4,9]   ')
	evalWithPrint(" [x * x for x in range(1,4)] ", '遍历处理fun 1  ')
	evalWithPrint(" list(map( lambda x: x * x, range(1,4) )) ", '遍历处理fun 2 map 惰性序列 ')
	if version3():
		from functools import reduce
	rres = reduce(lambda x1, x2: x1 + x2, range(1, 4))
	print(
		'遍历处理fun 3 reduce 累计处理 f(f(f(x1,x2),x3),x4)  python3 -> from functools import reduce ' + ' eg: \t' + 'reduce( lambda x1,x2: x1+x2, range(1,4) )' + '\t -> \t' + str(
			rres))
	evalWithPrint(" list(filter( lambda x: x > 1, range(1,4) )) ", '遍历处理fun 4 filter 惰性序列 ')

	evalWithPrint(" [str(a) + str(b) for a in range(2) for b in range(1,3)] ", '多维组合 [11,12,21,22] ')
	evalWithPrint(" (x * x for x in range(10)) ", 'generator生成器() yield resItem -> next(gen) for in  ')

	evalWithPrint(" sorted([{'name': 'a', 'age': 18}], key=lambda x: x['age'], reverse=False) ", ' 排序 ')

	print("""
	词典 dict->map {'a': {'name':'a','age':18} }
		.hash_key('a')
		.keys()
		.values()
		.items() -> entrySet
		.clear()
		.copy() -> clone
		.get('a', default=None)
		dict['a']
		
	元组 tuple = tuple(list) (1,2,3)
	数组 list = list(tuple) [1,2,3] arr[0] 
		序号 -1->len-1
		.clear()
		.append(obj) 
		.insert(1, obj)
		.pop(num=1)
		.extend(b) -> addAll
	数组截取 
		arr[0:3, 1:2:1, 2:4:2]
		分维度 :分片
		二维数组
		X[:, n] 每行 第n列 -> [n0,n1,...,nn]
		X[:, 1:] 每行 第1列起 -> [na,...,nn]
		X[1, :] 第1行
		X[:2, 1:] 第2行截止 第1列开始
		X[a:b:k, c:d:k] 行a->b, 列c->d
		k可选默认1 步长 -1则反向
		0=a<b=X.len
		0=c<d=X[0].len
		-n -> len - n
	
	分支
	if (True):
		pass
	else
		pass
	fi
	三目运算
	1 if True else 0
	
	循环
	
	for char in 'python':
	for i in range(len(arr)):
		print(i)
	else:
		print('for else') #for正常退出
	while(True):
		break;
		continue;
		
	""")


def version3():  # 兼容代码查看环境版本
	return sys.version > '3'


def aopLog(func):  # 装饰器 详细函数输入输出日志
	"""
	aop log before after cost 局限? 参数格式问题?
	"""

	def wrapper(*args, **kw):
		st = timeGet()
		info = 'call %s(%s, %s) -> ' % (func.__name__, str(args), str(kw))
		res = None
		try:
			res = func(args, kw)
		except Exception as e:
			info += ' error ' + str(traceback.format_exc())
			raise e
		else:
			info += ' ok '
		finally:
			info += " res-> " + str(res) + " cost " + str(timeGet() - st)
			print(info)
		return res

	return wrapper


@aopLog
def aopLogTestDevide(*args, **kwargs):
	return kwargs[0] / kwargs[1]


def getValue(map={}, defaultValue=None, *keys):  # 多key优先获取值
	"""
	getValue(map, 'hello', 'key1', 'key2') -> value
	"""
	for key in keys:
		if key in map and map[key] is not None:
			return map[key]
	return defaultValue


def showList(name='info list', arr=[1, 2, 3, 4, 5], eg='eg', size=3):  # list -> info
	s = name + ' len ' + str(len(arr)) + ' ' + eg
	for i in range(len(arr)):
		if i < size or i > len(arr) - size or len(arr) < 2 * size:
			s += ' ' + str(arr[i])
		if i == size:
			s += '...'
	return s


def makeByte(img):  # img二维数组 压缩 value=0-255 100/height 1字节Byte = 8bit = 256编码  16进制2位 2f
	res = ''
	for row in img:
		for col in row:
			res += hex(col)[2:4]
	return res


def getRandomWeight(start=0, stop=5, step=3):  # 按权重分配随机数选择器 1024 512 ... 1
	size = stop - start  # 5	2^5=32-1=31=16 8 4 2 1 ->
	area = []
	cc = 1
	for i in range(size):  # 0, 1, 2, 3, 4
		for j in range(cc):  # 1, 2, 4, 8, 16   1 3 9 27
			area.append(i)  # 0, 1,1, 2,2,2,2, 3,3,3,3,3,3,3,3,
		cc = cc * step
	ran = int(random.uniform(0, len(area)))  # getRandom(0, len(area)) # 0,1,2
	res = size - 1 - area[ran]  # 0,1 -> 1,0
	return res


def getRandom(start=0, stop=10):  # 伪造真随机数
	if start < 0:
		start = 0
	if stop <= start:
		stop = start + 1
	msec = timeGet() + int(random.uniform(0, 100))
	# 时间轴 毫秒+随机数100 投影到目标区间
	return int(msec % (stop - start) + start)


def getUuid():  # uuid
	return (str(uuid.uuid1())).split("-")[0]


def encode(string):  # 编码问题
	"""
	内存 unicode
	文件 utf-8
	"""
	t = type(string)
	res = string
	if t == "unicode":
		res = res.encode('utf-8')
	elif t == int:
		pass
	else:
		pass
	return res


def makeObj(data):  # 递归转换对象词典 为 utf encode 避免Unicode!
	if isinstance(data, list):
		return [makeObj(item) for item in data]
	if isinstance(data, dict):
		res = {}
		for key, value in data.iteritems():
			res[encode(key)] = makeObj(value)
		return res
	return encode(data)


def toJson(jsonStr):  # 通过字符串 解析为json 并编码 Unicode
	if isinstance(jsonStr, dict):
		return makeObj(jsonStr)
	if jsonStr == None or jsonStr == "":
		return {}
	if type(jsonStr) is str and jsonStr.strip()[0:1] != "{" and jsonStr.strip()[0:1] != "[":
		return {"error": jsonStr}
	# json.loads(jsonStr) 针对单引号问题ast.literal_eval(jsonStr)
	return makeObj(json.loads(jsonStr))


def getClassName(cla, value=[], defValue=None):  # 获取某个模块或者 class 值为value的变量名
	keys = dir(cla)
	for key in keys:
		ret = hasattr(cla, key)
		if ret:
			method = getattr(cla, key)  # 获取的是个对象
			for v in value:
				if v == method:
					return key
	return defValue


def exe(str):  # exe('ll')
	# (status, output) = commands.getstatusoutput(str)
	print('>>>>exe', str)
	return os.popen(str).read().encode('utf-8')


def call(strr): # exe without parent
	print('>>>>call', strr)
	res = subprocess.Popen("" + strr + "", shell=True, close_fds=True)
	res = res.wait()
	out(">>>>call res", strr, res)
	return res


def call2(strr):
	print('>>>>call', strr)
	try:
		out_temp = tempfile.TemporaryFile(mode='w+')
		fileno = out_temp.fileno()
		p = subprocess.Popen(strr, shell=True, close_fds=True, stdout=fileno, stderr=fileno)
		p.wait()
		out_temp.seek(0)
		rt = out_temp.read()
		rt_list = rt.strip().split('\n')
	except Exception as e:
		print(traceback.format_exc())
	else:
		print('exe ok normal ')
	finally:
		if out_temp:
			out_temp.close()
	print(rt_list)
	return rt_list


def doMethod(cls, methodName, *params):  # 反射 do the method of the class, *params动态参数 元组 也可以作为动态参数传递
	print('# do method')
	print("class:  " + cls.__class__.__name__)  # className
	print("dir: " + cls.__class__)
	print("method: " + methodName)  # list
	print("params: " + str(params))  # {arg1: 'a1', arg2: 'a2' }
	# 检查成员
	ret = hasattr(cls, methodName)  # 因为有func方法所以返回True
	if (ret == True):
		# 获取成员
		method = getattr(cls, methodName)  # 获取的是个对象
		if callable(ret):
			return method(*params)
		else:
			return method
	else:
		print("Error! 该方法不存在")
	return ''


def sleep(mills):
	time.sleep(mills)


def timeGet():  # time 199313231000
	return int(time.time() * 1000)


def timeFormat(timeStamp=199313231000, format="%Y-%m-%d %H:%M:%S"):  # %a %b %d %H:%M:%S %Y -> Sat Mar 28 22:24:24 2016
	return time.strftime(format, time.localtime(timeStamp))


def line():
	print("--------------------------------")


def fill(argStr, char=' ', toLen=10):  # 补齐长度
	length = len(argStr)
	charLen = len(char)
	for i in range((toLen - length) / charLen):
		argStr = argStr + str(char)
	return argStr


def calcTime(mills=60000): # 2h 3m 10s 203ms
	mills = int(mills)
	levh = 60 * 60 * 1000
	levm = 60 * 1000
	levs = 1000
	if (mills / levh > 0):
		res = str(mills / levh) + "h" + str(mills % levh / levm) + "m"
	elif (mills / levm > 0):
		res = str(mills / levm) + "m" + str(mills % levm / levs) + "s"
	elif (mills / levs > 0):
		res = str(mills / levs) + "s" + str(mills % levs / 1) + "ms"
	else:
		res = str(mills) + "ms"
	return res


def out(*objs, **kwargs):# 日志 动态参数键值
	print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), objs)
	if (kwargs != None and len(kwargs) > 0):
		print(kwargs, type(kwargs))


def setFileList(filePath, listData=[1, 2, 3]): # 文件存储 数据 保存list
	np.save(filePath, listData)


def getFileList(filePath):
	return np.load(filePath)


def setFileJsonObj(filePath, data):  # ('1', ('2', '3'))
	with open(filePath, 'w') as f:
		json.dump(data, f)


def getFileJsonObj(filePath): # ['1', ['2', '3']]
	data = None
	with open(filePath, 'r') as f:
		data = json.load(f)
	return data


def predict_proba_to_class(classes=[2, 1, 3], predict=[[0.3, 0.1, 0.2], [0.8, 0.6, 0.2], ], top=None, p=6, points=[]):  # [ [(1, 0.2, {l,w,h,t}), (2, 0.3, {}), (3, 0.5, {})], ]
	res = []

	for index in range(len(predict)):
		point = points[index] if points != None and len(points) > index else None
		item = predict[index]
		resi = []
		for i in range(len(classes)):
			if (type(classes) == 'list'):
				strRes = classes[i]
			else:
				strRes = classes[str(i)]
			if p is None:
				resi.append((strRes, item[i], point))
			else:
				resi.append((strRes, round(item[i], p), point))
		resi = sorted(resi, key=lambda x: x[1], reverse=True)
		if (top != None and len(resi) > top):
			resi = resi[0:top]
		res.append(resi)

	all = []
	for item in res:
		for iitem in item:
			all.append(iitem)
	alli = sorted(all, key=lambda x: x[1], reverse=True)
	if (alli != None and len(alli) > top):
		alli = alli[0:top]

	return res, alli

# 系统工具截图
def screenCapture(filepath='./capture.png', bbox=(0, 0, 576, 982)):
    from PIL import ImageGrab
    from PIL import Image
    # 参数说明
    im = ImageGrab.grab(bbox)
    a=im.transpose(Image.ROTATE_90)
    a.save(filepath)
    return filepath

#鼠标键盘
def mouseClickKeep(x=100, y=100, count=1, interval=0.05, button='left'):
    import pyautogui
    lx, ly = pyautogui.position()
    mouseClick(x, y, count, interval, button)
    mouseMoveTo(lx, ly, 0.001)
def mouseClick(x=100, y=100, count=1, interval=0.05, button='left'):
	import pyautogui
	# out('mouseClick', x, y, count, interval, button)
	pyautogui.click(x = x, y = y, clicks=count, interval=interval, button=button)
def mouseMoveTo(x = 600, y = 600, duration=3.5):
	import pyautogui
	# out('mouseMoveTo', x, y,  duration)
	pyautogui.moveTo(x=x, y=y, duration=duration)
def mouseClickMoveTo(x = 300, y = 300, duration=2.5):
	import pyautogui
	# out('mouseClickMoveTo', x, y,  duration)
	pyautogui.dragTo(x=x, y=y, duration=duration)
def mouseClickMoveToKeep(xfrom = 300, yfrom = 300, dx=10, dy=10, duration=0.5):
    import pyautogui
    lx, ly = pyautogui.position()
    mouseMoveTo(xfrom, yfrom, 0.001)
    mouseClickMoveTo(xfrom+dx, yfrom+dy, duration)
    mouseMoveTo(lx, ly, 0.001)

class ThreadRun(threading.Thread):  # 线程操作类
	"""
	ThreadRun( "InputHello.",  inputHello ).start()
	"""
	def __init__(self, name, runCallback, daemon=True):
		threading.Thread.__init__(self)
		self.name = name
		self.runCallback = runCallback
		self.setDaemon(daemon)  # 子线程随主线程退出

	def run(self):
		print("============Thread Start " + self.name)
		self.runCallback()
		print("============Thread Stop  " + self.name)


if __name__ == '__main__':
	res = {}
	cc = 1000
	ss = 5
	for i in range(cc):
		geti = getRandomWeight(0, ss)
		res[str(geti)] = res.get(str(geti), 0) + 1
	print(res)
	# print(predict_proba_to_class(top=2))
	# test()
	print(screenCapture)
	mouseClick()
	mouseClickMoveTo()
	mouseMoveTo()
