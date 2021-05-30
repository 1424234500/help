
## 系统信息
```bash
# 内核
cat /proc/version 
Linux version 4.15.0-45-generic (buildd@lgw01-amd64-031) (gcc version 7.3.0 (Ubuntu 7.3.0-16ubuntu3)) #48-Ubuntu SMP Tue Jan 29 16:28:13 UTC 2019

# 发行版
cat /etc/issue 
Ubuntu 18.04.1 LTS \n \l

# cpu信息
cat /proc/cpuinfo

```

## 基本命令
```

端口 21 FTP 22 SSH 23 TELNET
du -sh * # 查看文件大小占用 ls -lth
df -h  # 磁盘

# 查看指令来源
whereis ll
which	ll
whatis ls

man/info ls # 帮助文档
ls -lht <l>长信息 <h>size转换 <t>时间排序 <S>size排序 <d> 只显示目录
--time-style="+%Y-%m-%d %H:%M:%S"


type ls # 查看res
date --version / -v  # --引领单词


# 多任务切换
CTRL+Z 挂起进程后台
jobs 显示后台list
bg 1 使第1个任务在后台运行
fg 1 使第1个任务在前台运行

id  #查看当前用户组及其他状态
last #查看ssh记录
history	#cmd历史
wait #等待所有&执行完毕
ldconfig 启动时运行 动态链接库时手工运行。

```

## vim --help less > more
```bash
esc :set number 显示行号
esc :set nu
esc /str 查找1 正向 支持 * 通配符号
esc :{作用范围}s/{目标}/{替换}/{替换标志} g标示每行所有命中 全文替换 不要则只匹配每行第一个命中
	:%s/foo/bar/g
esc ?str 查找2 反向  n next  shift+n/N previous
esc shift + * 查找当前所在单词
esc G shift + g 滚动最底部
esc gg  滚动最顶部
esc yw 复制当前到单词结尾
esc p paste粘贴
撤销：u
恢复撤销：Ctrl + r
```
## eval xargs  kill --help
```bash
    st="ls | more"
    `$st`  ####将 | 和 more 看成了参数，而不是将文件按页显示
    eval $st      ####双次解析 一次解析变量 二次 放置执行？ 同js php shell
timeout 3 sleep 10 #超时机制 所有指令
#杀死指定规则进程pid获取 #字符分离数组 #截取
    '239 39234 2343' | xargs kill -9
    kill -9 25718 25719 25811 25812 依次排在后边
    killall nginx #删除所有依据名字
ps -elf | cut -c 9-15 | kill -9
    ps -elf | grep <-v反转> 'aaa'
    xargs的默认命令是echo，空格是默认定界符
    xargs入模式
        -p 请求输入
        -d 指定分隔符
    echo "--help" | cat
    echo "--help" | xargs cat
    cat test.txt | xargs -n3 ####多行
    cat test.txt | xargs -d'S' ####设定分隔符
    arg.txt :
        file1.txt
        file2.txt
    cat arg.txt | xargs -I {} cat -p {} -l  ####{}占位符 替换
    ->
    cat -p file1.txt -l
    cat -p file2.txt -l
```
# strings --help    用于分析dump内存 过滤特殊字符
```bash
用法：strings [选项] [文件]
打印 [文件] (默认为标准输入) 中可打印的字符串 
  -a - --all                Scan the entire file, not just the data section [default]
  -d --data                Only scan the data sections in the file
  -f --print-file-name      Print the name of the file before each string
  -n --bytes=[number]      Locate & print any NUL-terminated sequence of at
  -<number>                  least [number] characters (default 4).
  -t --radix={o,d,x}        Print the location of the string in base 8, 10 or 16
  -w --include-all-whitespace Include all whitespace as valid string characters
  -o                        An alias for --radix=o
  -T --target=<BFDNAME>    Specify the binary file format
  -e --encoding={s,S,b,l,B,L} Select character size and endianness:
                            s = 7-bit, S = 8-bit, {b,l} = 16-bit, {B,L} = 32-bit
  -s --output-separator=<string> String used to separate strings in output.
  @<file>                  Read options from <file>
  -h --help                Display this information
  -v -V --version          Print the program's version number
```
## awk --help 字符分割 格式化
```bash
awk [-F|-f|-v] ‘BEGIN{} ####{command1; command2} END{}’ file
    -F指定分隔符，-f调用脚本，-v定义变量 var=value
    '  '          引用代码块
    BEGIN  初始化代码块，在对每一行进行处理之前，初始化代码，主要是引用全局变量，设置FS分隔符
    //          匹配代码块，可以是字符串或正则表达式
    {}          命令代码块，包含一条或多条命令
    ；          多条命令使用分号分隔
    END      结尾代码块，在对每一行进行处理之后再执行的代码块，主要是进行最终计算或输出结尾摘要信息
    $0          表示整个当前行
    $1          每行第一个字段
    NF          字段数量变量   
    NR          每行的记录号，多文件记录递增
    FNR        与NR类似，不过多文件记录不递增，每个文件都从1开始 
    FS          BEGIN时定义分隔符
    RS      输入的记录分隔符， 默认为换行符(即文本是按一行一行输入)
    FILENAME 文件名
    OFS      输出字段分隔符， 默认也是空格，可以改为制表符等
    ORS        输出的记录分隔符，默认为换行符,即处理结果也是一行一行输出到屏幕
    -F'[:#/]'  定义三个分隔符

ps -lf | awk -Fwalker '{print NR,NF,$1,$NF}' OFS="\t"
ps -lf | awk -F" " 'NR!=1{print NR,NF,$1,$NF,($3>100 ? "yes":"no")}' OFS="\t" #不要第一行
-F'[ :]'  #' ' || '"' 多分隔符

代码段落处理

ps -lf | awk -F" " '
BEGIN{before=0;after=0;deta=5000}
{
    res=system("date")
    if($4>deta){
        after++;
        print $4,"large",$4">"deta
    }
    else {
        before++;
        print $4,"small----",$4"<"deta;
        print $4,"small",$4"<"deta

    }
}
END{printf "Total before:%-8s after:%-8s\n", before, after}
'

```

## sed --help 字符替换
```bash
用法: sed [选项]... {脚本(如果没有其他脚本)} [输入文件]...
  -r    -regexp-extended    扩展正则!!!!!!!
  -n, --quiet, --silent
                取消自动打印模式空间
  -e 脚本, --expression=脚本
                添加“脚本”到程序的运行列表
  -f 脚本文件, --file=脚本文件
                添加“脚本文件”到程序的运行列表
  --follow-symlinks
                直接修改文件时跟随软链接
  -i[SUFFIX], --in-place[=SUFFIX]
  -i.backup    添加备份文件命名
                edit files in place (makes backup if SUFFIX supplied)
  -l N, --line-length=N
                指定“l”命令的换行期望长度
  --posix
                关闭所有 GNU 扩展
  -E, -r, --regexp-extended
                use extended regular expressions in the script
                (for portability use POSIX -E).
  -s, --separate
                consider files as separate rather than as a single,
                continuous long stream.
      --sandbox
                operate in sandbox mode.
  -u, --unbuffered
                从输入文件读取最少的数据，更频繁的刷新输出
  -z, --null-data
                使用 NUL 字符分隔各行
      --help    打印帮助并退出
      --version  输出版本信息并退出

如果没有 -e, --expression, -f 或 --file 选项，那么第一个非选项参数被视为
sed脚本。其他非选项参数被视为输入文件，如果没有输入文件，那么程序将从标准
输入读取数据。
| sed -r "s%aaaaa%bbbbb%g 切换分隔符！！！
| sed -r 's/[0-9]{8}.BIN/20200102.BIN/g'
#取出5-10行
sed -n '5,10p' obcp-server29.log
#文件行管道替换
cat redis_cluster_7000.conf | sed s/7000/7001/g
#文件整体替换
sed -i.back "s/oldstring/newstring/g"   test.cnf
sed -i.back "s/oldstring/newstring/g"    `grep oldstring -rl yourdir`
#替换输出
sed s/7000/7002/ redis_cluster_7000.conf
#去掉控制台颜色代码##########
edjfl | sed -r "s/\x1B\[([0-9]{1,2}(;[0-9]{1,2})?)?[m|K]####g"

```

## find --help
```bash
    Usage: find [-H] [-L] [-P] [-Olevel] [-D debugopts] [path...] [expression]
    默认路径为当前目录；默认表达式为 -print
    表达式可能由下列成份组成：操作符、选项、测试表达式以及动作：
    操作符 (优先级递减；未做任何指定时默认使用 -and):
          ( EXPR )  ! EXPR  -not EXPR  EXPR1 -a EXPR2  EXPR1 -and EXPR2
          EXPR1 -o EXPR2  EXPR1 -or EXPR2  EXPR1 , EXPR2
    位置选项 (总是真): -daystart -follow -regextype
    普通选项 (总是真，在其它表达式前指定):
          -depth --help -maxdepth LEVELS -mindepth LEVELS -mount -noleaf
          --version -xdev -ignore_readdir_race -noignore_readdir_race
    测试(N可以是 +N 或-N 或 N):-amin N -anewer FILE -atime N -cmin 
          -cnewer 文件 -ctime N -empty -false -fstype 类型 -gid N -group 名称
          -ilname 匹配模式 -iname 匹配模式 -inum N -ipath 匹配模式 -iregex 匹配模式
          -links N -lname 匹配模式 -mmin N -mtime N -name 匹配模式 -newer 文件
          -nouser -nogroup -path PATTERN -perm [-/]MODE -regex PATTERN
          -readable -writable -executable
          -wholename PATTERN -size N[bcwkMG] -true -type [bcdpflsD] -uid N
          -used N -user NAME -xtype [bcdpfls]      -context 文本
find test</> | grep .png #查找当前路径 下 所有文件 深度优先 的 png图片文件
find test</> -name '.*.png'
find test -path "./Documents" -prune -o -path "./Desktop" -prune -o -name '.*.png' -o -name '*xml'      #例外 多个文件夹跳过  匹配文件
[-o or  -a and  ! not  逻辑运算]
[-path "./Desktop"  路径匹配]
[-name "*.xml"  名字匹配]
[-iname "*.xMl" 忽略大小写名字匹配] 
[-maxdepth 3    深度递归]
[-perm 777  权限]
[-user walker  用户]
[-group sunk    用户组]
[-size -10k 文件大小少于10k M G +大于]
[-mtime -7  -七天f前 +七天内 time天 min分 a访问 m修改 c权限改动]
[-prune 不递归子目录]
[-type f 文件]
[-empty 空文件]
[-exec rm -rf {} \  文件路径替换操作执行!]
find ./ -maxdepth 4 -type d   

find /var/svn/svnbackup -type f -name "new_*" -mtime +7 -exec rm -rf {} \;  #删除/var/svn/svnbackup目录下创建时间为7天之前，并且文件以new开头的的所有文件或文件夹； 
find ./ * -mtime 0
      -mtime -7 表示七天之内;
      -mtime +7 表示七天之前;
      -mtime 0  表示1天之内;
	  
```
#### grep --help
```bash
grep [OPTIONS]PATTERN [FILE...]
    PATTERN:是文本字符和正则表达式的元字符组合而成的匹配条件，
    用单引号‘ ’将pattern括起来以避免shell通配的影响，强引用不替换而显示字符本身。" " 双引号，
    字符串中的` ` ,$, \ 等特殊字符会被shell解释替换后，再传递给grep。
    对普通的字符串（没有特殊字符和空格的字符串）也可以不加引号，直接搜索。
    OPTIONS：（这里给出常用的选项）
    -i 忽略大小写
    -c 显示被匹配到的行数
    -n 输出行号
    -v 反向选择，即找没有搜索字符串的行  #############3
    -o 仅显示匹配到的内容  grep -oe<只显示匹配内容><-C 5 前后五行><-A 5 前><-B 5 后> '.*\[.*\].*' test.sh
    -w 匹配单词
    -A # 连同匹配行的下#行一并显示，#代表任意数字
    -B # 连同匹配行的上#行一并显示，#代表任意数字
    -C # 连同匹配行的上下#行一并显示，#代表任意数字
    -l 只显示命中的文件名
    -E  相当于egrep 支持扩展的正则表达式    三种模式正则 grep 转义 \|  \+
#    https://blog.csdn.net/yufenghyc/article/details/51078107
#抓取ip port 格式化输出并排序
    cat ips.txt | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+\.[0-9]\+\:[0-9]\+" | awk -F':' '{print $1,$2}' OFS="\t" | sort -k 1 -n

    -F  相当于fgrep 不支持正则表达式
    --color对匹配的内容以颜色显示
    -V  显示grep版本
    -R
    -r 递归搜索目录或子目录下匹配的字所在文件 可配合find命令 ###############
grep -rl 7000 ./*  #匹配所有文件子目录文件 输出概要或者文件列表
grep "7000" file1.txt file2.txt file3.txt  #匹配多个文件
grep "7000" `find ./ -name "*conf" -o -name "*conf3" `  #匹配 查找出的文件列表  并过滤一个子列表
grep -C 10 -inoe  '.*MccpMgr.*' obcp-server29.log | less
grep -ne  'getUserBean\|device:null' obcp-server29.log | grep -v '.*DEBUG.*'| grep -v '.*INFO.*' | less

```

## wc --help tr --help base64 --help 
```bash
wc -l file #### 统计行数
wc -w file #### 统计单词数
wc -c file #### 统计字符数
echo '123456' | base64  #编码
echo "a b c" | tr ' ' "\n"  #行列转换
```

## date --help
```bash
ntpd -s -d  ####自动同步
配置服务
vim /etc/ntpconf
# You do need to talk to an NTP server or two (or three).
# server ntp.your-provider.example
在下面添加以下内容，是一些亲测可用的ntp服务器。第一行最后的perfer表示优先使用此服务器，也就是复旦大学的ntp服务器。添加之后按Ctrl+X保存退出。
server ntp.fudan.edu.cn iburst perfer
server time.asia.apple.com iburst
server asia.pool.ntp.org iburst
server ntp.nict.jp iburst
server time.nist.gov iburst
/etc/init.d/ntp restart    ####重启
date --set="1999-01-01 08:00:00" # 设置时间

date +%Y-%m-%d
2013-02-19 
date "+%H:%M:%S" 
13:13:59 
date "+%Y-%m-%d %H:%M:%S"     # 2013-02-19 13:14:19 
date "+%Y%m%d-%H%M%S"        # 2013-02-19 13:14:19
date -d today 
date -d now 
date -d tomorrow  "+%Y-%m-%d %H:%M:%S"
date -d yesterday 
date -d "1 days"    # second | minutes | hours | days | months | years |
date -d "-1 days"
Mon Feb 18 13:11:58 CST 2013 
date -d now +%s #到s级别
date -d "2019-02-11 13:14:19" +%s #到s级别
1549862059
date -d @1599506957"+%Y-%m-%d %H:%M:%S"  #反转
2019-02-11
```

## top --help memory ps top
```bash
    top <-H, 查看线程级别>
        <-p 2833, 查看指定pid>
        <-b -n 1, 非交互模式, 只跑一次> 
        <-u walker, 只看某用户>
-c 显示完整的命令
-I 忽略失效过程
-s 保密模式
-S累积模式
-i<时间> 设置间隔时间
-u<用户名> 指定用户名
-n<次数>循环显示的次数
    top -b -n 1 -i -c
    top - 16:00:00 up 1 day,  7:20,  1 user,  load average: 1.93, 1.48, 0.90 
    #uptime 运行时间 登录用户数量 平均负载 5/10/15分钟
    任务: 285 total,  2 running, 233 sleeping,  0 stopped,  0 zombie
    #进程数 总共 运行 休眠 停止 僵尸
    %Cpu(s):  8.2 us,  1.9 sy,  0.0 ni, 88.9 id,  1.0 wa,  0.0 hi,  0.0 si,  0.0 st
    #cpu使用 user用户 sys系统 nice调优 idle空闲 wait-io等待 hi-cpu处理硬中断 si-cpu处理软中断 st-虚拟机偷走的cpu
    #满负荷运行cpu的使用率最好是user空间保持在65%～70%，system空间保持在30%，空闲保持在0%~5% 。
    KiB Mem :  8084668 total,  807312 free,  4124104 used,  3153252 buff/cache
    KiB Swap:  1755988 total,  1755988 free,        0 used.  3252680 avail Mem
    #free 全部可用内存、已使用内存、空闲内存、缓冲内存
    进�� USER      PR  NI    VIRT    RES    SHR �  %CPU %MEM    TIME+ COMMAND
    3332 walker    20  0 1829648 224564  64068 R 111.8  2.8  8:54.95 gedit
      754 root      20  0  47136  27848  2384 S  29.4  0.3  3:09.34 /sbin/moun+
      878 message+  20  0  51692  6164  3912 S  5.9  0.1  0:15.43 /usr/bin/d+
    22747 walker    20  0  51360  4004  3388 R  5.9  0.0  0:00.02 top -bn 1 +
    PR 进程的调度优先级。这个字段的一些值是’rt’。这意味这这些进程运行在实时态。
    NI 进程的nice值（优先级）。越小的值意味着越高的优先级。
    VIRT 进程使用的虚拟内存。
    RES 驻留内存大小。驻留内存是任务使用的非交换物理内存大小。
    SHR SHR是进程使用的共享内存。
    S 这个是进程的状态。它有以下不同的值:
        D – 不可中断的睡眠态。
        R – 运行态
        S – 睡眠态
        T – 被跟踪或已停止
        Z – 僵尸态
    %CPU 自从上一次更新时到现在任务所使用的CPU时间百分比。
    %MEM 进程使用的可用物理内存百分比。
    TIME+ 任务启动后到现在所使用的全部CPU时间，精确到百分之一秒。
    COMMAND 运行进程所使用的命令。
proc/stat节点记录的是系统进程整体的统计信息
获取pid父进程关系链
cat /proc/5164/stat

# show memory
    free -h
    cat /proc/meminfo  #(free / ps / top)等的组合显示
    vmstat <1 sleep> <5 count>
    procs -----------memory---------- ---swap-- -----io---- --system-- -----cpu-----
关于was内存持续升高稳定占用80%问题   
    #仅清除页面缓存（PageCache）
    sync; echo 1 > /proc/sys/vm/drop_caches     
    #清除目录项和inode
    sync; echo 2 > /proc/sys/vm/drop_caches     
    #清除页面缓存，目录项和inode
    sync; echo 3 > /proc/sys/vm/drop_caches 
```

## ps --help
```bash
    ps H -eo user,pid,ppid,tid,time,%cpu --sort=+%cpu  #cpu使用倒序
    ps是显示瞬间进程的状态，并不动态连续；如果想对进程进行实时监控应该用top命令
    命令 含义
      -e 显示所有进程,环境变量
        f 全格式
        h 不显示标题
        l 长格式
        w 宽输出
        a 显示终端上地所有进程,包括其他用户地进程
        r 只显示正在运行地进程
        x 显示没有控制终端地进程
        u 以用户为主的格式来显示程序状况
        au 显示较详细的资讯
        aux 显示所有包含其他使用者的行程
        -o c,C,f,g,G    按照指定格式输出
        args：进程名(command)
            c cmd  可执行地简单名称
            C cmdline  完整命令行
            f flags  长模式标志
            g pgrp  进程地组ID
            G tpgid  控制tty进程组ID
            j cutime  累计用户时间
            J cstime  累计系统时间
            k utime  用户时间
            K stime  系统时间
            m min_flt  次要页错误地数量
            M maj_flt  重点页错误地数量
            n cmin_flt 累计次要页错误
            N cmaj_flt 累计重点页错误
            o session  对话ID
            p pid  进程ID
            P ppid  父进程ID
            r rss  驻留大小
            R resident 驻留页
            s size  内存大小(千字节)
            S share  共享页地数量
            t tty  tty次要设备号
            T start_time 进程启动地时间
            U uid  UID
            u user  用户名
            v vsize  总地虚拟内存数量(字节)
            y priority 内核调度优先级
```
## sort --help
```bash
    ps | sort -r    #字符串空排前
    sort 选项与参数：
    -f  ：忽略大小写的差异，例如 A 与 a 视为编码相同；
    -b  ：忽略最前面的空格符部分；
    -M  ：以月份的名字来排序，例如 JAN, DEC 等等的排序方法；
    -n  ：使用『纯数字』进行排序(默认是以文字型态来排序的)；
    -r  ：反向排序；
    -u  ：就是 uniq ，相同的数据中，仅出现一行代表；
    -t  ：分隔符，默认是用 [tab] 键来分隔；
    -k  ：以那个区间 (field) 来进行排序的意思
    ps -eo rss,pmem,pcpu,vsize,args |  sort -k 1 -r -n | less
        sort命令对ps结果进行排序
        -k 1 :按第一个参数 rss进行排
        -r：逆序
        -n：numeric，按数字来排序
    ps --sort=[+|-] key
    按CPU降序排列：ps aux --sort=[-|+]%cpu
    pstree  以显示进程信息。它以树的形式显示
    kill -9
    pgrep 会返回所有匹配这个关键词的进程ID。例如，你可以使用以下命令寻找Firefox的PID: pgrep firefox
    pkill & killall pkill和killall命令可以根据进程的名字杀死一个进程。使用以下任一方法都可以杀死Firefox进程： pkill firefox  killall firefox
    renice 用来改变进程的nice值。nice值代表进程的优先级。renice 19 pid    -19的nice值是非常高的优先级，相反，19是非常低的优先级。0是默认的优先级。
```
	
## uniq --help    统计计数
```bash
用法：uniq [选项]... [文件]
Filter adjacent matching lines from INPUT (or standard input),
writing to OUTPUT (or standard output).
With no options, matching lines are merged to the first occurrence.
必选参数对长短选项同时适用。
  -c, --count          prefix lines by the number of occurrences 计数相邻同名
  -d, --repeated        only print duplicate lines, one for each group
  -D                    print all duplicate lines
  --all-repeated[=METHOD]  like -D, but allow separating groups
with an empty line;
METHOD={none(default),prepend,separate}
  -f, --skip-fields=N  avoid comparing the first N fields
  --group[=METHOD]  show all items, separating groups with an empty line;
  METHOD={separate(default),prepend,append,both}
  -i, --ignore-case    ignore differences in case when comparing
  -s, --skip-chars=N    avoid comparing the first N characters
  -u, --unique          only print unique lines
  -z, --zero-terminated    line delimiter is NUL, not newline
  -w, --check-chars=N 对每行第N 个字符以后的内容不作对照
  --help 显示此帮助信息并退出
--version 显示版本信息并退出
```


## netstat --help
```bash
usage: netstat [-vWeenNcCF] [<Af>] -r        netstat {-V|--version|-h|--help}
  netstat [-vWnNcaeol] [<Socket> ...]
  netstat { [-vWeenNac] -i | [-cnNe] -M | -s [-6tuw] }
-r, --route              显示路由表
-i, --interfaces        display interface table
-g, --groups            display multicast group memberships
-s, --statistics        display networking statistics (like SNMP)
-M, --masquerade        display masqueraded connections
-v, --verbose            显示详细信息
-W, --wide              don't truncate IP addresses
-n, --numeric            不解析名称
--numeric-hosts          不解析主机名
--numeric-ports          忽略端口名称
--numeric-users          忽略用户名
-N, --symbolic          resolve hardware names
-e, --extend            显示更多信息
-p, --programs          display PID/Program name for sockets
-o, --timers            display timers
-c, --continuous        continuous listing
-l, --listening          display listening server sockets
-a, --all                display all sockets (default: connected)
-F, --fib                display Forwarding Information Base (default)
-C, --cache              display routing cache instead of FIB
-Z, --context            display SELinux security context for sockets
  <Socket>={-t|--tcp} {-u|--udp} {-U|--udplite} {-S|--sctp} {-w|--raw}
  {-x|--unix} --ax25 --ipx --netrom
  <AF>=Use '-6|-4' or '-A <af>' or '--<af>'；默认： inet
netstat -ano  所有 包括 udp
netstat -antl 所有 tcp

```
## telnet --help 通过 cmd 依靠ip/端口/用户名密码 远程登录
```bash
    service openbsd-inetd start 
    /etc/init.d/openbsd-inetd restart
    1、首先查看telnet运行状态
    #netstat -a | grep telnet
    输出为空，表示没有开启该服务

    5、查看telnet运行状态
    #netstat -a | grep telnet
    输出：tcp　　0　　0 *:telnet　　*:*　　LISTEN
    此时表明已经开启了telnet服务。

        Telnet 客户端命常用命令：
    　　open : 使用 openhostname 可以建立到主机的 Telnet 连接。
    　　close : 使用命令 close 命令可以关闭现有的 Telnet 连接。
    　　display : 使用 display 命令可以查看 Telnet 客户端的当前设置。
    　　send : 使用 send 命令可以向 Telnet 服务器发送命令。支持以下命令：
    　　ao : 放弃输出命令。
    　　ayt : “Are you there”命令。
    　　esc : 发送当前的转义字符。
    　　ip : 中断进程命令。
    　　synch : 执行 Telnet 同步操作。
    　　brk : 发送信号。
    　　上表所列命令以外的其他命令都将以字符串的形式发送至 Telnet 服务器。例如，sendabcd 将发送字符串 abcd 至 Telnet 服务器，这样，Telnet 会话窗口中将出现该字符串。
    　　quit
```
## mv --help touch --help
```bash
    for i in `seq -w 10`; do touch -d "${i}/11/2011}" stu\_$i\_linux.jpg ; done #批量重命名
    touch -d "10/11/2011" ttt.txt2  #修改文件时间 文件修改时间
    touch -d  `  date -d '1 days' '+%Y-%m-%d %H:%M:%S'  ` test.txt
    rename \_linux '' *.jpg
    rename '\_linux' '' *.jpg           
    例子：将目录A重命名为B
    mv /a /b/c
    mv abc 1234
#批量操作 重命名
# *_?.jpg >  *_0?.jpg：
for var in `ls *_?.jpg`; do mv "$var" `echo "$var" |awk -F '_' '{print $1 "_0" $2}'`; done
8、把文件名的前三个字母变为 vzomik：
for var in `ls`; do mv -f "$var" `echo "$var" |sed 's/^.../vzomik/'`; done
#*.txt -> *.txt_bak
ls *.txt|xargs -n1 -i{} mv {} {}_bak
xargs -n1 –i{} 类似for循环，-n1意思是一个一个对象的去处理，-i{} 把前面的对象使用{}取代
find ./*.txt -exec mv {} {}_bak \;  
”\”为”;”转义

```
 
## echo --help 回响 标准输出
```bash
echo -e ${PATH}
-n 不尾随换行符 文件追加 lf lrlf异常
-e 启用解释反斜杠的转义功能
-E 禁用解释反斜杠的转义功能(默认)
--version 显示版本信息并退出
若-e 可用，则以下序列即可识别：
  \\    反斜杠
  \a    响铃声
  \b    退格
  \c    不再产生新的输出
  \e    转义符 
  \f    换页
  \n    新行
  \r    回车
  \t    水平制表符
  \v    竖直制表符
  \0NNN  字节数以八进制数 NNN (1至3位)表示    echo -e \x888
  \xHH    字节数以十六进制数 HH (1至2位)表示


```
## bc --help printf --help 进制转换 赋值
```bash
    let i=16#ff
    let aaa=n#[0 - n-1] #n进制定义
    let i=0xff  011
    echo 命令以十进制显示数据
    ((var=base#number));echo $var
    printf "%x\n" 65536

    bc命令格式转换
    echo "obase=进制;值" | bc
    echo "obase=16;65536" | bc
```

## tar --help zip --help 7z --help 解压问题
```bash
    语法：tar [主选项+辅选项] 文件或者目录
    使用该命令时，主选项是必须要有的，它告诉tar要做什么事情，辅选项是辅助使用的，可以选用。
    主选项：
    c 创建新的档案文件。如果用户想备份一个目录或是一些文件，就要选择这个选项。相当于打包。
    x 从档案文件中释放文件。相当于拆包。
    t 列出档案文件的内容，查看已经备份了哪些文件。
    特别注意，在参数的下达中， c/x/t 仅能存在一个！不可同时存在！因为不可能同时压缩与解压缩。
    辅助选项：
    -z ：是否同时具有 gzip 的属性？亦即是否需要用 gzip 压缩或解压？ 一般格式为xx.tar.gz或xx. tgz
    -j ：是否同时具有 bzip2 的属性？亦即是否需要用 bzip2 压缩或解压？一般格式为xx.tar.bz2 
    -v ：压缩的过程中显示文件！这个常用
    -f ：使用档名，请留意，在 f 之后要立即接档名喔！不要再加其他参数！
    -p ：使用原文件的原来属性（属性不会依据使用者而变）
-P : 避免绝对路径文件提示不合法s
    -A
    xz -d linux-3.12.tar.xz && tar -xvf linux-3.12.tar
    tar -xvJf  node-v6.10.1-linux-x64.tar.xz

    tar -tvf  file.gz  #查看tar包文件列表
    tar -xvf file.tar ####解压 tar包
    tar -xzvf file.tar.gz -C file1 ####解压tar.gz  并重命名
    tar -xjvf file.tar.bz2 ####解压 tar.bz2
    tar -xzvf file.tar.Z ####解压tar.Z
    --exclude FILE  在压缩的过程中，不要将 FILE 打包！
tar -czvf file.tar.gz --exclude=*logs* --exclude=*.jar --exclude=/dir/*
    将整个 /etc 目录下的文件全部打包成为 /tmp/etc.tar
    tar -cvf /tmp/etc.tar /etc　　　　<==仅打包，不压缩！
    tar -czvf /tmp/etc.tar.gz /etc　　<==打包后，以 gzip 压缩
    tar -cjvf /tmp/etc.tar.bz2 /etc　　<==打包后，以 bzip2 压缩
    tar -rvf file.tar test.txt  #追加文件 追加操作只针对没有压缩的tar包才有效

    unrar e file.rar ####解压rar
    zip -r xxx.zip ./*  #当前目录的内容为xxx.zip文件
    unzip file.zip ####解压zip
    ####对于.7z
    支持 7Z,ZIP,Zip64,CAB,RAR,ARJ,GZIP,BZIP2,TAR,CPIO,RPM,ISO,DEB 压缩文件格式
    安装： apt-get install p7zip p7zip-full p7zip-rar
    7z a yajiu.7z yajiu.jpg yajiu.png 将yajiu.jpg和yajiu.png压缩成一个7z包
    7z a yajiu.7z *.jpg 将所有.jpg的文件压缩成一个7z包
    7z a yajiu.7z yajiu 将文件夹yajiu压缩成一个7z包
    7z e yajiu.7z 将yajiu.7z中的所有文件解压出来，e是解压到当前路径
    7z x yajiu.7z 将yajiu.7z中的所有文件解压出来，x是解压到压缩包命名的目录下
```

## 初次登录ubuntu的root登录问题
    输入 root 密码 安装时 设置的是用户密码 而不是root 密码 ununtu 只能调用 root 不能直接 root登录
    输入 passwd root
## 定时任务
```bash
crontab -e #编辑
crontab -l  #列表
执行日志 tail -f /var/spool/mail/root
Cron是Unix系统的一个配置定期任务的工具，用于定期或者以一定的时间间隔执行一些命令或者脚本； 基于每个用户的，每一个用户（包括root用户）都拥有自己的crontab。
*/1 * * * * date >> ~/logs/crontab.log  #定时每m测试crontab状况
*/5 * * * * /usr/local/tomcat-6.0.41/tomcat_cardniu_stat/monitor.sh ####增量5m
  0 0 * * *  /home/pi/backup.sh ####0h0m
注意!!!!
%是有特殊含义 表示换行    常用的date +%Y%m%d在crontab里是不会执行的，应该换成date +\%Y\%m\%d
上下文环境变量不会加载 可手动加载    多条语句时，用分号“；”隔开
*/1 * * * * . /etc/profile; echo `date "+\%Y-\%m-\%d \%H:\%M:\%S"`" crontab trigger 1m " >> ~/logs/crontab.log  #定时每m测试crontab状况
#### service crond restart
service cron status
/etc/init.d/cron {start|stop|status|restart|reload|force-reload} ####重启服务
其中排列意思为：
http://cron.qqe2.com/
Bash
#    m    h    dom    mon    dow    user    command
#  分    时    日    月      周    用户    命令
#
#      m:表示分钟1～59 每分钟用*或者 */1表示 0表示整点 *表示启动时间开始 每增加/1单位
#      h:表示小时1～23（0表示0点）  21-23，23-6
#    dom:表示日期1～31
#    mon:表示月份1～12
#    dow:标识号星期0～6（0表示星期天）
#    user:表示执行命令的用户
# command:表示要执行的命令
#
#  * 代表任意数值
例程如下：
Bash
    30 21 * * * /usr/local/etc/rc.d/lighttpd restart
    #每晚的21:30重启apache。
    45 4 1,10,22 * * /usr/local/etc/rc.d/lighttpd restart
    #每月1、10、22日的4 : 45重启apache。
    10 1 * * 6,0 /usr/local/etc/rc.d/lighttpd restart
    #每周六、周日的1 : 10重启apache。
    0,30 18-23 * * * /usr/local/etc/rc.d/lighttpd restart
    #在每天18 : 00至23 : 00之间每隔30分钟重启apache。
    0 23 * * 6 /usr/local/etc/rc.d/lighttpd restart
    #每星期六的11 : 00 pm重启apache。
    * 0/1 * * * /usr/local/etc/rc.d/lighttpd restart
    #每一小时整点重启apache
    * 23-7/1 * * * /usr/local/etc/rc.d/lighttpd restart
    #晚上11点到早上7点之间，每隔一小时重启apache
    * 0/10 23-6 * * ?
    0 21-23,0-8 * * *
    0 11 4 * mon-fri /usr/local/etc/rc.d/lighttpd restart
    #每月的4号与每周一到周三的11点重启apache
    0 4 1 jan * /usr/local/etc/rc.d/lighttpd restart
    #一月一号的4点重启apache

```

## /etc/hosts 
    DNS 域名 -> ip 最前优先
/etc/resolv.conf
/etc/hosts
/etc/hostname #Debian
dns寻址顺序 本机hosts dns 网络dns
hosts 文件的格式为 IP地址 主机名/域名/多个域名
127.0.0.1 localhost localdomain zhanglei
sudo vim /etc/hosts
sudo /etc/init.d/networking restart
## lsof --help 系统 文件还原 进程
···bash
  lsof(list open files)是一个列出当前系统打开文件的工具。在linux环境下，任何事物都以文件的形式存在，
    通过文件不仅仅可以访问常规数据，还可以访问网络连接和硬件。
    所以如传输控制协议 (TCP) 和用户数据报协议 (UDP) 套接字等，系统在后台都为该应用程序分配了一个文件描述符，
    无论这个文件的本质如何，该文件描述符为应用程序与基础操作系统之间的交互提供了通用接口。
    因为应用程序打开文件的描述符列表提供了大量关于这个应用程序本身的信息，因此通过lsof工具能够查看这个列表对系统监测以及排错将是很有帮助的。
    /proc/1917  某进程动id下的 内存文件配置 还原文件？
    [1]+  已停止              ./pipe_maker.sh
    1.找到目标文件使用进程pid 7570 该文件动文件描述符 255r
    lsof | grep pipe_maker
    pipe_make 7570                walker  255r      REG                8,6      2522      17692 /home/walker/e/help_note/shell/pipe_maker.sh
    2.查看该进程文件列表
    ll /proc/7570/fd
    lrwx------ 1 walker walker 64 1月  24 15:36 1000 -> '/home/walker/e/help_note/shell/make.7570.fifo (deleted)'
    lrwx------ 1 walker walker 64 1月  24 15:36 2 -> /dev/pts/0
    lr-x------ 1 walker walker 64 1月  24 15:36 255 -> /home/walker/e/help_note/shell/pipe_maker.sh* (deleted)
    3.读取 转储目标文件
    cat /proc/7570/fd/255 > pipe_maker.sh
    lsof输出各列信息的意义如下：
    COMMAND：进程的名称 PID：进程标识符
    USER：进程所有者
    FD：文件描述符，应用程序通过文件描述符识别该文件。如cwd、txt等 TYPE：文件类型，如DIR、REG等
    DEVICE：指定磁盘的名称
    SIZE：文件的大小
    NODE：索引节点（文件在磁盘上的标识）
    NAME：打开文件的确切名称
    FD 列中的文件描述符cwd 值表示应用程序的当前工作目录，这是该应用程序启动的目录，除非它本身对这个目录进行更改,txt 类型的文件是程序代码，如应用程序二文件本身或共享库，如上列表中显示的 /sbin/init 程序。
    lsof abc.txt #显示开启文件abc.txt的进程
    lsof -c abc #显示abc进程现在打开的文件
    lsof -p 1234 #列出进程号为1234的进程所打开的文件
    lsof -g gid #显示归属gid的进程情况
    lsof +d /usr/local/ #显示目录下被进程开启的文件
    lsof +D /usr/local/ E同上，但是会搜索目录下的目录，时间较长
    lsof -d 4 #显示使用fd为4的进程
    lsof -i #show port tcp
    lsof -i[46] [protocol][@hostname|hostaddr][:service|port]  46 --> IPv4 or IPv6  protocol --> TCP or UDP  hostname --> Internet host name  hostaddr --> IPv4地址  service --> /etc/service中的 service name (可以不止一个)  port --> 端口号 (可以不止一个)
    lsof -i:8091 端口
	
```
## ulimit --help
```bash
ulimit -a [options] [limit]
具体的options参数含义如下表所示：
-a 显示当前系统所有的limit资源信息。
-H 设置硬资源限制，一旦设置不能增加。
-S 设置软资源限制，设置后可以增加，但是不能超过硬资源设置。
-c 最大的core文件的大小，以 blocks 为单位。
-f 进程可以创建文件的最大值，以blocks 为单位.
-d 进程最大的数据段的大小，以Kbytes 为单位。
-m 最大内存大小，以Kbytes为单位。
-n 查看进程可以打开的最大文件描述符的数量。
-s 线程栈大小，以Kbytes为单位。
-p 管道缓冲区的大小，以Kbytes 为单位。
-u 用户最大可用的进程数。
-v 进程最大可用的虚拟内存，以Kbytes 为单位。
-t 最大CPU占用时间，以秒为单位。
-l 最大可加锁内存大小，以Kbytes 为单位。
##最大设备数限制 too many open files 异常
1.查看当前进程设备数 最大限制    查看系统限制最大设备数 每个进程限制
    #系统文件数总数
    cat /proc/sys/fs/file-nr    #总数1
    cat /etc/security/limits.conf
    ulimit -a
    已打开        总限制file-max
    1184 0 6815744
    #进程限制数 suse出现进程限制和ulimit不一致问题?
    cat /proc/${pid}/limits
    #查询规则进程的文件占用数 分组统计
    #方式a
    ps -elf | grep java | grep -v grep | awk '{print $4}' | xargs -I {} lsof -p {} | awk '{print $1,$2}' | uniq -c | grep -v 'COMMAND PID'
    #方式b
    lsof -n | awk '{print $1,$2}' | uniq -c | sort -k 1 -r 
    #lsof -p不准确？？
    #系统的fd使用情况 而ulimit的配置是针对单用户？ 分组排序前十
    #方式c  依赖管理员用户  !!
    sudo find /proc -print | grep -P '/proc/\d+/fd/'| wc -l #总数2
    sudo find /proc -print | grep -P '/proc/\d+/fd/'| awk -F '/' '{print $3}' | uniq -c | sort -rn | head
        a  exe  pid    b  c   
        66 java 1903
        505 java 2147      218
        168 java 2621      80
        395 java 3257      204
        549 java 3361      356
        216 java 3877      .
        1903                4401
3.修改系统最大进程数 最大设备数
    vim /etc/sysctl.conf
        fs.file-max = 1000000
        net.ipv4.ip_conntrack_max = 1000000
        net.ipv4.netfilter.ip_conntrack_max = 1000000
2.优化代码 修改限制
    永久修改
    vim /etc/security/limits.conf
    # 添加如下的行
    * soft nofile 60000
    * hard nofile 61000
    以下是说明：
    * 代表针对所有用户
    noproc 是代表最大进程数
    nofile 是代表最大文件打开数
    添加格式：
    username|@groupname type resource limit
    username|@groupname：设置需要被限制的用户名，组名前面加@和用户名区别。也可以用通配符*来做所有用户的限制。
    type：有 soft，hard 和 -，soft 指的是当前系统生效的设置值。hard 表明系统中所能设定的最大值。soft 的限制不能比har 限制高。用 - 就表明同时设置了 soft 和 hard 的值。
    resource：
    core - 限制内核文件的大小(kb)
    date - 最大数据大小(kb)
    fsize - 最大文件大小(kb)
    memlock - 最大锁定内存地址空间(kb)
    nofile - 打开文件的最大数目
    rss - 最大持久设置大小(kb)
    stack - 最大栈大小(kb)
    cpu - 以分钟为单位的最多 CPU 时间
    noproc - 进程的最大数目
    as - 地址空间限制
    maxlogins - 此用户允许登录的最大数目
```

## 文件夹 限额 挂载
```bash
dd if=/dev/zero ibs=10M count=512 of=/root/disk.img
说明:
if=/dev/zero：表示输入文件为/dev/zero，一个虚拟的设备，顾名思义，里边的数据全是0
ibs=10M： 表示每次读取的块大小为10M,这个数值的大小跟内存有关，如果你要每次读1G的数据
count=512：表示共读取1024块  512 * 10M = 5120M = 5GB
of=/dfs2：输出文件
losetup /dev/loop0 /root/disk.img  #挂载镜像
mkfs.ext3 /dev/loop0    #格式化
mkdir /test
mount -t ext3 /dev/loop0 /test  #文件夹挂载绑定镜像限额
umount /test    #卸载文件夹
losetup -d /dev/loop0  #卸载镜像
rm -f /root/disk.img    #删除镜像
dirname='test10MB'  #文件名
loop='/dev/loop20'  #loop id
imgfile="/${dirname}"  #镜像放置位置
sudo dd if=/dev/zero ibs=10M count=1 of=${imgfile}  #新建镜像
sudo losetup ${loop} ${imgfile}  #挂载镜像
sudo mkfs.ext3 ${loop}    #格式化文件
mkdir ${dirname}
sudo mount -t ext3 ${loop} ${dirname}


## 挂载磁盘为虚拟路径
mount /dev/sda6 /home/e
    fdisk -l    #磁盘
    df -h                          # 查看已经挂载的磁盘
    mkfs.ext4 /dev/vdb            # 初始化磁盘
    mount /dev/vdb /u01            # mount 磁盘到/u01，保证/u01为空
    blkid                          # 获取磁盘的uuid和属性，用uuid来进行开机mount
    vim /etc/fstab                # 开机mount，模板是UUID=********** /home/u01  ntfs  defaults  1 1
    mkfs.ext4 /dev/vdb  #初始化磁盘 格式化？ 
    unmount /dev/vdb #扩容 取消挂载 重新处理 后 再挂载
    e2fsck -f /dev/vdb  # 诊治数据磁盘，返回磁盘信息
    resize2fs /dev/vdb  # 重置数据磁盘大小
```

## 防火墙问题 

debian:
vim /etc/sysconfig/iptables #防火墙表
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 80 -j ACCEPT
-A RH-Firewall-1-INPUT -m state --state NEW -m tcp -p tcp --dport 22 -j ACCEPT
chkconfig iptables off/on #永久生效
service iptables stop/start #重启失效
centos:
/sbin/iptables -I INPUT -p tcp --dport 9332 -j ACCEPT 
/etc/rc.d/init.d/iptables save
/etc/init.d/iptables restart
/etc/init.d/iptables status 

## 启动项
```bash
    1.操作系统接管硬件以后，首先读入 /boot 目录下的内核文件
    2.内核文件加载以后 /sbin/init pid=1
    注意如果脚本需要用到网络，则NN需设置一个比较大的数字，如99。
    sudo update-rc.d test defaults 95 #优先级配置
## 总启动项 在 /etc/init.d文件夹下是全部的服务程序，将脚本复制或者软连接到/etc/init.d/目录下，
ls /etc/init.d
####各级别启动目录 软连接 init.d目录下的应用 每个rc(1-6).d只链接它自己启动需要的相应的服务程序！
ls /etc/ | grep rc
rc0.d # 0 - 停机（千万别把initdefault设置为0，否则系统永远无法启动）
rc1.d # 1 - 单用户模式
rc2.d # 2 - 多用户，没有 NFS
rc3.d # 3 - 完全多用户模式(标准的运行级)
rc4.d # 4 - 系统保留的
rc5.d # 5 - X11 （x window)
rc6.d # 6 - 重新启动
rcS.d
## 每个级别都会在在对应的目录下有对应的启动文件
    ls /etc/rc3.d/
    初始化操作都在 /etc/init/*.conf文件中完成    */
    cat /etc/init/anacron.conf
    start on runlevel [2345]
    stop on runlevel [!2345]
    #####启动1
    vim /etc/rc.local
    /etc/init.d/test.sh start
    #####启动2
    cp test.sh /etc/profile.d/
    #####启动3
    cp test.sh /etc/init.d/
    ln -s /etc/init.d/test.sh /etc/rc3.d/init.d/
    vim 启动文件，文件前面务必添加如下三行代码，否侧会提示chkconfig不支持
    #!/bin/sh #告诉系统使用的shell,所以的shell脚本都是这样
    #chkconfig: 35 20 80 #分别代表运行级别，启动优先权，关闭优先权，此行代码必须
    #description: http server #（ 两行都注释掉！！！，此行代码必须
    chkconfig --add test.sh
```
---

#### 用户组

```
cat /etc/passwd # 查看user home 命令sh环境
chown -R wasup:wasgrp com # 修改文件所属用户及组权限
chmod 755 files # rw-的值为4+2=6 wxr-xr-x的值为755
groupadd mysql # 用户组
groupdel mysql # 删除组
useradd/usermod # 用户新增 修改
    -r # system count
    -s /bin/bash /sbin/nologin /bin/ksh # 登录sh
    -g mysql mysql	# 用户组
    -d /home/z  # home
    -l walker walkerdust # 用户名

passwd walker # 修改密码
userdel walker # 删除用户
su - # 拥有/ .bash_profile .bashrc文件
su 拥有当前用户环境

```

## 目录 home

```
/bin # 普通用户cmd
/dev # system设备 驱动
/home # user home
/lost-found # 系统非正常关机 无家可归 的文件
/misc # 特殊字符定义
/net # 网络相关的文件
/proc # 用户与内核的交互信息
/sbin # sys cmd
/srv # 系统启动服务时数据库
/tmp # 临时文件 重启清空
/var # 大文件的溢出区:日志
/boot # linux启动文件
/etc # sys conf
/lib # sys lib
/media # 可移除的设备:软盘 光盘
/mnt #  挂载临时安装文件
/opt #  源码软件安装位置
/root # 超级用户home
/sys # 管理设备文件
/usr # 最大的目录 应用程序和文件

find /usr/lib/x86_64-linux-gnu/ -name *perl*so*

```

---

## 安装ubuntu后操作记录
修改apt源
修改环境变量添加ls -lth
    alias ll='ls -alFh' 
    英文版本
    安装中文输入法
    apt install ibus-pinyin
    设置系统为中文展示
    language 配置 input source chinese - pinyin 拖动汉语before english
    配置自动挂载磁盘 结合修改help_note目录git同步
    安装python git
    gedit插件安装 编辑器
    sudo apt-get install gedit-plugins
    点击应用关闭
    gsettings set org.gnome.shell.extensions.dash-to-dock click-action 'minimize'
    底座下靠
    chrome
    eclipse
    jdk
    tomcat resin
maven
idea

# apt-get --help debian 源配置
```bash
cat /proc/version
vim /etc/apt/sources.list                                               
# for pi
deb http://mirrors.aliyun.com/raspbian/raspbian/ stretch main contrib non-free rpi
# for pc
对比原有配置 找到系统版本
XXXX='focal'
deb http://mirrors.aliyun.com/ubuntu/ ${XXXXX} main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ ${XXXXX}-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ ${XXXXX}-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ ${XXXXX}-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ ${XXXXX}-backports main restricted universe multiverse 

apt autoremove #自动删除无依赖包
apt-get update  #更新源
apt-get upgrade #更新已安装的包
apt-get dist-upgrade 更新已安装的包 and auto dependcy
apt-get install python<=2.7> <--reinstall> 安装包
apt-get remove package 删除包
apt-get remove package --purge 删除包，包括配置文件等
apt-cache search package 搜索软件包
apt-cache show package  获取包的相关信息，如说明、大小、版本等
apt-get -f install  修复安装
apt-get -f -y install  ???
apt-get build-dep package 安装相关的编译环境
apt-cache depends package 了解使用该包依赖那些包
apt-cache rdepends package 查看该包被哪些包依赖
apt-get source package  下载该包的源代码
apt-get clean && apt-get autoclean 清理无用的包
apt-get check 检查是否有损坏的依赖
# 指定版本安装 
apt-cache policy <<package>>
列出所有来源的版本 已安装版本
apt-cache madison vim
  vim | 2:7.3.547-1 | http://debian.mirrors.tds.net/debian/ unstable/main amd64 Packages
  vim | 2:7.3.547-1 | http://debian.mirrors.tds.net/debian/ unstable/main Sources
apt-get install <<package name>>=<<version>>
apt-get install open-client=1:6.6p1-2ubuntu1
```

# nmon --help 性能监控 分析工具 监控 cpu mem netstat
```bash
apt-get install nmon
nmon -fT -s 5 -c 20
nmon -f -T -s 5 -c 20 -m  ~/logs/
    -f 以后台方式运行nmon,把收集到的数据保存到csv文件中
    -t 包含top的输出
    -T 输出最耗资源的进程
    -s 间隔时间
    -c 收集多少次
    -m 生成目录

nmon_analyser.xls excel脚本宏
https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Power%20Systems/page/nmon_analyser
选择文件转换为excel格式
excel图表展示

```

# nginx搭建 rtmp模块 pcre openssl zlib
```bash
http://blog.csdn.net/shuxiaogd/article/details/47662115
wget http://nginx.org/download/nginx-1.8.0.tar.gz
wget https://codeload.github.com/arut/nginx-rtmp-module/zip/master #master.zip
wget ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.39.tar.gz
wget http://www.openssl.org/source/openssl-1.0.1c.tar.gz
wget http://www.zlib.net/zlib-1.2.11.tar.gz

cd nginx-1.10.1
./configure --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-pcre=../pcre-8.39 --with-zlib=../zlib-1.2.11 --with-openssl=../openssl-1.0.1c --with-http_stub_status_module --add-module=../nginx-rtmp-module-master

./configure --sbin-path=/usr/local/nginx/nginx --conf-path=/usr/local/nginx/nginx.conf --pid-path=/usr/local/nginx/nginx.pid --with-http_ssl_module --with-pcre=../pcre-8.39 --with-zlib=../zlib-1.2.11  --with-md5=/root --with-http_ssl_module --with-openssl=../openssl-1.0.1c --add-module=../nginx-rtmp-module-master

make
make install
```
# haproxy socket 代理搭建
```bash
    wget http://www.haproxy.org/
    tar -xzvf haproxy-1.7.8.tar.gz
    cd  haproxy-1.7.8
    make TARGET=linux26 #cat /proc/version
    make install PREFIX=/usr/local/haproxy
    kill启动后
    ./usr/local/haproxy/sbin/haproxy -f /usr/local/haproxy/conf/haproxy.cnf
    # 监控
    listen  admin_stats
        bind 0.0.0.0:8888
        mode  http
        stats uri  /haproxy
        stats realm    Global\ statistics
        stats auth  admin:admin
    # 监控是否代理目标宕机
    listen test1
            bind 0.0.0.0:3306
            mode tcp
            #maxconn 4086
            #log 127.0.0.1 local0 debug
            server s1 192.168.111.101:3306 check port 3306
            server s2 192.168.111.102:3306 check port 3306
    http://192.168.111.100:8888/haproxy
```

# 编译安装ffmpeg
```bash
http://ffmpeg.org/releases/ffmpeg-2.8.11.tar.gz
wget -c http://ffmpeg.org/releases/ffmpeg-3.0.tar.bz2
tar xvf ffmpeg-3.0.tar.bz2
cd ffmpeg-3.0
./configure --host-cppflags=-fPIC --host-cflags=-fPIC --enable-shared
make
make install
```


# openssl安装
版本不能太高，太高有些接口与libRTMP 的接口不一样，会导致libRTMP编译不能通过 
```bash
wget http://www.openssl.org/source/openssl-1.0.1f

tar -xvf openssl-1.0.1f.tar.gz
cd openssl-1.0.1f
./config --prefix=/usr/local/openssl
./config -t
make depend
cd /usr/local
ln -s openssl ssl
make install
vim /etc/ld.so.conf 
     /usr/local/openssl/lib
ldconfig
vim /etc/profile
    export OPENSSL=/usr/local/openssl/bin
    export PATH=$OPENSSL:$PATH:$HOME/bin
source /etc/profile
# 验证
cd /usr/local
ldd /usr/local/openssl/bin/openssl
    linux-vdso.so.1 =>  (0x00007fff2116a000)
    libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007f378e239000)
    libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f378de7c000)
    /lib64/ld-linux-x86-64.so.2 (0x00007f378e44f000)

openssl version
    OpenSSL 1.0.1f 6 Jan 2014  
```

