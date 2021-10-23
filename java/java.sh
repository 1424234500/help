# JDK才有的 分析工具  jre不可用!!!	 ibm jdk有差异 
#jps | grep -v 'jps' | awk '{print $1}'
pid=$1  
[ -z "${pid}" ] &&  echo 'eg: ./make.sh ${pid} ' && exit 1 

#采集java进程pid和command	jps 
####################采集脚本#######
 
ti=`date "+%Y%m%d-%H%M%S"`    #时间戳
key=$pid.$ti        #命名键
file=~/logs         #存储根路径
file_tcp_top=$file/$key.tcp_top.log
file_cpu_thread=$file/$key.ps.cpu_thread.log
file_mem_thread=$file/$key.ps.mem_thread.log
file_jstack=$file/$key.jstack.javacore	 
file_jmap=$file/$key.jmap_dump.hprof	 

#采集linux最消耗cpu/mem的进程/线程 command
ps H -eo user,pid,ppid,tid,time,%cpu,%mem --sort=%cpu  | awk '{printf "0x%x\t %s\n", $4, $0}'  > $file_cpu_thread 
ps H -eo user,pid,ppid,tid,time,%cpu,%mem --sort=%mem  | awk '{printf "0x%x\t %s\n", $4, $0}'  > $file_mem_thread  
#采集top 存在ps查不到 而top查到的情况
top -Hp $pid > ${file_tcp_top}
#采集端口信息
netstat -anolp >> ${file_tcp_top}	
#采集java线程栈 	javacore	IBM jre kill -3
jstack -l $pid > $file_jstack     
#采集java堆快照	headdump	jmap	已包含javacore	
jmap -dump:format=b,live,file=$file_jmap $pid      

	
#新一代抓取shell 依赖环境jcmd
##抓取所有java进程pid 拿到每个pid的jvm参数  gc信息 
lineOrDiffOrNo=$2	# 2 baseline 1 diff 3 baseline&summary ? summary
echo "############ ${2}. now "`jps | grep ${pid}`" type ${lineOrDiffOrNo} "`date "+%Y%m%d-%H%M%S"`" #################"  
jcmd ${pid} VM.command_line | grep  'jvm_args'  			#看jvm启动参数
top -p ${pid}  -b -n 1 | grep "${pid}\|COMMAND" 			#看res进程内存总占用
jcmd ${pid} GC.heap_info scale=MB | grep -v ${pid}  		#看堆内信息和元空间
if [[ "${lineOrDiffOrNo}" == "1" ]];then   
	echo 'summary.diff'
	jcmd ${pid} VM.native_memory summary.diff scale=MB | grep -v ${pid} 	#变化过于小 看不到差异 
elif [[ "${lineOrDiffOrNo}" == "2" ]];then   
	echo 'baseline&summary'
	jcmd ${pid} VM.native_memory baseline scale=MB | grep -v ${pid} 	#开启基线快照  
	jcmd ${pid} VM.native_memory summary scale=MB | grep -v ${pid}   	#同时summary
else 
	echo 'summary'
	jcmd ${pid} VM.native_memory summary scale=MB | grep -v ${pid}  
fi


