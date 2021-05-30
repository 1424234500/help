import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures

import file
import tool

"""
线性数据 
	入参: [ [x,y],... ] 坐标集
	阶数: 高阶函数模拟 
	出参: 预测未来趋势 非已知分类
阶数过高函数 过拟合
阶数过低函数 欠拟合
偏差-方差困境
"""
class Line:
	def __init__(self
				 , name='test'
				 , dirTemp = './__pycache__'
				 , loadable = True  # 是否加载历史
				 , x_train = []
				 , y_train = []
				 , x_test = []
				 , y_test = []
				 , modelTupleDef = [
						('pipeline', Pipeline([
											  ("polynomial_features", PolynomialFeatures(degree=3, include_bias=False))
											, ("linear_regression", LinearRegression() )
											])
						 )
						,
					]
		 ):
		self.name = name
		self.dirTemp = dirTemp
		self.loadable = loadable
		self.x_train = x_train
		self.y_train = y_train
		self.x_test = x_test
		self.y_test = y_test
		self.modelTupleDef = modelTupleDef
	def funx2(self, x):
		return x*x+2*x+4
	# 函数 3πx/2
	def funPi(self, x):
		return np.cos(1.5 * np.pi * x)
	def loadDefaultDataTest(self, shuffle=False):
		name = 'test'
		info = '测试造数'
		np.random.seed(10)
		size=20
		# x_train = np.array(range(size))
		# 随机x序列 对应值上下波动 40%
		x_train = np.sort(np.random.rand(size)) * size
		y_train = self.funx2(x_train) * (np.random.randn(size)*0.4 + 0.8)
		# y_train = [self.funx2(xx) + np.random.randn(32) * 0.3 for xx in x_train]
		test_size=0
		# 有序映射
		x_test = np.linspace(0, size, 100)
		y_test = line.funx2(x_test)
		self.loadDataMake(name=name, info=info, x_train=x_train, y_train=y_train, x_test=x_test, y_test=y_test, test_size=test_size, shuffle=shuffle)
	def loadDataMake(self, name='testData', info='测试造数', x_train=[], y_train=[], x_test=[], y_test=[], test_size=0.001, shuffle=True):
		tool.out(name, info)
		tool.out(name, 'labels', y_train, '# [0, 1, 2, ..., 8, 9, 8]')
		tool.out(name, 'samples 随机点', x_train[:1], '# [0, 1, 2, ..., 8, 9, 8]')
		tool.out('# 加载数据 原样本', len(x_train), len(y_train))
		if (test_size > 0):
			x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
																test_size=max(1, round(len(x_train) * test_size)),
																shuffle=shuffle)
		
		self.name = name
		self.x_train = x_train
		self.y_train = y_train
		self.x_test = x_test
		self.y_test = y_test
		map = {}
		for item in y_train:
			map[item] = item
		self.classes = map.keys()
		tool.out('# 分离扰乱!!数据 训练集 测试集（曲线点）', len(x_train), len(y_train), len(x_test), len(y_test), 'classes', len(self.classes), self.classes)
	def loadModelAndFit(self):
		self.modelTuple = []
		i = 0
		for modelName, modelImpl in self.modelTupleDef:
			i += 1
			modelFile = self.dirTemp + '/' + self.name + '.' + modelName + '.line.joblib'
			tool.out(i, '# 初始化分类器（classifier）', modelName)
			file.mkdir(modelFile)
			if (os.path.isfile(modelFile) and self.loadable):
				tool.out(i, '# 加载模型', modelName, modelFile)
				clf = joblib.load(modelFile)
			else:
				clf = modelImpl
				# 连续分解用于我们训练和测试用的 折叠数据。 KFold 交叉验证.
				tool.out(i, '# 训练模型', modelName, clf.fit(self.x_train[ : , np.newaxis], self.y_train))
				tool.out(i, '# 保存模型', modelName, joblib.dump(clf, modelFile))
			
			# Evaluate the models using crossvalidation
			scores = cross_val_score(clf, self.x_test[:, np.newaxis], self.y_test, scoring="neg_mean_squared_error", cv=10)
			tool.out(i, '# 当前模型', modelName, clf, 'classes', len(self.classes), self.classes, '评分 scores', scores)
			self.modelTuple.append((modelName, clf))
		tool.out(i, '# 模型加载训练完毕', len(self.modelTuple))

	def predict(self, x_predict=None, y_predict=None):
		if x_predict == None and y_predict == None:
			x_predict = self.x_test
			y_predict = self.y_test
		i = 0
		fig = plt.figure(figsize=(16, 6))  # 设置图大小
		for modelName, clf in self.modelTuple:
			i += 1
			tool.out(i, '多图绘制')
			canvas = fig.add_subplot(1, len(self.modelTuple), i)  # 画1行2列个图形的第1个
			
			canvas.plot(self.x_test, self.y_test, label='function', linewidth=3, linestyle='-.')
			canvas.scatter(self.x_train, self.y_train, label="train", s=20, edgecolor='r')
			scores = cross_val_score(clf, self.x_test[:, np.newaxis], self.y_test, scoring="neg_mean_squared_error", cv=10)
			y_res = clf.predict(x_predict[:, np.newaxis])
			
			tool.out(i, '# 预测', modelName)
			# tool.out(x_predict)
			# tool.out(y_predict)
			# tool.out(y_res)
			canvas.plot(x_predict, y_res, label='predict', linewidth=1, linestyle='-')
			plt.title("{} \nmean={:.2e}\nstd={:.2e})".format(modelName, -scores.mean(), scores.std()))
			plt.xlabel("x")
			plt.ylabel("y")
			# 固定展示xy区间
			# plt.xlim((0, 1))
			# plt.ylim((-2, 2))
			plt.legend(loc="best")
			
		plt.show()


if __name__ == '__main__':
	modelTupleDef = [ ]
	for i in range(0, 4):
		i = 2 ** i
		modelTupleDef.append(('pipeline' + str(i), Pipeline([
			  ("polynomial_features", PolynomialFeatures(degree=i, include_bias=False))
			, ("linear_regression", LinearRegression())
		])))
	line = Line(modelTupleDef = modelTupleDef)
	line.loadDefaultDataTest()
	line.loadModelAndFit()
	line.predict()
	# tsk.predict(x_predict=)
