
# 环境配置 命令执行注意事项
```bash
sh ./ bash dash各种语法错误
sh csh ksh bash dash
#!/bin/sh
#!/bin/bash    #功能全面
执行命令
在新的shell窗口环境执行sh
./test.sh  在当前的工作目录下执行test.sh
. test.sh  在当前shell窗口环境执行sh
test.sh    在环境变量中查找test.sh
/data/shell/test.sh    在指定路径下查找test.sh
bash /data/shell/test.sh    使用bash执行指定sh    不必赋予执行权限 不用文件第一行指定执行环境
sudo sh -c 'echo aaa > bbb.txt' 整体命令权限 管理员sudo重定向问题
sudo bash -c '' 两次执行的不是同一种shell，在用./sample的方式执行的时候，系统会使用脚本首行声明的/bin/bash来解释脚本，而用sh方式执行的时候，系统会调用sh
    echo xxx  | sudo tee -a bbb.txt
ll `which sh` 
    /bin/sh -> dash* 
    ln -s /bin/bash /bin/sh #连接替换sh dash？
    切换bash dash
    输入bash即可
	
系统 换行符
windows \r\n
unix \n
mac \r

## 环境变量 
/etc/profile, /etc/bashrc, .bash_profile, .bashrc
登陆Linux系统时：
首先启动”/etc/profile”；
然后启动 用户目录下的”~/.bash_profile” 附：(~/.bash_profile文件先调用~/.bashrc，然后再把PATH加载)；
如果”~/.bash_login”和”~/.profile”文件存在的时候也会在执行”~ /.bash_profile”后被依次调用。
各个文件的作用
/etc/profile：此文件为系统的每个用户设置环境信息,当用户第一次登录时,该文件被执行，并从/etc/profile.d目录的设置文件中搜集shell的设置；
/etc/bashrc：为每一个运行bash shell的用户执行此文件，当bash shell被打开时，该文件被读取；
~/.bash_profile：每个用户都可使用该文件输入专用于自己使用的shell信息，当用户登录时，该文件仅仅执行一次！默认情况下，他设置一些环境变量，执行用户的.bashrc文件，
~/.bashrc:该文件包含专用于你的bash shell的bash信息,当登录时及每次打开新的shell时,该文件被读取；
~/.bash_logout:当每次退出系统(退出bash shell)时,执行该文件；
区别
/etc/profile是全局性的功能，其中设置的变量作用于所有用户，~/.bash_profile中设置的变量能继承/etc/profile中的变量并作用于用户。
~/.bash_profile 是交互式、login 方式进入 bash 运行的；~/.bashrc 是交互式 non-login 方式进入 bash 运行的。
    export JAVA_HOME=/home/walker/software/jdk1.7.0_79
    export CLASSPATH=$JAVA_HOME/bin 
    export PATH=$PATH:$CLASSPATH
    source /etc/profile

    # export CLASSPATH=$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JAVA_HOME/bin


# source --help sh代码复制到当前shell
　　source命令或者"."，不会为脚本新建shell，而只是将脚本包含的命令在当前shell执行
# /dev/null  ： 空设备，是一个特殊的设备文件，弃一切写入其中的数据（但报告写入操作成功），读取它则会立即得到一个EOF。
    称为位桶(bit bucket)或者黑洞(black hole)。
    通常被用于丢弃不需要的输出流
    提供无限的空字符(NULL, ASCII NUL, 0x00)。
    nohup ./start.sh >/dev/null 2>&1 &      #正常日志丢弃 异常日志重定向标准输出
	
```

## 调用 命令、sh脚本

```bash
ll `which sh`    #查看 sh 软连接到了 bash
bash  #切换当前执行环境到bash
test.sh 脚本首行默认执行环境
#!/bin/sh
#!/bin/bash     
./test.sh 当前目录 执行 test.sh
. test.sh 在当前shell窗口环境 test.sh 复制文本到窗口执行 继承当前PATH export
source ./test.sh 相对绝对问题 cd `dirname $0`
test.sh     在 PATH 中查找执行 test.sh
/data/shell/test.sh  绝对/相对 执行
bash /data/shell/test.sh    使用bash执行 test.sh ! 不必权限(文件首行)
echo $(cd `dirname $0`; pwd -LP)    #脚本路径
#系统指令解释执行 指令传递 转义 替换
cmd=" ls "
${cmd}  #=键盘录入 ls 
eval ${cmd}  #=键盘录入 ls 一次变量解析替换 二次指令执行
echo ` eval echo '$'{"${k}"}` 变量取值变量
echo ` ${cmd} `  #=键盘录入 ls 执行结果放入echo

#行列 数组 分隔符ifs !!!
IFS_old=$IFS; echo "IFS_old: ${IFS_old}" 
IFS=$'\n' #更改为 $’\n’ 
xxxxxxxxxxxxxxxxxxxx
IFS=$IFS_old #恢复原IFS值
```

## 返回值
```bash
通过 return 返回 整数 0 正常 1 异常错误码
通过 
echo 'res'
res=`function` 
获取stdout输出返回值

```

## 权限 管道 重定向 输出日志文件

```bash
sudo sh -c 'echo aaa > bbb.txt 2>&1 '  管理员 sudo 整体命令重定向
echo xxx  | sudo tee -a bbb.txt 
nohup ./start.sh >/dev/null 2>&1 & echo $! > now.pid     #丢弃正常日志 执行异常2日志重定向标准输出1 后台&非挂载终端nohup执行 启动子pid文件

#管道/文件输入 密码
echo -e '222\nbbb' | ./exe_reader.sh
./exe_reader.sh < filename.txt
```
# 数据结构 变量  取值 运算 
shell中万物皆字符串 变量的值添加'，"和不添加没区别
## 赋值 取值 注意=空格不能多 
```bash
#全局变量
var=hello
var="hello ${world}" '${abc}'    # ' 绝对字符串 " 可转义 变量 
var=$(ls)  ; echo ${var}
var=` ls `  ; echo ${var}

#局部变量 函数中定义local  for 管道? 
  local var='local' 
```
## 整数 小数 进制
```bash
a=2 ; b=3 ; c=4 
echo 'expr 1 + ${a} = '`expr 1 + ${a} ` # + - * / %
echo '$((b*a)) = '$((b*a))
echo '$[a+1] = '$[a+1] 
echo "scale=4;1/7" | bc  #4位小数 
echo "obase=16;65535" | bc  #n进制
printf "0X%x\n" 65536   #n进制
let d=16#F00e  # 15#1AdE  #n进制定义
let f=0xff  011  ; echo ${f}  #空格分离?
let z=16#FFFf ; echo ${z}    #echo 命令十进制显示 

```
## 字符串 定义 截取substr 替换replace 分割split
```bash
str=` ls test* `  #!!! 非保护字符串 * 作为通配符
str='hello '"world`date`"of`date`; echo ${str}  #拼定字符串
len=${#str} ; echo '${#str}: '${len}  #长度 
str='http://www.www/aaa/bbb.ccc.html'

#按规则 截取 # % 保留左右  *key key*
v=${str#*//} ; echo '${var#*//}: '${v}  #最前//之后
filename=${str##*/} ; echo '${str##*/}: '${filename}  #bbb.ccc.html 最后/之后=文件名
dirParent=${str%/*}; echo '${str%/*}: '${dirParent}  #*/aaa 最后/之前=父目录 
ext=${str##*.} ; echo '${str##*.}: '${ext}  #html 最后.之后=文件类型
filenameOnly=${str%.*} ; echo '${str%.*}: '${filenameOnly}  #*/bbb.ccc 最后.之前=文件名 不要后缀

#按长度 截取 substring
echo ${str:1:5}  #substring(1, 5)
echo ${str:7} #substring(7, len)
echo ${str:0-7:3} #substring(len-7, len-7+3)
echo ${str:0-7}  #substring(len-7, len)

#按规则 替换 replace
str='www.www.www'
echo ${str/www/qqq}  #匹配第一个www    
echo ${str//www/qqq}   #匹配所有www
echo ${str/#www/qqq}  #匹配起始 ^www  
echo ${str/%www/qqq}  #匹配 www$ 结束 

#按规则 分离 split
str='abcd;efgh'
arr=(`  echo ${str} | tr ";" "\n"  `)  ; echo ${arr[@]}  # split( ';' ) 默认分隔符空格

```

## 数组
```bash
arr=(1 2 3)  #括号标记 默认分隔符空格
arr[5]=4 ; echo ${arr[5]}      #赋值 可不连续
unset arr[2] || unset arr    # 删除元素2 || 删除arr
str=${arr[*]} ; echo '${arr[*]}: '${str}    #转所有元素 * 取值 
str=${arr[@]} ; echo '${arr[@]}: '${str}    #.toString 转字符串 @ 
len=${#arr[@]} ; echo '${#arr[@]}: '${len}  #.length 
arrChild=(${arr[@]:1:4}) ; echo ${arrChild[@]}  #切片数组   
```

# 逻辑处理 执行 并行
```bash
true && echo a &&  ( echo c1; echo c2 )  #条件组合 !!(中exit隔离)
true && echo "this is error "  && exit 0 #条件退出sh正确方式 pr  return 0
false || echo b  
echo a; true; false; echo b    #单行多指令; 分隔 
```
## 分支 if 所有条件均 "  " 空格异常
```bash
a=1; b=2; c=123; str='hello123'

#[ expr ] test条件 !  -z -n -f -d   
[ ! -d "${str}" ] && echo "not dir ${str}"
  -d/f/e/s 存在dir/file/dir or file/filesize非空 0
  -r/w/x 可读/写/执行
  -eq/ne/lt/le/gt/ge =/!/</<=/>/>=
  
#[[ expr ]] 字符串条件 ! == ~= != =
  [[ "${str}" =~ .*llo.*  $regular<'.*Test.*'> ]]  #正则匹配
  [[ "${str}" == *llo* ]]  #模式匹配 
  [[ "${str}" != "hello123" ]]  #全值匹配    

#(( expr )) 算术运算条件 ! < > == !=
  (( ${a} == 2 )) && echo "a=2"

#if elif else 语法
 #单行写法
if (( ( ${a}==2 || ${a}!=3 ) && ${a}==1   )) ; then echo aaa; fi 
#单行简写 常用指令块
[ ! -d ${var} ] && ( mkdir -p ${var} ;  echo "mkdir ${var}" )  #确保文件夹(创建)
[ ! -d  ${fileTo%/*} ] && ( mkdir -p  ${fileTo%/*} ; echo "mkdir ${fileTo%/*}" )  #确保文件所在父目录(创建) 
 
#多行写法
if (( a==2 )) ; then 
  echo "if (( )) " 
elif [ -z "${str}" ]; then
  echo "elif [ ] "
elif [[ "${c}" == *12* ]]; then
  echo "elif [[ ]]"
else
  echo "else"
fi 

```
## 循环 i为local变量
```bash
arr=( ` ls ` ) 
while [[ "1" == "1" ]]
while true
for i in a b c
for i in {0..5}  #序列
for i in `seq 0 10`
for item in ${arr[@]}
for ((i=0; i<${#arr[@]}; i++))  ; do # !!! 序号依次
  item=${arr[$i]} 
  echo "item.${i}: ${item} "
done   

#单行写法常用
for i in `seq -w 0 10`; do echo ${i}; done
#遍历单词
for word in $line; do echo ${word}; done 
 #遍历字母
for((i=0;i<${#word};i++)); do key=${word:i:1}; echo "${i}.${key}"; done
#定时器
while true; do echo "`date '+%Y-%m-%d %H:%M:%S' `./do start ` "; sleep 1; done  
#日期序列模拟创建 历史修改记录 文件
tt=''; for i in `seq -w 0 365`; do  tt="mkfile-`  date -d \"${i} days\"  '+%Y%m%d%H%M%S'  `.txt"; echo ${tt}; echo ${i} > ${tt}; touch -d "`  date -d \"${i} days\" '+%Y-%m-%d %H:%M:%S'  `"  ${tt} ;  done 

#生成序列分表
tt=''; for i in `seq -w 0 99`; do tt="${tt},msg_entity_${i}"; done ; tt=${tt:1}; str='before '"${tt}"' after '; echo ${str} 
#获取路径列表中第一个有效路径
res=""; for i in "/home/t.txt" "/home/walker/t.txt" "./git-cmd.exe" ; do [ -f "${i}" ] && ( res=${i} ; echo ${res}; break ) done

#迭代文件每一行 注意尾行必须要有\n换行符号否则丢失最后行!!!
while read line;
do
  echo $line;
done < file.txt
cat file.txt | (while read line; do echo ${line}; done)
cat file.txt | awk '{print NR,$0}'

```
## 函数 
```bash
#调用 传参 空格分离 参数本身有空格 必须 ' " 保护 尽量保护
./do show aa bb 'cc' "d  d"    
$0  ./do  取参数,  执行路径相对
$#  5 参数个数,
$@   ".do" "show" "pp"  数组
$*  "./do show pp"  串
$?  0/1 函数返回值 上一条指令结果 
$$   59 当前进程pid
$! &进程pid?
shift 1	#移位 无法 ${${i}} ($#)--  $2->$1

函数返回方式 1.全局变量 2.eval $ 3.echo stdout 
function f()  
{  
    local  _arg=$1  
    local  res='value'  
    if [ -n "$1" ]; then  
        eval $_arg="'$res'"
    else  
        echo "$res"  
    fi  
}  
f r
r=`f r` 

#系统函数
printf "% 3d"$res''$obj"\n" "$i"   #格式化
sleep 1  #休眠 1s/1m/1h
wait       #等待 后台指令完成
echo $(($RANDOM%26))  #随机数 0 32767

 ```
 
