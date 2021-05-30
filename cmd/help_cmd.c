#
#	bat 编程
#
cmd路径 \ 反斜杠 linux
1.start b.bat 新开cmd窗口 
2.call b.bat 不显示 路径执行  命令/bat 等待后续
3.b.bat 直接调用exe终止 当前bat后续代码 而 call不会
::top grep
tasklist /v | findstr Simulator
::端口 不要 p 
netstat -ano | findstr  111
::进入脚本所在目录
cd /d %~dp0

cmd路径 \ 反斜杠 linux
1.start b.bat 新开cmd窗口 
2.call b.bat 不显示 路径执行  命令/bat 等待后续
3.b.bat 直接调用exe终止 当前bat后续代码 而 call不会

::不展示cmd窗口启动
set ws=WScript.CreateObject("WScript.Shell") 
ws.Run "D:\cph\note\help_note\cmd\niuniu\NiuniuCapture.exe niuniu,d:\nn.png,0,0,0,0,0,0",0

%1% 取出第一个参数

字符串替换
@echo off REM 字符串替换 set str=待替换文本信息XXX echo 对“%str%”中的“XXX”进行替换，替换为“YYY” REM 替换str中的XXX为YYY set str2=%str:XXX=YYY% echo - echo 替换后为：%str2% echo - pause
setx path "%path%;D:\webpack sample project\node_modules\.bin" /M 
有的路径中会带有空格,用双引号包裹起来。/M开关表示添加系统变量。
IF /? 帮助文档 命令介绍

分支控制 EQU NEQ LSS LEQ GTR GEQ
IF EXIST FILENAME. （
    del filename.
) ELSE （
    echo filename. missing.
)

for
for  %%I in (ABC) do echo %%I
pause

@echo off
set num=0
:ok
set /a num+=1
echo.test-%num%
if "%num%"=="10" pause&&echo.over！
goto ok

::延迟ping 1s 等待启动间隔
tasklist | find /i "node.exe" && taskkill /f /t /im node.exe  & ping localhost -n 1

tasklist | find /i "node.exe" || start "node" node proxy.js  

copy  复制文件
xcopy /Y /E /F /O D:\c\src D:\d\src\ 
xcopy /Y /E /F /O D:\c\* D:\d\
rd /S /Q "C:\Users\235605\AppData\Local\dahua"  删除文件夹
dir /A /S  "C:\Users\235605" 查看文件夹大小 du -sh
等待耗时sleep
TIMEOUT /T 2

时间
echo "hello" > %date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt


文件搜索grep ?
find /?
    文件目录检索批量 文本关键词
    find /I /N "keys" * 

tasklist | find /i "node.exe" && taskkill /f /t /im node.exe

tasklist | find /i "node.exe" || start "node" node proxy.js 

copy  复制文件
xcopy 复制文件夹

等待耗时sleep
TIMEOUT /T 2


文件搜索grep ?
find /?
    文件目录检索批量 文本关键词
    find /I /N "keys" *



计算机管理
任务计划程序
启动配置
msconfig


//双网卡设置
无线局域网适配器 WLAN 2: 内网
   连接特定的 DNS 后缀 . . . . . . . :
   本地链接 IPv6 地址. . . . . . . . : fe80::dda8:653d:8109:5298%22
192.168.2.90
255.255.255.0
192.168.2.1

无线局域网适配器 WLAN: 外网
   连接特定的 DNS 后缀 . . . . . . . :
   本地链接 IPv6 地址. . . . . . . . : fe80::5156:591e:35a0:92e0%7
192.168.104.235
255.255.255.0
192.168.104.254

//重置ipv4 避免127.0.0.1失效问题
netsh int ip reset
设置内网静态ip 掩码 不要网关！！    dns解析服务器 114.114.114.114 
设置外网自动ip 自动掩码 自动网关
接下来的route应该会有一个0.0.0.0外网路由
// 0.0.0.0          0.0.0.0  192.168.104.254   192.168.104.77     55
// 0.0.0.0          0.0.0.0      192.168.2.1     192.168.2.24     50
配置路由
route delete 0.0.0.0 //设置了网关就得删除默认路由 网关==路由 (-p 永久有效 异常?)  
//配置映射 路由  192.168.2.*->192.168.2.1 内网配置路由
route -p add 192.168.2.0 mask 255.255.255.0 192.168.2.1
route -p add 122.0.0.0 mask 255.0.0.0 192.168.2.1

route delete 192.168.2.0
route delete 122.0.0.0
//最后面 * -> 192.168.104.254 外网  默认配置
route -p add 0.0.0.0 mask 0.0.0.0 192.168.104.254  metric 400


//热点
netsh wlan set hostednetwork mode=allow ssid=dust7.11 key=9012345678
netsh wlan start hostednetwork 

//dns树 本机-hosts  ->  ip配置 dns -> other dns
//域名-ip转换表 
C:\Windows\System32\drivers\etc\hosts
C:\Windows\SysWOW64\drivers\etc\hosts
/etc/hosts
ipconfig /flushdns  //fulush refresh
//ip-mac转换表(!rarp) 该命令显示和修改“地址解析协议 (ARP)”缓存中的项目。ARP 缓存中包含一个或多个表，它们用于存储 IP 地址及其经过解析的以太网或令牌环物理地址。 
arp -a 

ping -a ip  ping -a 将地址解析为计算机名。用户名
nbtstat -a ip 来获得更详细的信息，包括计算机的名称已经硬件Mac地址，这样不论他们怎么变化遁形，都逃不过你的法眼啦，赶紧试试吧。

ping 目标计算机名
nbtstat -a 目标计算机名（可以省去）
////////////////////ip和用户名互转

重置网络连接
netsh int ip reset
netsh winhttp reset proxy
ipconfig /flushdns
重置winsock
netsh winsock reset
1366X768
“开始”--输入“regedit”依次找到：
HKEY_LOCAL_MACHINE/SYSTEM/ControlSet001/Control/GraphicsDrivers/Configuration

然后右键点击Configuration，选择查找，输入Scaling，在右框内即可看到scaling，
右键scaling选择修改，将数值改为3即可。

gpedit.msc
计算机配置"-"windows设置"-"安全设置"
-"软件设置策略",右击"软件设置策略"点"新建策略"-"其它规则"-右击"其它规则"-"新路径规则把你要阻止的某些软件放在一个盘里面就OK了..


　　
dir /?
    dir /N /S /A:-L-S-H-D


cd /home 进入 '/ home' 目录' 
　　cd .. 返回上一级目录 
　　cd ../.. 返回上两级目录 
　　 
 