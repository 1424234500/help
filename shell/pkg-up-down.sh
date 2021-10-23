
function upload(){
	sshuser=root@xxx		#scp -p *.gz root@xxx:/opt/upload/
	if [ ! -z $1 ];then
		sshuser=$1 
	else 
		echo '$1 is null'" default sshuser now: ${sshuser}" 
		line 
	fi
	
	#上传
	scp -p ${upgzfile} ${sshuser}:${dirUploadGz}/
	
 
}
#上传升级包 && 升级脚本
#部署目标路径 升级包名字（默认扫描脚本目录） 升级包所在路径（默认脚本目录） 
function upgrade(){
	local paramsDef=( ""  "${defDeployPath}" "${defBackDir}") 
	for ((i=0; $# > 0; i++)) ; do  
		item=${1} 
		paramsDef[${i}]=${item}  
		out "param.${i}: '${item}' " 
		shift 1 
	done    
	local dirProject=${paramsDef[1]} #部署路径
	local dirBack=${paramsDef[2]}	#备份路径
	[ ! -d "${dirBack}" ] && mkdir -p ${dirBack}   
	local fromPackageGz=${paramsDef[0]}	#指定升级包名
	local dateStr=`date "+%Y%m%d_%H%M%S" `
	
	if [ -z "${fromPackageGz}" ] ; then  
		fromPackageGz=`getGzName ${dirBack} ` 
	fi   

	if [ -z "${fromPackageGz}" ] ; then 
		out "no package gz && scan no ok package error  ${dirBack}"
		ls -alFth ${dirBack}
		return 2
	fi 
	
	local gzfilePathBefore=${dirBack}/${fromPackageGz}.before.tar.gz
 	if [ -f "${gzfilePathBefore}" ]; then 
		waittime 3 "have upgrade ${fromPackageGz} and back at ${gzfilePathBefore} then to downgrade 已经升级过该版本包 现在先还原"
		downgrade "${fromPackageGz}"  "${dirProject}" "${dirBack}" 
	else
		waittime 3 "back 备份"
		tar -czf ${gzfilePathBefore} ${dirProject}
		if (( $?==0 )); then
			outWarn "
			back ok (before upgrade) at   ${gzfilePathBefore}    备份 成功   \n
			downupgrade cmd 参考还原指令 ./help_svn.sh downgrade \"${fromPackageGz}\"  \"${dirProject}\" \"${dirBack}\"   
			"	  
		else
			out "tar -czf ${gzfilePathBefore} ${dirProject}   back error $? 备份 失败  " 
			return 3
		fi  
	fi 
	waittime 3 "upgrade 升级" 
	tar -xzvf ${fromPackageGz} -C ${dirProject}/  
	if (( $?==0 )); then
		out "upgrade ok ${fromPackageGz}   升级 成功"	  
	else
		out "tar -xzvf ${fromPackageGz} -C ${dirProject}/  error $? 升级 失败  " 
		return 4
	fi  

	restart
	log
    return 0
}

#降级 某before 备份版本
function downgrade(){
	local paramsDef=( ""  "${defDeployPath}" "${defBackDir}") 
	for ((i=0; $# > 0; i++)) ; do  
		item=${1} 
		paramsDef[${i}]=${item}  
		out "param.${i}: '${item}' " 
		shift 1 
	done    
	local dirProject=${paramsDef[1]} #部署路径
	local dirBack=${paramsDef[2]}	#备份路径
	[ ! -d "${dirBack}" ] && mkdir -p ${dirBack}   
	local fromPackageGz=${paramsDef[0]}	#指定升级包名 
	local dateStr=`date "+%Y%m%d_%H%M%S" `
	
	if [ -z "${fromPackageGz}" ] ; then 
		fromPackageGz=`getGzName ${dirBack} ` 
	fi 
	if [ -z "${fromPackageGz}" ] ; then 
		out "no package gz && scan no ok package error  ${dirBack}"
		ls -alFth ${dirBack}
		return 1
	fi 
	fromPackageGzBefore=${fromPackageGz}
	[[ "${fromPackageGzBefore}" == *.before.tar.gz ]] || fromPackageGzBefore="${fromPackageGzBefore}.before.tar.gz" 
	# 是否需要完全还原  rm old dir
	if [ ! -f "${dirBack}/${fromPackageGzBefore}" ]; then 
		out "back before gz not exists 未曾备份和升级 无法还原 ${dirBack}/${fromPackageGzBefore} 未还原 "
		return 2
	fi
	tar -xzf ${dirBack}/${fromPackageGzBefore} -C / 
	if (( $?==0 )); then
		out "tar -xzf ${dirBack}/${fromPackageGzBefore} -C /   downgrade ok $? 还原 成功 "
	else
		out "tar -xzf ${dirBack}/${fromPackageGzBefore} -C /   downgrade error $? 还原 失败  " 
		return 3
	fi 
	
}

#根据序号、简称名字 获取对应安装包 
#gzName=`getGzName ${dirBack}`
function getGzName(){
	local lastDir=`pwd -LP`
	local dirBack=$1
	cd ${dirBack}
	ls -t *tar.gz 2>/dev/null | grep -v '.*.before.tar.gz$' | head -n 1
	cd ${lastDir}
}

source template.sh
