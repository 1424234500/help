#!/usr/bin/python
#-*- coding:utf-8 -*-  
import sys
import cv2
import numpy as np
sys.path.append("../")
import tool
import file

####
# 作为常用cv2工具 详细见cv2文档

cvhelp_classfier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

def getWidthHeight(image):
	if (len(image.shape) == 3):
		h, w, _ = image.shape
	else:
		h, w = image.shape
	return (w,h)
# 统一尺寸时需要保证，图像不会被扭曲变形，在多余的空白处用纯黑色填充。
def resizeKeep(image, widthHeight=(100, 200), BLACK = [0, 0, 0]):
	top, bottom, left, right = (0, 0, 0, 0)
	if(len(image.shape) == 3):
		h, w, _ = image.shape
	else:
		h, w = image.shape
	# 对于长宽不相等的图片，找到最长的一边
	# w1 / h1 = w2 / h2
	# 宽重比
	#	   20			  /	   10		> 4		  / 3
	if 1.0 * widthHeight[0] / widthHeight[1] > 1.0 * w  / h  :
		neww = 1.0 * h *  (widthHeight[0] / widthHeight[1])
		newh = h
		bottom = 0
		# top = h
		top = 0
		left = (neww - w) / 2
		# right = left + w
		right = left
	else:
	# 长重比
	# 10			  /	   20		> 4		  / 3
		newh = 1.0 * w / (widthHeight[0] / widthHeight[1])
		neww = w
		bottom = (newh - h) / 2
		# top = h + bottom
		top = bottom
		left = 0
		# right = w
		right = 0
	# 给图像增加像素 分别各个方向的数值，cv2.BORDER_CONSTANT指定边界颜色由value指定
	constant = cv2.copyMakeBorder(image, int(top), int(bottom), int(left), int(right), cv2.BORDER_CONSTANT, value=BLACK)

	# 调整图像大小并返回
	return cv2.resize(constant, widthHeight)

#LUT 直方图均衡化处理
#GaussianBlur边缘检测
#laplacian算子
#sabel算子
#初级滤波
def getBlur(img, count=1):
	img = getGray(img.copy())
	#用低通滤波来平滑图像 将每个像素替换为该像素周围像素的均值
	#imgBlur = cv2.blur(img, (5,5))
	#高斯模糊
	for j in range(count):
		imgaussian = cv2.GaussianBlur(img,(5,5),1.5)
	#低通滤波中，滤波器中每个像素的权重是相同的，即滤波器是线性的。而高斯滤波器中像素的权重与其距中心像素的距离成比例
	return imgaussian
#形态学处理
#检测拐角
#边缘检测
def getFindLine(img):
	img = getGray(img.copy())
	#构造一个3×3的结构元素
	element = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
	dilate = cv2.dilate(img, element)
	erode = cv2.erode(img, element)

	#将两幅图像相减获得边，第一个参数是膨胀后的图像，第二个参数是腐蚀后的图像
	result = cv2.absdiff(dilate,erode);

	#上面得到的结果是灰度图，将其二值化以便更清楚的观察结果
	retval, result = cv2.threshold(result, 40, 255, cv2.THRESH_BINARY);
	#反色，即对二值图每个像素取反
	result = cv2.bitwise_not(result);

	return result
#开闭运算
def getOpen(img):
	img = getGray(img.copy())
	#定义结构元素
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
	#开运算
	opened = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
	return opened
#开闭运算
def getClose(img):
	img = getGray(img.copy())
	#定义结构元素
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(5, 5))
	closed = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	return closed
#腐蚀-膨胀
def getErode(img):
	img = getBinary(img.copy())
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
	eroded = cv2.erode(img,kernel)
	return eroded
#腐蚀-膨胀
def getDilate(img):
	img = getBinary(img.copy())
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(3, 3))
	dilated = cv2.dilate(img,kernel)
	return dilated
#RGB GRAY BINARY -> 二值图
def getBinary(img, type=0, border=3):
	rgbSize = getImageType(img)
	if(rgbSize == 1):
		img = img
	elif(rgbSize == 2):
		if(type == 0): #自适应阈值 决定是否反转颜色 边框宽度
			imgBlack = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, border,2)
		else:
			#普通127阈值
			ret,imgBlack = cv2.threshold(img,127,255,cv2.THRESH_BINARY) #转二值图
		img = imgBlack
	# 彩色图点[(0, 0, (0~255, 0~255, 0~255) )]
	elif(rgbSize == 3):
		img = getGray(img)
		img = getBinary(img)
	return img
#转二值图
def getGray(img):
	imgType = getImageType(img)
	if(imgType == 3):
		res = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		res = img
	return res
#绘制 三通道 折线图
def getHistRGB(image):
	h = np.zeros((256,256,3)) #创建用于绘制直方图的全0图像
	bins = np.arange(256).reshape(256,1) #直方图中各bin的顶点位置
	color = [ (255,0,0),(0,255,0),(0,0,255) ] #BGR三种颜色
	for ch, col in enumerate(color):
		originHist = cv2.calcHist([image],[ch],None,[256],[0,256])
		cv2.normalize(originHist, originHist,0,255*0.9,cv2.NORM_MINMAX)
		hist=np.int32(np.around(originHist))
		pts = np.column_stack((bins,hist))
		cv2.polylines(h,[pts],False,col)
	h=np.flipud(h)
	return h
#绘制 单通道 直方图
def getHist(img, color):
	hist= cv2.calcHist([img], [0], None, [256], [0.0,255.0])
	minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
	histImg = np.zeros([256,256,3], np.uint8)
	hpt = int(0.9* 256);
	for h in range(256):
		intensity = int(hist[h]*hpt/maxVal)
		cv2.line(histImg,(h,256), (h,256-intensity), color)
	return histImg;
#画圆
def drawCircle(image, point=(100,100), radius=60, rgb=(255,128,255), line_width=4, line_type=8):
	cv2.circle(image, point, radius, rgb, line_width, line_type)
	return image
#画线
def drawLine(image, start_point=(0,0), end_point=(0,0), rgb=(255,128,255), line_width=4, line_type=8):
	cv2.line(image, start_point, end_point, rgb, line_width, line_type)
	return image
#画矩形
def drawRect(image, start_point=(0,0), end_point=(10,20), rgb=(120,120,120), fill=False, alpha=1, line_width=2, line_type=8):
	if(fill):
		if(alpha < 1):
			bbox1 = [start_point[0], start_point[1], end_point[0], end_point[1]]
			zeros1 = np.zeros((image.shape), dtype=np.uint8)
			zeros_mask1 = cv2.rectangle(zeros1, (bbox1[0], bbox1[1]), (bbox1[2], bbox1[3]), color=rgb, thickness=-1)  # thickness=-1 表示矩形框内颜色填充
			zeros_mask = np.array((zeros_mask1))
			# alpha 为第一张图片的透明度
			# beta 为第二张图片的透明度
			gamma = 0
			# cv2.addWeighted 将原始图片与 mask 融合
			image = cv2.addWeighted(image, 1, zeros_mask, alpha, gamma)
		else:
			points = np.array([ start_point, [start_point[0], end_point[1]], end_point, [end_point[0],start_point[1]] ], np.int32)
			#[1，3]，[4，8],[1,9]为要填充的轮廓坐标
			cv2.fillConvexPoly(image, points, rgb)
	cv2.rectangle(image, start_point, end_point, rgb, line_width, line_type)
	return image
#画text
def drawText(image, point=(100,100), string="drawText", rgb=(22,42,0), textSize=0.45, lineWidth=1):
	cv2.putText(image,str(string),  point,	  0,	  textSize,	   rgb,	 lineWidth)
	# 照片/添加的文字/			  左上角坐标/ 字体/   字体大小/ 颜色/	 字体粗细
	return image
#画text #5C2C00
#多行 文本
def drawTextFile(img, imageFileTo=None, point=(100,100), string=["drawText"], dep=(0, 20), rgb=(22,42,0), textSize=0.5, lineWidth=1):
	img = img.copy()
	i = 0
	for item in string:
		cv2.putText(img,str(item),  (point[0] + dep[0] * i, point[1] + dep[1] * i),	  0,	  textSize,	   rgb,	 lineWidth)
		# 照片/添加的文字/			  左上角坐标/ 字体/   字体大小/ 颜色/	 字体粗细
		i += 1
	if(imageFileTo != None):
		save(imageFileTo, img)
	return img
#创建图片 大小
def createImage(width=256, height=256, rgb=(0,255,0)):
	image = np.zeros((height, width, 3), dtype=np.uint8)
	image = drawRect(image, (0,0), (width,height), rgb, fill=True)
	return image
#保存图片
def save(filepath, img):
	file.mkdir(filepath)
	cv2.imwrite(filepath, img)
	# tool.out("save img", filepath)
	return
#0~255, 0~255, 0~255
#打开图片
def open(name, rgb=3):
	if(rgb == 3):
		return cv2.imread(name)
	elif(rgb == 2):
		return openGray(name)
	else:
		return openBinary(name)
#0~255
def openGray(name):
	return cv2.imread(name, cv2.IMREAD_GRAYSCALE)
#0/255
def openBinary(name):
	img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	return getBinary(img)
#0/1
def openZero(name):
	img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
	binary = getBinary(img)
	return binary/255.

#RGB GRAY BINARY - 3 2 1
def getImageType(img):
	res = img.ndim
	if(res == 2):
		res = 1
		#根据像素是否只存在255/0来判定图片类型GRAY 2 BINARY 1
		rowLen = img.shape[0]
		colLen = img.shape[1]
		for i in range(0, rowLen, 1):
			for j in range(0, colLen, 1):
				if(img[i, j] != 255 and img[i, j] != 0):
					res = 2
	return res
#填充扩大
def getFill(img, width=12, height=12):
	img = getBinary(img.copy())
	kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
	fill = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
	return fill

#人脸检测
def findFace(img):
	# img = getGray(img.copy())
	faces = cvhelp_classfier.detectMultiScale(img,scaleFactor=1.1,minNeighbors=5,minSize=(5,5))
	for (x, y, w, h) in faces:
		cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

	return faces, img
# 轮廓检测绘制
def findContours(img, minArea=1000, colorMin=(0, 255, 0), colorMax=(0, 255, 255)):
	img = getGray(img)
	contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	c_max = []
	c_min = []
	for i in range(len(contours)):
		cnt = contours[i]
		area = cv2.contourArea(cnt)
		if (area < minArea):  # 小区域处理
			c_min.append(cnt)
			continue
		c_max.append(cnt)
	cv2.drawContours(img, c_min, -1, colorMin, thickness=-1)  # 填充
	cv2.drawContours(img, c_max, -1, colorMax, thickness=2)  # 画框
	return contours, img


def rotateClockWise90(img):
    trans_img = cv2.transpose( img )
    img90 = cv2.flip(trans_img, 1)
    return img

def totateClockWise90ByNumpy(img):  # np.rot90(img, 1) 顺时针旋转90度
    img90 = np.rot90(img, -1)
    return img90

def findImg(imgBig, imgSmall, text='info', tempFile=None, tempDir="__pycache__"):
	methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
	res = []
	for md in methods:

		for i in range(1):  # len(x_train)):
			th, tw, _ = imgSmall.shape
			result = cv2.matchTemplate(imgBig, imgSmall, md)
			min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
			if md == cv2.TM_SQDIFF_NORMED:
				tl = min_loc
			else:
				tl = max_loc
			br = (tl[0] + tw, tl[1] + th)
			res.append([tl[0], tl[1], tl[0] + tw, tl[1] + th])
			drawRect(imgBig, start_point=(tl[0], tl[1]), end_point=br, rgb=(255, 128, 255), fill=False, alpha=0.8,
							line_width=4, line_type=8)
			drawText(imgBig, point=(tl[0], tl[1] + 20), string=text, rgb=(0, 64, 64), textSize=0.45,
							lineWidth=1)
		# cv2.rectangle(target, tl, br, [0, 0, 0])
		if tempFile == None:
			tempFile = tempDir + '/' + 'md' + str(md) + '_' + text + '_res.png'
		save(tempFile, imgBig)
	return res

if __name__ == '__main__':
	filepath='sperson.jpg'
	img = open(filepath)
	save('./__pycache__/fill' + filepath, drawText(drawRect(open(filepath), start_point=(80, 80), end_point=(200, 200), fill=True, alpha=0.8), ))
	save('./__pycache__/s' + filepath, open(filepath))
	# save('./__pycache__/sc' + filepath, findContours(img)[1])
	# save('./__pycache__/' + filepath, findFace(img)[1])







