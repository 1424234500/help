# 一级# 文章标题
## _二级## 倾_斜_菜单_

==标记文本==
~~删除文本~~
小字 H~2~O 
幂2^10^
- [ ] 勾选框
- [x] 勾选框

外链[csdn](https://www.csdn.net/)
![Alt](https://imgconvert.csdnimg.cn/aHR0cHM6Ly9hdmF0YXIuY3Nkbi5uZXQvNy83L0IvMV9yYWxmX2h4MTYzY29tLmpwZw)


### 子菜单
- v1 item 项 * - + 空格
- v1 一级同符号相邻 否则额外行距
	+ v2 ✨支持缩进 ✨
		* v3 ✨ ✨
	+ v2 ✨Magic ✨

空行隔离  **分割线上空行**

---
### 引用 
[引用文献] 间隔字符串! [提示语=默认引用文献名 可指定引用][引用文献] 
> markdown标准规范问题
> [融合规范01 编辑器 dillinger.io] 
> [融合规范02 编辑器 csdn] 
> 引用标记行2  `行内部代码段`
不换行不隔离 

### 代码段
```bash
echo 代码段
while echo ls
```
### 表格
id | name | age 
 - | - | - 
1 | [plugins/dropbox/README.md][PlDb] |  15
2 | [plugins/github/README.md][PlGh] |

#### 文献引用清单
[//]: # (注释)
[name]:<url>
[引用文献]: <http://www.baidu.com?wd=引用>
[融合规范01 编辑器 dillinger.io]: <https://dillinger.io/>
[融合规范02 编辑器 csdn]: <https://blog.csdn.net/>


---

# csdn语法

*[HTML]:   超文本标记语言


<kbd>加框文本</kbd>
## 新的甘特图功能，丰富你的文章

```mermaid
gantt
        dateFormat  YYYY-MM-DD
        title Adding GANTT diagram functionality to mermaid
        section 现有任务
        已完成               :done,    des1, 2014-01-06,2014-01-08
        进行中               :active,  des2, 2014-01-09, 3d
        计划一               :         des3, after des2, 5d
        计划二               :         des4, after des3, 5d
```
- 关于 **甘特图** 语法，参考 [这儿](https://mermaidjs.github.io/),


## UML 图表

可以使用UML图表进行渲染。 [Mermaid](https://mermaidjs.github.io/). 例如下面产生的一个序列图：

```mermaid
sequenceDiagram
张三 ->> 李四: 你好！李四, 最近怎么样?
李四-->>王五: 你最近怎么样，王五？
李四--x 张三: 我很好，谢谢!
李四-x 王五: 我很好，谢谢!
Note right of 王五: 李四想了很长时间, 文字太长了<br/>不适合放在一行.

李四-->>张三: 打量着王五...
张三->>王五: 很好... 王五, 你怎么样?
```

这将产生一个流程图。:

```mermaid
graph LR
A[长方形] -- 链接 --> B((圆))
A --> C(圆角长方形)
B --> D{菱形}
C --> D
```

- 关于 **Mermaid** 语法，参考 [这儿](https://mermaidjs.github.io/),

## FLowchart流程图

我们依旧会支持flowchart的流程图：
```mermaid
flowchat
st=>start: 开始
e=>end: 结束
op=>operation: 我的操作
cond=>condition: 确认？

st->op->cond
cond(yes)->e
cond(no)->op
```

- 关于 **Flowchart流程图** 语法，参考 [这儿](http://adrai.github.io/flowchart.js/).
