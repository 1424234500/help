import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn import svm
from sklearn.model_selection import train_test_split, validation_curve
from sklearn.neighbors import KNeighborsClassifier

import file
import tool

"""
监督学习 任意分类 
	入参: x_train, y_train
	模型: model
	出参: 预测x_test已知分类
"""
class Tsk:
	def __init__(self
				 , name='test'
				 , dirTemp = './__pycache__'
				 , loadable = False  # 是否加载历史
				 , x_train = []
				 , y_train = []
				 , x_test = []
				 , y_test = []
				 , modelTupleDef = [
						('svc', svm.SVC(C=100.0, kernel='rbf', degree=3, gamma='auto',  # gamma='scale'
										coef0=0.0, shrinking=True, probability=True,
										tol=1e-3, cache_size=200, class_weight=None,
										verbose=False  # 日志详细s
										, max_iter=-1, decision_function_shape='ovr',
										break_ties=False,
										random_state=None)
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
	def loadDefaultDataIris(self, test_size=0.001, shuffle=True):
		name = 'iris'
		iris = datasets.load_iris()
		x_train = iris.data
		y_train = iris.target
		# print( iris.DESCR )
		info = '鸢尾花卉 150个样本，每个样本包含4个特征：花萼长度，花萼宽度，花瓣长度，花瓣宽度'
		self.loadDataMake(name=name, info=info, x_train=x_train, y_train=y_train, test_size=test_size, shuffle=shuffle)
	def loadDefaultDataDigits(self, test_size=0.001, shuffle=True):
		name = 'digits'
		info = '手写数字 1797个 每个图像为8*8像素'
		digits = datasets.load_digits()
		x_train = digits.data
		y_train = digits.target
		tool.out(name, '', digits.images[0])
		self.loadDataMake(name=name, info=info, x_train=x_train, y_train=y_train, test_size=test_size, shuffle=shuffle)
	def loadDefaultDataTest(self, test_size=0.2, shuffle=True):
		name = 'test'
		info = '测试造数'
		# 随机x序列 对应值上下波动 40%
		size=10
		x_train = []
		y_train = []
		for i in range(size):
			for j in range(100):
				x_train.append((i, i))
				y_train.append(i)
		x_train = np.array(x_train)
		y_train = np.array(y_train)
		self.loadDataMake(name=name, info=info, x_train=x_train, y_train=y_train, test_size=test_size, shuffle=shuffle)
	# 训练数据
	def loadDataMake(self, name='testData', info='测试造数', x_train=[], y_train=[], test_size=0.001, shuffle=True):
		tool.out(name, info)
		tool.out(name, 'labels', y_train, '# [0, 1, 2, ..., 8, 9, 8]')
		tool.out(name, 'samples', x_train[:1], '# [  [0,1] , [2, 3] , ... , [19, 20]  ]')
		tool.out('# 加载数据 原样本', len(x_train), len(y_train))
		if(test_size > 0):
			x_train, x_test, y_train, y_test = train_test_split(x_train, y_train,
															test_size=max(1, round(len(x_train) * test_size)),
															shuffle=shuffle)
		self.name = name
		self.x_train = x_train
		self.y_train = y_train
		self.x_test = x_test
		self.y_test = y_test

		map={}
		for item in y_train:
			map[item] = item
		self.classes = list(map.keys())
		tool.out('# 分离扰乱!!数据 训练集 测试集', len(x_train), len(y_train), len(x_test), len(y_test), 'classes', len(self.classes), self.classes)

	def loadModelAndFit(self):
		self.modelTuple = []
		i = 0
		for modelName, modelImpl in self.modelTupleDef:
			i += 1
			modelFile = self.dirTemp + '/' + self.name + '.' + modelName + '.svc.joblib'
			tool.out(i, '# 初始化分类器（classifier）', modelName)
			file.mkdir(modelFile)
			if (os.path.isfile(modelFile) and self.loadable):
				tool.out(i, '# 加载模型', modelName, modelFile)
				clf = joblib.load(modelFile)
				# 再设置属性后重新训练
				# clf.set_params(kernel='linear')
				# clf.fit(x_train, y_train)
			else:
				clf = modelImpl
				# 连续分解用于我们训练和测试用的 折叠数据。 KFold 交叉验证.
				tool.out(i, '# 训练模型', modelName, clf.fit(self.x_train, self.y_train))
				tool.out(i, '# 保存模型', modelName, joblib.dump(clf, modelFile))
			scores = clf.score(self.x_test, self.y_test)
			tool.out(i, '# 当前模型', modelName, clf, 'classes', len(self.classes), self.classes, '评分 scores', scores)
			self.modelTuple.append((modelName, clf))
			# self.scores(modelName, clf)
		tool.out(i, '# 模型加载训练完毕', len(self.modelTuple))
	def scores(self, modelName, clf):
		param_range = np.logspace(-6, -1, 5)
		train_scores, test_scores = validation_curve(
			clf, self.x_train, self.y_train, param_name="gamma", param_range=param_range,
			scoring="accuracy", n_jobs=1)
		train_scores_mean = np.mean(train_scores, axis=1)
		train_scores_std = np.std(train_scores, axis=1)
		test_scores_mean = np.mean(test_scores, axis=1)
		test_scores_std = np.std(test_scores, axis=1)
		
		plt.title("Validation Curve with SVM " + modelName + ' ' + self.name)
		plt.xlabel(r"$\gamma$")
		plt.ylabel("Score")
		plt.ylim(0.0, 1.1)
		lw = 2
		plt.semilogx(param_range, train_scores_mean, label="Training score",
					 color="darkorange", lw=lw)
		plt.fill_between(param_range, train_scores_mean - train_scores_std,
						 train_scores_mean + train_scores_std, alpha=0.2,
						 color="darkorange", lw=lw)
		plt.semilogx(param_range, test_scores_mean, label="Cross-validation score",
					 color="navy", lw=lw)
		plt.fill_between(param_range, test_scores_mean - test_scores_std,
						 test_scores_mean + test_scores_std, alpha=0.2,
						 color="navy", lw=lw)
		plt.legend(loc="best")
		plt.show()
	def predict(self, x_predict=None, y_predict=None, top=2, p=3):
		if x_predict == None and y_predict == None:
			x_predict = self.x_test
			y_predict = self.y_test
		i = 0
		for modelName, clf in self.modelTuple:
			i += 1
			# tool.out(i, '# 预测', modelName, self.y_test, 'predict', clf.predict(self.x_test))
			predict_proba = tool.predict_proba_to_class(self.classes, clf.predict_proba(x_predict), top=top, p=p)
			ok = len(x_predict)
			for pi in range(len(predict_proba)):
				pitem = (None, None)
				if len(predict_proba[pi]) > 0:
					pitem=predict_proba[pi][0]
				if len(y_predict) > pi and pitem[0] != y_predict[pi]:
					ok -= 1
					tool.out('predit error', pi, x_predict[pi], '->', pitem[0], '!=', y_predict[pi])

			tool.out(i, '# 预测', modelName, 'percent', round(ok/len(x_predict),3), 'classes', y_predict, 'predict_proba', predict_proba)


if __name__ == '__main__':

	tsk = Tsk(modelTupleDef = [
		('svc-rbf', svm.SVC(C=100.0, kernel='rbf', degree=3, gamma='auto',  # gamma='scale'
							coef0=0.0, shrinking=True, probability=True,
							tol=1e-3, cache_size=200, class_weight=None,
							verbose=False  # 日志详细s
							, max_iter=-1, decision_function_shape='ovr',
							break_ties=False,
							random_state=None)
		)
		# ,('svc-poly', svm.SVC(C=100.0, kernel='poly', degree=3, gamma='auto',  # gamma='scale'
		#					 coef0=0.0, shrinking=True, probability=True,
		#					 tol=1e-3, cache_size=200, class_weight=None,
		#					 verbose=False  # 日志详细s
		#					 , max_iter=-1, decision_function_shape='ovr',
		#					 break_ties=False,
		#					 random_state=None)
		# )
		, ('knn', KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski', metric_params=None, n_jobs=1, n_neighbors=5, p=2, weights='uniform') )
		# , ('logistic', LogisticRegression(C=100.0, class_weight=None, dual=False, fit_intercept=True, intercept_scaling=1, max_iter=100, multi_class='ovr', n_jobs=1, penalty='l2', random_state=None, solver='liblinear', tol=0.0001, verbose=0, warm_start=False))

	])
	tsk.loadDefaultDataIris()
	tsk.loadModelAndFit()
	tsk.predict()
	# tsk.predict(x_predict=)
