
# -*- coding: utf-8 -*-

import os
import cv2
import matplotlib.pyplot as plt
import sklearn
import tool
from FileUtil import *
from cvhelp import *
from keras.callbacks import *
from keras.layers import *
from keras.models import Sequential
from keras.models import load_model
from keras.optimizers import *
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

"""cnn识别模板 快速替换model train path资源 对比多种模型效率 识别率"""
class Cnn:
    """A simple example class"""
    name = 'number'
    widthHeight = (80, 80)
    img_channels_rgb = 3
    epochs = 5
    batch_size = 4096
    tempDir = './__pycache__'
    path = './number'
    pathTest = './number-test'
    toFileH5 = './__pycache__/cnn.number.' + str(epochs) + '.h5'
    mapIndexFilePath = './__pycache__/cnn.number.' + str(epochs) + '.json'

    modelMake = None    #模型模板
    model = None        #历史加载模型
    test_percent = 0.05
    test_size = 10

    x_train = None
    y_trainNoOneHot = None
    mapRes = None

    def __init__(self
                 , name='number'
                 , widthHeight=(80, 80)
                 , img_channels_rgb=3
                 , epochs=10
                 , batch_size=1024
                 , tempDir='./__pycache__'
                 , path='./number'
                 , pathTest='./number-test'
                 , toFileH5=None
                 , mapIndexFilePath=None

                 , test_percent=0.05
                 , test_size = 10
                 ):
        self.widthHeight = widthHeight
        self.img_channels_rgb = img_channels_rgb
        self.epochs = epochs
        self.batch_size = batch_size
        self.tempDir = tempDir
        self.path = path
        self.pathTest = pathTest
        if(toFileH5 == None):
            self.toFileH5 = tempDir + '/' + 'cnn.' + name + '.epochs.' + str(epochs) + '.h5'
        else:
            self.toFileH5 = toFileH5
        if (mapIndexFilePath == None):
            self.mapIndexFilePath = tempDir + '/' + 'cnn.' + name + '.epochs.' + str(epochs) + '.json'
        else:
            self.mapIndexFilePath = mapIndexFilePath
        self.test_percent = test_percent

        self.test_size = test_size

    def setModel(self, model):
        self.model = model
    def setModelNormal(self):
        ##构建网络
        model = Sequential()
        model.add(ZeroPadding2D((2, 2), input_shape=(self.widthHeight[0], self.widthHeight[1], self.img_channels_rgb)))
        model.add(Lambda(lambda x: x / 255.0))  # 归一化
        # data_format 区别问题 非重点 !!!!!
        model.add(Convolution2D(64, (11, 11), strides=(4, 4), activation='relu', data_format='channels_last'))
        model.add(MaxPooling2D((3, 3), strides=(2, 2)))

        model.add(ZeroPadding2D((2, 2)))
        model.add(Convolution2D(192, (5, 5), activation='relu', data_format='channels_first'))
        model.add(MaxPooling2D((3, 3), strides=(2, 2)))

        model.add(ZeroPadding2D((1, 1)))
        model.add(Convolution2D(384, (3, 3), activation='relu', data_format='channels_first'))
        model.add(ZeroPadding2D((1, 1)))
        model.add(Convolution2D(256, (3, 3), activation='relu', data_format='channels_first'))
        model.add(ZeroPadding2D((1, 1)))
        model.add(Convolution2D(256, (3, 3), activation='relu', data_format='channels_first'))
        model.add(MaxPooling2D((3, 3), strides=(2, 2)))

        model.add(Flatten())
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(4096, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.loadModelOrData()[2].keys()), activation='softmax'))

        # 训练计划
        lr = 0.01
        sgd = SGD(lr=lr, decay=lr / self.epochs, momentum=0.7, nesterov=True)
        model.compile(loss='mse', optimizer=sgd)

        self.modelMake = model
        return model

    def setModelTraffic(self):
        # initialize the model
        model = Sequential()
        input_shape = (self.widthHeight[0], self.widthHeight[1], self.img_channels_rgb)
        # first set of CONV => RELU => POOL layers
        model.add(Convolution2D(20, (5, 5), padding="same", input_shape=input_shape, data_format='channels_last'))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # second set of CONV => RELU => POOL layers
        model.add(Conv2D(50, (5, 5), padding="same"))
        model.add(Activation("relu"))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # first (and only) set of FC => RELU layers
        model.add(Flatten())
        model.add(Dense(500))
        model.add(Activation("relu"))

        # softmax classifier
        model.add(Dense(len(self.loadModelOrData()[2].keys())))  #由于问题
        model.add(Activation("softmax"))

        # 训练计划
        lr = 1e-3
        opt = Adam(lr=lr, decay=lr / self.epochs)
        model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])

        self.modelMake = model
        return model

    def predictDefault(self):
        x_trainTest, y_trainTestNoOneHot, filesTest, countsTest, yInfo, mapResTest = CvHelp().loadImage(path=self.pathTest,
                                                                                                           img_channels_rgb=self.img_channels_rgb,
                                                                                                           widthHeight=self.widthHeight,
                                                                                                           tempDir=self.tempDir,
                                                                                                           shuff=True,
                                                                                                           size=self.test_size)

        return self.predict(x_trainTest, yInfo, filesTest)

    def predict(self, x_trainTest, yInfo, filesTest):
        ################# 训练后及时测试 复用已编码数据!!
        self.loadModelOrData()

        predict = self.model.predict(x_trainTest)
        print('predict eg 0 :', predict[0])
        # 批量预测
        # 构造预测结果 编号 概率 字符串结果
        predictMake = tool.makePredictRes(predict, self.mapRes)
        print('predictMake eg 0 :', predictMake[0])
        # x_train, y_train, files, counts, dirs, mapRes
        error = []
        for i in range(len(predictMake)):
            pi = predictMake[i]
            predictFirst = pi[0]
            shouldBe = str(yInfo[i])
            # shouldBe = str(self.mapRes.get(str(np.argmax(y_trainTest[i], axis=-1))))
            # shouldBe = dirsTest[countsTest[i]]
            # shouldBe = str(mapRes.get(str(y_trainTest[i] )))

            predictByFile = filesTest[i]
            tempFile = self.tempDir + '/predict.temp.should.' + shouldBe + '.but.' + predictFirst[2] + '.' + CvHelp().format(predictByFile, widthHeight=self.widthHeight)
            if (len(pi) > 1):
                print('predict list', pi)

            if (shouldBe != None and shouldBe != '' and shouldBe != predictFirst[2]):
                error.append(pi)  # (5, 0.2, 'b') 编号 概率 字符串结果
                print('test i.' + str(i) + ' predictRes[no:' + str(predictFirst[0]) + ',res:' + str(
                    predictFirst[2]) + ',percent:' + str(predictFirst[
                                                             1]) + '] <===> should be ' + shouldBe + ' predictByFile:' + predictByFile + ' tempFile:' + tempFile)

            text = []
            for k in range(len(pi)):
                if (k >= 3):
                    break
                text.append('' + str((pi[k][0], round(pi[k][1], 2), pi[k][2])))
            CvHelp().drawTextFile(imageFile=predictByFile, imageFileTo=tempFile, point=(1, 18), string=text,
                                  dep=(0, 18), rgb=(0, 1, 242),
                                  textSize=0.30, lineWidth=1)

        print('==============================')
        print(''
              + ' All types ' + str(len(self.mapRes.keys()))
              + ' ok/predict ' + str(str((len(x_trainTest) - len(error))) + '/' + str(len(x_trainTest)))
              + ' ok percent ' + str(round(1.0 * (len(x_trainTest) - len(error)) / len(x_trainTest), 2))
              )
        return predictMake

    def predictImgBig(self, imgSrc='D:\\help_note\\python\\opencv\\number-source\\1.jpg'):
        pdir, nameOnly, ext = tool.getFilePath(imgSrc)
        print('model parse imgSrc:' + str(imgSrc) + ', name:' + nameOnly + ext)
        widthHeight = self.widthHeight
        resList = []
        img = cv2.imread(imgSrc)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        height, width = img.shape[:2]
        before = self.tempDir + '/parse.temp.' + nameOnly + ext + '.size.' + str(width) + 'x' + str( height) + '.t'
        after = '.png'
        infoi = 0

        infoi += 1
        CvHelp().save(before + str(infoi) + '.gray.' + after, gray)

        # ret, thresh = cv2.threshold(gray, 128, 255, 1) ## 阈值分割
        thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)  ## 自适应二值化

        infoi += 1
        CvHelp().save(before + str(infoi) + '.thresh.' + after, thresh)

        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (2, 2))  # 卷积
        dilated = cv2.dilate(thresh, kernel)  # 腐蚀
        infoi += 1
        CvHelp().save(before + str(infoi) + '.dilated.' + after, dilated)

        # image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  ## 轮廓提取
        # img = CvHelp().drawImage(img, contours, 1500)
        infoi += 1
        CvHelp().save(before + str(infoi) + '.hierarchy.' + after, hierarchy)

        for i in range(len(contours)):
            cnt = contours[i]
            x, y, w, h = cv2.boundingRect(cnt)
            area = cv2.contourArea(cnt)
            # 处理掉小的轮廓区域，这个区域的大小自己定义。
            if (area < (1200)):
                # thickness不为-1时，表示画轮廓线，thickness的值表示线的宽度。
                # cv2.drawContours(img, [cnt], -1, (0, 255, 0), thickness=-1)
                continue
            # 3通道 rgb问题
            number_roi = img[y:y + h, x:x + w]
            ## 统一大小
            resized_roi = CvHelp().resizeKeep(number_roi, widthHeight)
            # thresh1 = cv2.adaptiveThreshold(resized_roi, 255, 1, 1, 11, 2) ## 阈值分割
            ## 归一化像素值
            normalized_roi = resized_roi / 255.
########################################### 分图预测
            x_trainTest = [normalized_roi]
            x_trainTest = np.array(x_trainTest)
            # 4维度 shape问题  数据量 r g b

            self.loadModelOrData()
            predict = self.model.predict(x_trainTest)
            print( before + ' predict eg 0 :', predict[0])
            # 批量预测
            # 构造预测结果 编号 概率 字符串结果
            predictMake = tool.makePredictRes(predict, self.mapRes)
            print( before + ' predictMake eg 0 :', predictMake[0])
            predictMakeOne = predictMake[0]
            ## 识别结果展示
            cv2.rectangle(img, (x - 1, y - 1), (x + w, y + h), (0, 0, 255), 2)
            #    结果集序号 概率 字符串结果
            #   [( 1, 0.8, 'a'), (5, 0.2, 'b')  ]
            for k in range(len(predictMakeOne)):
                if (k >= 3):
                    break
                text = ('' + str((predictMakeOne[k][0], round(predictMakeOne[k][1], 2), predictMakeOne[k][2])))
                CvHelp().drawText(img, point=(x+2 , y + 20 + 18 * k), string=text, rgb=(0, 255, 242), textSize=0.30, lineWidth=1)
#########################

            resList.append(   (predictMakeOne[0], (x, y, w, h))   )

        infoi += 1
        CvHelp().save(before + str(infoi) + '.res.' + after, img)

        resList.sort(key=lambda x: x[0][1])

        print(resList)

        return (img, resList)

    def train(self):
        ################读取数据
        # x_train, y_trainNoOneHot, _, _, _, self.mapRes = CvHelp().loadImage(path=self.path,
        #                                                                            img_channels_rgb=self.img_channels_rgb,
        #                                                                            widthHeight=self.widthHeight, shuff=True)
        x_train, y_trainNoOneHot, mapRes = self.loadModelOrData()
        if(self.model != None):
            return 'has train finish file or load from file h5 '
        
        # 独热编码 距离问题 不存在倍数问题  将每个值编码 最大种类数
        y_train = np_utils.to_categorical(y_trainNoOneHot, len(self.mapRes.keys()))  # One-Hot encoding
        # y = np.argmax(Y, axis=-1)

        x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=self.test_percent)

        ################训练模型 ################# 训练计划
        if(self.modelMake == None):
            self.modelMake = makeModel(resSize=len(self.mapRes.keys()), img_channels_rgb=self.img_channels_rgb, widthHeight=self.widthHeight)
            raise Exception(' no init model ? cnn.setModel? ')

        history, _ = train(self.modelMake, x_train, y_train, x_test, y_test, batch_size=self.batch_size, toFileH5=self.toFileH5,
                                  epochs=self.epochs)

        print('save mapRes ' + str(self.mapRes))
        if (self.mapIndexFilePath != None):
            tool.setFileJsonObj(self.mapIndexFilePath, self.mapRes)
        return history

    def loadModelOrData(self):
        ################加载模型
        if(self.model == None):
            if os.path.exists(self.toFileH5):
                print('load model cnn from file  ' + self.toFileH5)
                self.model = load_model( self.toFileH5)
                self.mapRes = tool.getFileJsonObj(self.mapIndexFilePath)
                print(self.mapRes)
            else:
                print('load model cnn from file not exists, then to load data file !!! ' + self.toFileH5)
        ################读取数据
                self.x_train, self.y_trainNoOneHot, _, _, _, self.mapRes = CvHelp().loadImage(path=self.path,
                                                                                    img_channels_rgb=self.img_channels_rgb,
                                                                                    widthHeight=self.widthHeight,
                                                                                    shuff=True)
                print(self.mapRes)
                self.model = None
        else:
            pass

        return (self.x_train, self.y_trainNoOneHot, self.mapRes)


# 一次性吞吐不了太多的数据，只好用generator的方式，一点一点的从数据池里拿小批量数据喂给网络
def generator(samples_X, samples_Y, batch_size=32):
    num_samples = len(samples_X)
    while 1:  # Loop forever so the generator never terminates
        for offset in range(0, num_samples, batch_size):
            batch_samples_X = samples_X[offset:offset+batch_size]
            batch_samples_Y = samples_Y[offset:offset+batch_size]

            yield sklearn.utils.shuffle(batch_samples_X, batch_samples_Y)

# SGD（随机梯度下降），对于大量的图片数据库，SGD在执行梯度下降时
# ，只需要抽取batch_size的样本放入神经网络计算。
# 所以避免出现程序报错，出现电脑显存不足的情况。
# 用mse（均方差）来计算loss，计划训练300各回合，如果持续30个回合稳定便自动保存网络。（很实用！）
def train(model, x_train, y_train, x_test=None, y_test=None, batch_size=32, toFileH5='./person.cnn.h5', epochs=10):
    if os.path.exists(toFileH5):
        print('make file is exists skip make ' + str((toFileH5)))
        return None, toFileH5

    # compile and train the model using the generator function
    train_generator = generator(x_train, y_train, batch_size=batch_size)
    validation_generator = generator(x_test, y_test, batch_size=batch_size)

    callbacks_list = [
        EarlyStopping(monitor='val_loss', patience=10), #降低过拟合
        # monitor: 需要监视的值通常为：val_acc 或 val_loss 或 acc 或 loss 5折交叉验证，没有单设验证集，所以只能用acc
        # patience：能够容忍多少个epoch内都没有improvement。
        ModelCheckpoint(filepath=toFileH5, monitor='val_loss', verbose=1, save_best_only=True) #保存结果
        # filepath = “weights_  {epoch: 03d} - {val_loss: .4f}.h5” 则会生成对应epoch和验证集loss的多个文件。
        # monitor：需要监视的值，通常为：val_acc
        # verbose：信息展示模式，0  或1。为1表示输出epoch模型保存信息，默认为0表示不输出该信息，信息形如：
        # Epoch  00001: val_acc improved  from   -inf  to  0.49240, saving model to / xxx / checkpoint / model_001 - 0.3902.h5
        # save_best_only：当设置为True时，将只保存在验证集上性能最好的模型
        # mode：‘auto’，‘min’，‘max’之一，在save_best_only = True时决定性能最佳模型的评判准则，例如，当监测值为val_acc时，模式应为max，当检测值为val_loss时，模式应为min。在auto模式下，评价准则由被监测值的名字自动推断。
        # save_weights_only：若设置为True，则只保存模型权重，否则将保存整个模型（包括模型结构，配置信息等）
        # period：CheckPoint之间的间隔的epoch数
    ]


    H = model.fit_generator(train_generator,
                                  steps_per_epoch=len(y_train) / batch_size,
                                  validation_data=validation_generator,
                                  validation_steps=len(y_test) / batch_size,
                                  epochs=epochs, verbose=1,
                                  callbacks=callbacks_list, shuffle=True)
    print('train ok ' + toFileH5)
    print("--- history --- ")
    history = H.history
    print(history)
    # 学习曲线图生成
    plt.style.use("ggplot")
    plt.figure()
    lent = epochs
    keyss = ['loss', 'val_loss', 'acc', 'val_acc', 'accuracy', 'val_accuracy']
    for item in keyss:
        if item in history:
            if(len(history[item]) < lent):
                lent = len(history[item])
    for item in keyss:
        if item in history:
            plt.plot(np.arange(0, lent), history[item][:lent], label=item)
    plt.title("Training Loss and Accuracy on traffic-sign classifier")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend(loc="lower left")
    plt.savefig(toFileH5 + '.png')
    print('save history png ' + toFileH5 + '.png')

    return history, toFileH5

# 答案穷举数量 labels size
def makeModel(resSize=2, img_channels_rgb=3, widthHeight=(80, 100)):
    ##构建网络
    model = Sequential()
    model.add(ZeroPadding2D((2, 2), input_shape=(widthHeight[0], widthHeight[1], img_channels_rgb)))
    model.add(Lambda(lambda x: x / 255.0))  # 归一化
    #data_format 区别问题 非重点 !!!!!
    model.add(Convolution2D(64, (11, 11), strides=(4, 4), activation='relu', data_format='channels_last'  ))
    model.add(MaxPooling2D((3, 3), strides=(2, 2)))

    model.add(ZeroPadding2D((2, 2)))
    model.add(Convolution2D(192, (5, 5), activation='relu', data_format='channels_first'  ))
    model.add(MaxPooling2D((3, 3), strides=(2, 2)))

    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(384, (3, 3), activation='relu', data_format='channels_first'  ))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu', data_format='channels_first'  ))
    model.add(ZeroPadding2D((1, 1)))
    model.add(Convolution2D(256, (3, 3), activation='relu', data_format='channels_first'  ))
    model.add(MaxPooling2D((3, 3), strides=(2, 2)))

    model.add(Flatten())
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(4096, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(resSize, activation='softmax'))

    #
    # model.add(Dense(40, input_dim=65, kernel_initializer='uniform', activation='relu'))
    # model.add(Dense(20, kernel_initializer='uniform', activation='relu'))
    # model.add(Dense(2, activation='sigmoid'))
    # model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    return model


if __name__ == '__main__':
    name = 'number'
    widthHeight = (80, 80)
    img_channels_rgb = 3
    epochs = 5
    batch_size = 4096
    tempDir = './__pycache__'
    path = './number'
    pathTest = './number-test'
    test_percent = 0.05
    test_size = 60

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

    cnn.setModelNormal()
    cnn.train()
    cnn.predictDefault()


