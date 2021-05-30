# 公开课程
https://www.coursera.org/learn/machine-learning

scikit-learn 机器学习工具
  https://scikit-learn.org/stable/
  https://github.com/apachecn/sklearn-doc-zh

  pip install sklearn-doc-zh
  sklearn-doc-zh 9990   # 访问 http://localhost:9990  

Keras 深度学习库 高级神经网络 API 
  以 TensorFlow、CNTK、Theano作为后端
  https://keras.io/zh/

TensorFlow 谷歌第二代机器学习系统
 

KNN
SVM
R-CNN
Faster R-CNN 
论文
https://arxiv.org/pdf/1504.08083.pdf
https://github.com/rbgirshick/fast-rcnn
 
# voc2007资源介绍
https://arleyzhang.github.io/articles/1dc20586/
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtrainval_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCtest_06-Nov-2007.tar
wget http://host.robots.ox.ac.uk/pascal/VOC/voc2007/VOCdevkit_08-Jun-2007.tar


## faster rcnn案例 
40000次训练模型能有效识别样例 但自己训练4000次 不能用 移植失败
https://github.com/dBeker/Faster-RCNN-TensorFlow-Python3
https://blog.csdn.net/tuoyakan9097/article/details/81776019
https://blog.csdn.net/tuoyakan9097/article/details/81782257
https://blog.csdn.net/tuoyakan9097/article/details/82528245

从数据的属性中学习，并将它们应用到新数据的过程

# 监督学习
已知样本 [(x1,y1)...] 求解 x=a时 y=?
## 回归 已知样本具有连续性
房价随着时间的走势预测
### 线性回归 曲线拟合 y=ax+b ->求解最优a b 计算新x的y 
###逻辑回归 n-1维分割n类数据 属于svm分类算法 ?

## 分类 已知样本是离散点
手写数字图像一维化向量识别
### knn 样本中距离最近的k个样本概率分布   
###朴素贝叶斯 选择后验概率最大的类为分类标签
  文本分类、垃圾文本过滤，情感判别
### 决策树 构造一棵熵值下降最快的分类树
  用户贷款风险评估 有房->有车->有工资
### 支持向量机SVM 构造 n-1维最优超平面 分n类非线性数据
  垃圾邮件识别、手写识别、文本分类

# 无监督学习
无已知样本 增量给出 [(x1,y1)...] 求解 x=a时 y=?聚类 数据分布


## 聚类算法 K-means 计算质心 聚类无标签数据  年龄分布聚集?
  消费水平评估、图像压缩
## 关联分析 挖掘啤酒与尿布 频繁项集 FP-growth
  营销策略、推荐算法
## PCA降维 减少数据维度，降低数据复杂度
## 深度学习 机器学习的分支
  cnn frcnn
  图像识别

## 打分模型

一般样本划分成训练集和验证集 如9:1
loss 训练集整体的损失值 
val_loss 验证集（测试集）整体的损失值 
当loss下降,val_loss下降 训练正常,最好情况 
当loss下降,val_loss稳定 网络过拟合化 这时候可以添加Dropout和Max pooling 
当loss稳定,val_loss下降 说明数据集有严重问题,可以查看标签文件是否有注释错误,或者是数据集质量太差 建议重新选择 
当loss稳定,val_loss稳定 学习过程遇到瓶颈,需要减小学习率（自适应网络效果不大）或batch数量 
当loss上升,val_loss上升 网络结构设计问题,训练超参数设置不当,数据集需要清洗等问题,最差情况 



调优参考
https://zhuanlan.zhihu.com/p/29534841









