#!/usr/bin/python
#-*- coding:utf-8 -*-  

import os 
import sys
import glob as gb
import traceback

"""文件工具类

os.rename( "test1.txt", "test2.txt" )
os.remove("test.txt")
os.mkdir("newdir")
os.rmdir('dirname') 
os.chdir("/home/newdir") # 将当前目录  
os.getcwd() #当前的工作目录
gb.glob("/home/*")

"""

def open(filepath='./test.txt'):
	res = ''
	with open(filepath, 'r') as f:
		res = f.read()
	return res
def save(filepath='./test.txt', string='hello'):
	with open(filepath, 'w') as f:
		f.write(string)
def openByLine(filepath='./test.txt'):
	with open(filepath, 'w') as f:
		res = f.readlines()
	return res


"""
获取目录下  子目录及文件列表 用于 分类识别 测试
idf=file.getDirDirNames('./number')
[
	{
		  index : 0
		, dirname : 'd1'
		, files : [
					('file1.png', '/d1/file1.png')
					,( 'file2.png', 'd1/file2.png'  )
			   	  ]
	},
]
"""
def getDirDirNames(dirpath='D:\\Pictures\\pc\\model') :
	print('dirDirNames ' + dirpath)
	obj_path = gb.glob(dirpath + "/*")
	res=[]
	valueIndex = 0
	for path in obj_path:
		resd={}
		a, value, c = getFilePath(path)
		resd['index'] = valueIndex
		resd['dirname'] = value
		resd['files'] = []
		valueIndex = valueIndex + 1
		paths = gb.glob(path + "/*")
		for path3 in paths:
			pdir, nameOnly, ext = getFilePath(path3)
			resd['files'].append( (nameOnly + ext, path3) )

		res.append(resd)
	return res

def getLevel(path):
	res = 0
	strs = path.split("/")
	name = strs[-1]
	res = len(strs)
	#print("path:" + str(path) + " res:" + str(res) )
	return res
def pr(parent, filepath):
	#lev = getLevel(parent)
	for i in range(len(parent)) :
		#print(" ",)
		sys.stdout.write(" ")
	#sys.stdout.write("/" + filepath);
	filepath = os.path.join(parent, filepath)
	filesize = os.path.getsize(filepath)
	print(filepath + "\t@size=" + str(calSize(filesize)))

	return

def calSize(len) :
	gb = len / (1024 * 1024 * 1024) #GB
	mb = len % (1024 * 1024 * 1024) / (1024 * 1024) #MB
	kb = len % (1024 * 1024 * 1024) % (1024 * 1024) / 1024 #KB
	b  = len % (1024 * 1024 * 1024) % (1024 * 1024) % 1024 #B
	if gb > 0:
		res = str(gb) + "." + str(mb / 100) + "GB"
	elif mb > 0:
		res = str(mb) + "." + str(kb / 100) + "MB"
	elif kb > 0:
		res = str(kb) + "." + str(b / 100) + "KB"
	else :
		res = str(b) + "B"
	#print("" + str(len) + "->" + res)
	return res

# pdir, nameOnly, ext = file.getFilePath(imgSrc)
# ('a/b', 'c', '')
# ('c:/a/b/c', 'd', '.txt')
def getFilePath(fileUrl='c:/a/b/c/d.txt'):
	pdir, tmpfilename = os.path.split(fileUrl)
	nameOnly, ext = os.path.splitext(tmpfilename)
	return pdir, nameOnly, ext
def exists(file='D:/aaa.txt'):
	if os.path.exists(file):
		return True
	return False

# 创建文件所在目录
def mkdir(filepath='/home/test/test.txt'):
	if(filepath.endswith('/') or filepath.endswith('\\')):
		pass
	else:
		file_dir, nameOnly, ext = getFilePath(filepath)
	try:
		if ( not os.path.isdir(file_dir) ):
			os.makedirs(file_dir)
			print('mkdir', file_dir)
	except Exception as e:
		print(filepath, file_dir, str(e), traceback.format_exc())
	return

if __name__ == '__main__':
	pass
	mkdir("./__pycache__/Test/20210328-160858.png")