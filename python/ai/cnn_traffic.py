
# -*- coding: utf-8 -*-
import sklearn

import numpy as np
from keras.callbacks import *
from sklearn.model_selection  import train_test_split
from keras.optimizers import *
from keras.models import Sequential
from keras.layers import *
from keras.utils import np_utils
from keras.models import load_model
import matplotlib.pyplot as plt
from cnn import *
import os
import tool
from FileUtil import *
from cvhelp import *

if __name__ == '__main__':

    name = 'traffic'
    widthHeight = (32, 32)
    img_channels_rgb = 3
    epochs = 35
    batch_size = 1024
    tempDir = './__pycache__'
    path = 'D:\\Pictures\\pc\\BelgiumTSC_Training\\Training'
    pathTest = 'D:\\Pictures\\pc\\BelgiumTSC_Training\\Testing'
    test_percent = 0.05
    test_size = 1000

    cnn = Cnn( name=name
                 , widthHeight=widthHeight
                 , img_channels_rgb=img_channels_rgb
                 , epochs=epochs
                 , batch_size=batch_size
                 , tempDir=tempDir
                 , path=path
                 , pathTest=pathTest
                 , toFileH5=None
                 , mapIndexFilePath=None
                 , test_percent=test_percent
                 , test_size=test_size
               )

    cnn.setModelTraffic()
    cnn.train()
    cnn.predictDefault()


