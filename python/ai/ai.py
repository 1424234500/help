#!/usr/bin/env python
#-*- coding:utf-8 -*-

import json
import sys
sys.path.append("../")

import numpy as np
from sklearn.model_selection import train_test_split
import glob as gb
from sklearn import datasets

import file,tool,cvhelp




# def loadData(path='./number-predict', img_channels_rgb=3, widthHeight=(20,40), test_size=0.001, test_all=False, shuffle=True):
def loadDefaultDataDigits(test_size=0.001, shuffle=True):
	name = 'digits'
	info = '手写数字 1797个 每个图像为8*8像素 一维'
	digits = datasets.load_digits()
	x_train = digits.data
	y_train = digits.target
	tool.out(name, '', digits.images[0])
	return loadDataMake(name=name, info=info, x_train=x_train, y_train_NoOneHot=y_train, test_size=test_size, shuffle=shuffle)
	
# 训练数据
def loadDataMake(name='testData', info='测试造数', x_train=[], y_train_NoOneHot=[], test_size=0.001, shuffle=True, test_all=False):
	y_train = []
	y_train_filepath = []
	
	x_test = []
	y_test = []
	y_test_NoOneHot = []
	y_test_filepath = []
	
	mapRes = {}
	mapRes['map'] = {}
	mapRes['point'] = [{"left": 0, "top": 0, "width": 1, "height": 1}]
	
	for item in y_train_NoOneHot:
		mapRes['map'][item] = item
	tool.out(name, info)
	tool.out(name, 'labels', y_train_NoOneHot, '# [0, 1, 2, ..., 8, 9, 8]')
	tool.out(name, 'samples', x_train[:1], '# [  [0,1] , [2, 3] , ... , [19, 20]  ]')
	tool.out('# 加载数据 原样本', len(x_train), len(y_train_NoOneHot))
	from keras.utils import np_utils
	y_train = np_utils.to_categorical(y_train_NoOneHot, len(mapRes['map'].keys()))  # One-Hot encoding
	y_train_filepath = np.array(y_train_NoOneHot)
	
	if (test_size > 0):
		x_train, x_test, y_train, y_test, y_train_NoOneHot, y_test_NoOneHot, y_train_filepath, y_test_filepath = train_test_split(
			x_train, y_train, y_train_NoOneHot, y_train_filepath, test_size=max(1, round(len(x_train) * test_size)),
			shuffle=shuffle)
	if (test_all == True):
		x_test = x_train
		y_test = y_train
	
	tool.out('----load data-----')
	mapRes['point'] = dupList(mapRes['point'])
	tool.out(tool.showList('point', arr=mapRes['point'], size=4))
	tool.out(tool.showList('x_train', arr=x_train, size=0))
	tool.out(tool.showList('y_train', arr=y_train))
	tool.out(tool.showList('y_train_NoOneHot', arr=y_train_NoOneHot))
	tool.out(tool.showList('y_train_filepath', arr=y_train_filepath))
	
	return np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test), np.array(
		y_train_NoOneHot), np.array(y_test_NoOneHot), y_train_filepath, y_test_filepath, mapRes


# 获取类别数
def loadDirImageClassesSize(path='./number-predict'):
	return len(gb.glob(path + "/*"))

#去重 小数点
def dupList(arr=[], p=4):
	res=[]
	map = {}
	for item in arr:
		ik = 'k'
		for key in item.keys():
			i = round(item[key], p)
			i = i if i <= 0.99 else 1
			i = i if i >= 0.01 else 0
			ik += '-' + key + '=' + str(i)
		map[ik] = item
	for key in map.keys():
		res.append(map[key])
	return res
	
# 多key优先获取值
def getValue(map={}, defaultValue=None, *keys):
	for key in keys:
		if key in map:
			if map[key] != None:
				return map[key]
	return defaultValue

# x_train, x_test, y_train, y_test, y_train_NoOneHot, y_test_NoOneHot, y_train_filepath, y_test_filepath, mapRes = ai.loadDirImage(path=path, img_channels_rgb=img_channels_rgb, widthHeight=widthHeight, test_size=test_size, shuffle=True)
#
# x_train : x轴 samples 图片数组	[ [20x40], ...]
# y_train :应的 labels 编码 onhot
# y_train_NoOneHot : 对应的 labels 未编码 序号 0 -> len(classes) [0, 1, 1, ...]
# y_train_filepath : 每个label对应的文件全路径 [ './a.png', './b.png', ...]
#
# mapRes : 序号->字符串 结果集映射 { map:{'0': '0', '1': '1', '2': '2'}, point:[{'left'@0.1,'top'@0.1,'width'@0.2,'height'@0.2}, {'left'@0.1,'top'@0.1,'width'@0.2,'height'@0.2} ] }
#
def loadDirImage(path='./number-predict', img_channels_rgb=3, widthHeight=(20,40), test_size=0.001, test_all=False, shuffle=True):
	x_train = []
	y_train = []
	y_train_NoOneHot = []
	y_train_filepath = []
	
	x_test = []
	y_test = []
	y_test_NoOneHot = []
	y_test_filepath = []


	mapRes = {}
	mapRes['map'] = {}
	mapRes['point'] = [{"left": 0, "top": 0, "width": 1, "height": 1}]

	idf = file.getDirDirNames(path)
	for idfItem in idf:
		index = idfItem['index']
		dirname = idfItem['dirname']
		files = idfItem['files']
		mapRes['map'][str(index)] = dirname
		for fileName, filepath in files:
			# 资源标记问题 @ : 一图多框 多框标记 兼容百分比例换算 属性预算 兼容自检 切图
			# +!@#$%^&()_+
			#{'name'@'xxxx','width'@200,'height'@300,'point'@[{'x'@102,'y'@18,'w'@22,'h'@36,'left'@0.1,'top'@0.1,'width'@0.2,'height'@0.2},{'x'@159,'y'@75,'w'@28,'h'@42}]}.jpg
			jsonstr = file.getFilePath(fileName)[1]
			if(jsonstr.startswith('{') and jsonstr.endswith('}')):
				pass
			else:
				jsonstr = '{"name":"' + jsonstr + '"}'
			obj = json.loads(jsonstr.replace('@', ':').replace('\'', '"'))
			imgBig = cvhelp.open(filepath, img_channels_rgb)
			name = getValue(obj, fileName, 'name')
			wbig = getValue(obj, 0, 'width')
			hbig = getValue(obj, 0, 'height')
			if wbig <= 0 or hbig <= 0:
				(wbig,hbig) = cvhelp.getWidthHeight(imgBig)
			for pointItem in getValue(obj, [{}], 'point'):
				x = getValue(pointItem, getValue(pointItem, 0, 'left') * wbig, 'x')
				y = getValue(pointItem, getValue(pointItem, 0, 'top') * hbig, 'y')
				w = getValue(pointItem, getValue(pointItem, 1, 'width') * wbig, 'w')
				h = getValue(pointItem, getValue(pointItem, 1, 'height') * hbig, 'h')

				tool.out(name, x, y, w, h)
				# 记录案例框
				mapRes['point'].append({"left":x/wbig,"top":y/hbig,"width":w/wbig,"height":h/hbig})
				
				img = imgBig[y:y+h, x:x+w]

				# ttt = './td/' + name + '/' + fileName
				# print(ttt)
				# cvhelp.save(ttt, imgBig)

				if(widthHeight != None):
					img = cvhelp.resizeKeep(img, widthHeight=widthHeight)
				x_train.append(img)
				y_train.append(index)
				y_train_NoOneHot.append(dirname)
				y_train_filepath.append(filepath)
	from keras.utils import np_utils
	y_train = np_utils.to_categorical(y_train, len(mapRes['map'].keys()))  # One-Hot encoding
	# y = np.argmax(Y, axis=-1)
	
	if test_all:
		x_test = x_train
		y_test = y_train
		y_test_NoOneHot = y_train_NoOneHot
		y_test_filepath = y_train_filepath
	elif test_size > 0:
		x_train, x_test, y_train, y_test, y_train_NoOneHot, y_test_NoOneHot, y_train_filepath, y_test_filepath = train_test_split(
			x_train, y_train, y_train_NoOneHot, y_train_filepath, test_size=max(1, round(len(x_train) * test_size)),
			shuffle=shuffle)
	tool.out('----load data-----')
	mapRes['point'] = dupList(mapRes['point'])
	tool.out(tool.showList('point', arr=mapRes['point'], size=4))
	tool.out(tool.showList('x_train', arr=x_train, size=0))
	tool.out(tool.showList('y_train', arr=y_train))
	tool.out(tool.showList('y_train_NoOneHot', arr=y_train_NoOneHot))
	tool.out(tool.showList('y_train_filepath', arr=y_train_filepath))

	return np.array(x_train), np.array(x_test), np.array(y_train), np.array(y_test), np.array(y_train_NoOneHot), np.array(y_test_NoOneHot), y_train_filepath, y_test_filepath, mapRes

# data, mapp, keys = ai.loadAutoImg(dirpath='./td')
# [
#   { name:aaaa, rects:[(left,top,right,bottom)], imgs[img1,img2], wh:(w, h), filename:{aaxsfas}.png, filepath:xxxx}
# ]
# name index
# keys sorted
def loadAutoImg(dirpath='./td', dx=6, dy=6):
	mapp = {}
	data = []
	keys = []

	print('dirDirNames ' + dirpath)
	obj_path = gb.glob(dirpath + "/*")
	valueIndex = 0
	for filepath in obj_path:
		resd = {}
		pdir, nameOnly, ext = file.getFilePath(filepath)
		resd['filepath'] = filepath
		resd['filename'] = nameOnly + ext
		# {'name'@'xxxx','width'@200,'height'@300,'point'@[{'x'@102,'y'@18,'w'@22,'h'@36,'left'@0.1,'top'@0.1,'width'@0.2,'height'@0.2},{'x'@159,'y'@75,'w'@28,'h'@42}]}.jpg
		jsonstr = nameOnly
		if (jsonstr.startswith('{') and jsonstr.endswith('}')):
			pass
		else:
			jsonstr = '{"name":"' + jsonstr + '"}'
		obj = json.loads(jsonstr.replace('@', ':').replace('\'', '"'))
		imgBig = cvhelp.open(filepath, 3)
		name = getValue(obj, nameOnly, 'name')
		wbig = getValue(obj, 0, 'width')
		hbig = getValue(obj, 0, 'height')
		if wbig <= 0 or hbig <= 0:
			(wbig, hbig) = cvhelp.getWidthHeight(imgBig)
		rects = []
		imgs = []
		for pointItem in getValue(obj, [{}], 'point'):
			x = getValue(pointItem, getValue(pointItem, 0, 'left') * wbig, 'x') + dx
			y = getValue(pointItem, getValue(pointItem, 0, 'top') * hbig, 'y') + dy
			w = getValue(pointItem, getValue(pointItem, 1, 'width') * wbig, 'w') -2*dx
			h = getValue(pointItem, getValue(pointItem, 1, 'height') * hbig, 'h') -2*dy
			tool.out( name, x, y, w, h, filepath)

			img = imgBig[y:y + h, x:x + w]
			imgs.append(img)
			rects.append([x, y, x+w, y+h])
		resd['rects'] = rects
		resd['imgs'] = imgs
		resd['name'] = name
		data.append(resd)
		mapp[resd['name']] = resd
	keys = sorted(mapp.keys())
	tool.out(tool.showList('keys', arr=keys, size=4))
	for k in keys:
		tool.out(mapp[k]['name'], mapp[k]['rects'], 'imgs size', len(mapp[k]['imgs']))
	return data, mapp, keys


#格式化输出
def formatFileWithShape(imgFile, w, h, point, widthHeight=(100,100) ):
	pdir, nameOnly, ext = file.getFilePath(imgFile)
	return '' + nameOnly + ext + '.from.' + str(w) + 'x' + str(h) + '[' + str(point).replace(':', '@') + '].to.' +  str(widthHeight[0]) + 'x' + str(widthHeight[1]) + '.png'



if __name__ == '__main__':
	# print(loadDirImage())
	print(loadDirImage("td"))
	# print(loadDefaultDataDigits())
	
