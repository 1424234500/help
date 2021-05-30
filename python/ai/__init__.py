# 如果目录中包含了 __init__.py 时，当用 import 导入该目录时，会执行 __init__.py 里面的代码。
# 如果目录中存在该文件，该目录就会被识别为 module package 。
# 控制包默认全部的导入限制
# from dirname import *
# __all__ = ['module_13', 'module_12', 'subPack2']

# 导入包默认执行
# 导入同级/lib模块 无需后缀.py
import json
import os
import sys
import time
import uuid
import threading
import random

# 导入子目录 模块 dirname下应有__init__.py
# from dirname import xxx
# import dirname.xxx as xxx
# 导入上级目录下的
sys.path.append("..")
import tool, file, ai
import matplotlib.pyplot as plt
