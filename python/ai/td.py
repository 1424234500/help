#!/usr/bin/python
#-*- coding:utf-8 -*-  
import json
import sys
sys.path.append("../")

import numpy as np
from keras.utils import np_utils
from sklearn.model_selection import train_test_split
import glob as gb
from sklearn import datasets
import ai
import file,tool,cvhelp
import cv2

def action(path = 'td', img_channels_rgb = 3, widthHeight = None, test_all=True, tempDir='./__pycache__'):
	print('start----------')
	x_train, x_test, y_train, y_test, y_train_NoOneHot, y_test_NoOneHot, y_train_filepath, y_test_filepath, mapRes = ai.loadDirImage(
		path=path, img_channels_rgb=img_channels_rgb, widthHeight=widthHeight, test_all=test_all, shuffle=False)

	pass
	for ti in range(len(y_test_filepath)):
		testFile = y_test_filepath[ti]
		testText = y_test_NoOneHot[ti]
		methods = [cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED]
		for md in methods:
			target = cvhelp.open(testFile)

			for i in range(1):#len(x_train)):
				smallImg = x_train[i]
				smallText = y_train_NoOneHot[i]
				th, tw, _ = smallImg.shape
				result = cv2.matchTemplate(target, smallImg, md)
				min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
				if md == cv2.TM_SQDIFF_NORMED:
					tl = min_loc
				else:
					tl = max_loc
				br = (tl[0] + tw, tl[1] + th)
				cvhelp.drawRect(target, start_point=(tl[0], tl[1]), end_point=br, rgb=(255,128,255), fill=True, line_width=2, line_type=8)
				cvhelp.drawText(target, point=(tl[0], tl[1] + 20), string=smallText, rgb=(0,64,64), textSize=0.45, lineWidth=1 )
				# cv2.rectangle(target, tl, br, [0, 0, 0])
			cvhelp.save(tempDir + '/' + 'md' + str(md) + '_' + testText + '_res.png', target)

	print('end--------------')





if __name__ == '__main__':
	action()










