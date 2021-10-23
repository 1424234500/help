#!/bin/bash  
########################################### 
#./xxx <help> 
# 
###########################################

about="
Ctrl the xxx tools.    \n
Usage: 
./xxx.sh [ start   | stop | help ] [other args]   \n 
    \t  start   \t  start server with log/system.log    \n
    \t  stop    \t  stop server kill pid    \n
    \t  restart \t  stop & start    \n
    \t  log \t  tailf log/*.log \n
    \t  pid \t  ps -elf | grep server   \n
    \t  help    \t  show this   \n
eg: \n
	\t	./xxx.sh  start all d:/cph/hello	\n

"


function argsDef(){  
	local params=('args0' 'args1' 'args2' 'args3' 'a4' 'a5')   
	for ((i=0; $# > 0; i++)) ; do  
		item=${1} 
		params[${i}]=${item}  
		out "param.${i}: '${item}' "  
		shift 1 
	done    
	for ((i=0; i<${#params[@]}; i++)) ; do  
		item=${params[${i}]} 
		out "param.${i}: '${item}' "  
		echo ${item}
	done    
	[ -z "" ] && out " error "  && help #简单提示并中断sh 

} 

function help(){
    toolsLine
    echo -e $about
    toolsLine 
	exit $1
	toolsLine

} 
function out(){
    echo -e `date "+%Y-%m-%d %H:%M:%S" `' '$@
}
function outArr(){
	local arr=($@)
	out "arr.size=${#arr[@]}"
	for ((i=0; i<${#arr[@]}; i++))  # !!! 序号依次
	do
	  item=${arr[$i]} 
	  out "item.${i}: ${item} "
	done   
}
# do the cmd and show cmd
# do "echo asdf"
function doShell(){
    out $*
    eval $*
}
# start a function or a system call nohup &
# call "echo aasdb"
function call(){
    local tools_out='nohup '$*' & '
    out $tools_out
    eval $tools_out
} 
#Show the split line such as '-----------'
#toolsLine <10>
function toolsLine(){
    local split='-'
	  [ -n "$2" ] && split="$2"
    local str=''
    local len=$1
    [ -Z "$len"] && len=16
    for ((tools_i=0; tools_i<$len; tools_i++)); do
        str=$str""$split
    done

    out $str
}  
function outline(){
	toolsLine $@
}
function outWarn(){
	outline 16
	outline 8 '#'
	out $@
	outline 8 '#'
	outline 16
}
#倒计时3秒
#waittime 3
function waittime(){
	local params=('2' )   
	for ((i=0; $# > 0; i++)) ; do  
		item=${1} 
		params[${i}]=${item}  
		#echo "param.${i}: '${item}' "  
		shift 1 
	done    
	outline
	out "timer begin wait ${params[0]} seconds then to ${params[1]}"
	for ((i=${params[0]}; i > 0; i--)); do 
		out "${i}..."
		sleep 1
	done
	out "timer end wait ${params[0]} seconds"
	outline

}

#class拷贝 内部类问题！！！
function cpclass(){
	local fileFrom=$1
	local fileTo=$2
	local type=$3
	#fileFrom='target/b/WEB-INF/classes/comx.class' 
	#fileFrom='target/b/WEB-INF/classes/cx.class' 
	#fileTo='D:/make/WEB-INF/classes/cx.class'
	#x.class
	#x$2.class 
	#拷贝文件
	cpfile ${fileFrom}   ${fileTo}  ${type} 
	ls -l ${fileFrom%.*}\$*.class 2>/dev/null |  awk '{print $9}' | (while read line;do 
		cpfile ${line} ${fileTo%/*}/   class-I   
	done) 
} 
#文件拷贝 判断异常 记录到日志文件
# cpfile ../test.txt ./test.txt 'classes'
function cpfile(){
	local fileFrom=$1
	local fileTo=$2

	local type=$3
	local fileToShow=${fileTo:${#dirMake} }
	local fileToDir=${fileTo%/*}
	[ ! -d ${fileToDir} ] && ( out "mkdir ${fileToDir}" ; mkdir -p ${fileToDir}  )  
	
	out "${type}\t cp ${fileFrom} \t${fileTo}"  
	if [ ! -f ${fileFrom} ];then 
		out "Error file not exists !!!!! ${fileFrom} ${fileTo} "
		out "${fileToShow} \t Error file not exists !!!!! " >> ${dirFileList}
		return
	fi 
	cp ${fileFrom} ${fileTo}
}
function rmfile(){
	[ -d $1 ] && ( doShell "rm -r '$1'")
	[ -f $1 ] && ( doShell "rm  '$1'")
}
# get a file from files
function getdirEg(){
	local dirs=('/log' '.')
	local filename='test.txt'
	for item in ${dirs[@]}; do [ -f "${item}/${filename}" ] && echo ${item} && return; done
}
function getfileEg(){
	local files=('/log/test.txt' './test.txt')
	for item in ${files[@]}; do [ -f "${item}" ] && echo ${item} && return; done
}


# 控制开机启动
# bootup name /xx/xx.sh true (start stop restart)
function bootup(){
    local serviceName=$1
    local shUrl=$2
    local enable=$3

    is7=`cat /etc/issue | grep -i 'CentOS.*7\.[0-9]\+' `
    if [ ! -z "${is7}" ]; then
#centos 7
      echo "make auto start boot ${is7}"
      systemd_dir='/usr/lib/systemd/system'
      [ ! -d ${systemd_dir} ] && ( mkdir -p ${systemd_dir} ;  echo "mkdir ${systemd_dir}" )
      if [ -f ${systemd_dir}/${serviceName}.service ]; then
        doShell "systemctl disable ${serviceName}.service"
        doShell "rm ${systemd_dir}/${serviceName}.service"
      fi
      doShell "systemctl daemon-reload"

      echo "[Unit]
Description=${serviceName}
After=network-online.target remote-fs.target nss-lookup.target
Wants=network-online.target

[Service]
Type=forking
ExecStart=${shUrl} start
ExecReload=${shUrl} restart
ExecStop=${shUrl} stop
KillMode=none

[Install]
WantedBy=multi-user.target
" > ${systemd_dir}/${serviceName}.service

      if [[ "${enable}" == "true" ]]; then
        doShell "systemctl enable ${serviceName}.service"
        doShell "systemctl status ${serviceName}.service"
      else
        echo 'no start'
      fi

    else
#centos 6
      echo "make auto start boot not centos7 " `cat /etc/issue`
      if [ -f "/etc/init.d/${serviceName}" ]; then
        doShell "chkconfig  ${serviceName} off"
        doShell "rm /etc/init.d/${serviceName}"
      fi
      echo "#!/bin/bash
#chkconfig: 2345 80 40
#description: ${serviceName}
${shUrl} start
" > ${shUrl}.chkconfig.start.sh
      doShell "ln -s ${shUrl}.chkconfig.start.sh  /etc/init.d/${serviceName}"
      if [[ "${enable}" == "true" ]]; then
        doShell "chkconfig --add ${serviceName}"
        doShell "chkconfig  ${serviceName} on"
      else
        echo 'no start'
      fi
    fi

    echo 'make auto start over '
    return 0
}










#多进程并发
function threadTest() {
  threadBefore 4
  for (( i=0; i < 20; i++)); do
    read -u1000 readStr #管道阻塞消费信号
    {
      out "get Source: "$readStr
      sleep 4
      echo `date "+%Y-%m-%d %H:%M:%S"` >&1000 #还原信号
    } &
  done
  threadAfter
}
function threadBefore() {
  # 线程数
  local params=('4'   )
  for ((i=0; $# > 0; i++)) ; do
    item=${1}
    params[${i}]=${item}
    shift 1
  done
  local tempfifo='make.'$$'.fifo'
  # exec 1000>&-; 关闭绑定 >写 <读
  trap "exec 1000>&-;  exec 1000<&-;exit 0" 2 #捕获中断
  mkfifo -m 0644 ${tempfifo} # 创建管道
  exec 1000<>${tempfifo}
  rm -rf $tempfifo

# 预热信号数
  for ((i=1; i<=${params[0]}; i++)); do
    echo `date "+%Y-%m-%d %H:%M:%S"` >&1000
  done


}
function threadAfter(){
  wait
  exec 1000>&-;  exec 1000<&-; #解绑
}

# 定时多次执行指令
function timer() {
               #指令    间隔时间s 次数
  local params=('date' '1'      '3' )
  for ((i=0; $# > 0; i++)) ; do
    item=${1}
    params[${i}]=${item}
    shift 1
  done

  for ((i=0; i<${params[2]}; i++)); do
    echo "----------------"
    echo "timer at "`date "+%Y-%m-%d %H:%M:%S" `" now $i/${params[2]} sleep ${params[1]} run ! "
    ${params[0]}
    sleep ${params[1]}
  done
}

#确认退出机制 信号
function onCtrlC() {
  read -p "ctrl c exit? (Y/N): " input
  if [[ ${input} == "Y" || ${input} == "y" ]] ; then
      exit
  fi
}
# 函数启动入口 传递参数 context设置
# ./he.sh methodName methodArgs01 methodArgs02 ...
trap -l #所有信号列表
#SIGINT        2      中断 CTRL+C
#SIGQUIT       3      杀死
#SIGKILL       9      强制杀死进程 不可trap!
#SIGTSTP      20      挂起 CTRL+Z
trap "onCtrlC" SIGQUIT #3 ctrl + c


method=$1
out ">>cmd   : "$@
out ">>shAt  : "$(cd `dirname $0`; pwd -LP)
out ">>args  : "'size:$#='"$#"
out ">>method: ${method}"
params=()	# (${rootParams[@]:1})  #重构数组空格问题 1 - n
childArgs=" "
echo "param.0: \"${0}\" "
echo "param.1: \"${1}\" "
for ((i=2; $# > 1; i++)) ; do
	item=${2}
	params[${i}]=${item}
	echo "param.${i}: '${item}' "
	childArgs="${childArgs} '${item}' "	#"包含 避免空格 
	shift 1	#移位遍历 因为无法 ${${i}} ($#)减一，而变量值提前一位
done    

echo ">>method params.size: ${#params[@]}"  
echo ">>method cmd: ${method} ${childArgs}" 

toolsLine
if [ -n "$method" ]; then 
   # $method ${params[@]} #重构数组空格问题
   # str=""; for i in `seq 0 32`; do str="$str \"\$${i}\""; done ; echo ${str} 
	eval ${method} ${childArgs}	#二次解析? 
else
  help
fi 
 