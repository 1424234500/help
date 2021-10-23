
#!/bin/bash  
## 
about="
用于 svn 增量打包和部署  \n
Ctrl the xxx tools.    \n
Usage: \n   
eg: \n 
  ./help_svn.sh package 301 389  'D:/workspace/walker' 'D:/doc/walker'	\n 
"

lastModuleFile="/ttt.txt"
lastModule=`cat ${lastModuleFile}`
_now=` date "+%Y%m%d-%H%M%S" `
 
 
defLocalProjectDefPath='D:\workspace\walker' 
defMakePackagePath='D:\make' 
defDeployPath='/home/walker/tomcat/webapps' 
defBackDir='/home/walker/package' 
defSh='/home/walker/tomcat/bin/startup.sh'


#打包
function package(){  
	paramsDef=( '132002' '132543' "${defLocalProjectDefPath}" "${defMakePackagePath}" ' ' ) 
	for ((i=0; $# > 0; i++)) ; do  
		item=${1} 
		paramsDef[${i}]=${item}  
		echo "param.${i}: '${item}' " 
		shift 1 
	done 
	versionFrom=${paramsDef[0]} 
	versionTo=${paramsDef[1]}  
	dirProjectInput=${paramsDef[2]} 
	dirMakeInput=${paramsDef[3]} 
	dirMakeInput=${dirMakeInput//\\/\/}
	MODE_FILE=${paramsDef[4]} #指定svn差异文件列表 用于无版本号svn
	MODE_FILE=${MODE_FILE//\\/\/}   
	out "versionFrom: ${versionFrom}, versionTo: ${versionTo}, dirProjectInput: ${dirProjectInput}, MODE_FILE:${MODE_FILE}"
  
	dirProject=${dirProjectInput//\\/\/}  
	out "dirProject: ${dirProject}"
	[ ! -d "${dirProject}" ] && out "dirProject: ${dirProject} is not directory error " && help
	
	#相对路径
	doShell "cd ${dirProject}"

	#模块名
	moduleName=` ls -F ${dirProject}/target | grep '/$' | grep -v '-' | awk -F'/' '{print $1}'  `
	out "moduleName: ${moduleName}" 

	[ -z "${moduleName}" ] && out "parse moduleName: ${moduleName}  error "  && help

	packageName=
	if [ -f "${MODE_FILE}" ]; then 
		toolsLine 
		out "is from MODE_FILE '${MODE_FILE}'"
		[ ! -z "`tail ${MODE_FILE} -n 1`" ] && ( out '!! filelist not end with //n add ! ' ; echo "" >> ${MODE_FILE} )
		
		packageName=package_filelist_`ls -alF --time-style="+%Y%m%d_%H%M%S" "${MODE_FILE}" | awk '{print $6}' ` #指定文件 修改时间
	else
		packageName=package_svn_${versionFrom}_${versionTo} 
	fi
	dirMake=${dirMakeInput}/${packageName} 

	out "dirMake: ${dirMake}" 
	[ ! -d "${dirMake}" ] 	&& ( echo "dirMake: ${dirMake} is not directory, now mkdir "  ) 
	
	dirMakeWebinf=${dirMake}/${moduleName}/WEB-INF	#/d/make /walker/ WEB-INF
	dirMakeBack=${dirMake}_source/${moduleName} 
	
	dirTempFile=${dirMake}_source/svndiff.txt
	dirFileList=${dirMake}/filelist.txt
	
	out "dirMakeWebinf: ${dirMakeWebinf}"  
	[ ! -d "${dirMakeWebinf}" ] && mkdir -p ${dirMakeWebinf}  
	[ ! -d "${dirMakeBack}" ] && mkdir -p ${dirMakeBack}  
	
	dirClass=target/${moduleName}/WEB-INF/classes	#target/walker/WEB-INF/classes
	toolsLine
	out "webinf dir: ${dirProject}/target/${moduleName}/WEB-INF"
	[ ! -d "${dirProject}/target/${moduleName}/WEB-INF" ] 	&& ( echo "webinf dir: ${dirProject}/target/${moduleName}/WEB-INF is not directory, NO BUILD ??? "; help  )
	ls -alFht ${dirProject}/target/${moduleName}/WEB-INF
	toolsLine
	out "class dir: ${dirProject}/${dirClass}"
	[ ! -d "${dirProject}/${dirClass}" ] 	&& ( echo "class dir: ${dirProject}/${dirClass} is not directory, NO BUILD ??? "; help  )
	ls -alFht ${dirProject}/${dirClass}
	toolsLine 
	rmfile ${dirTempFile}
	rmfile ${dirFileList}  
	if [ -f "${MODE_FILE}" ]; then
		dirTempFile=${MODE_FILE}
		cat ${dirTempFile}
		out
		toolsLine 
	else 
		out "svn diff --summarize -r ${versionFrom}:${versionTo} | sed -r 's%\\%\/%g' | sed -r 's%  +% %g' | cut -c 2-9999    "
		svn diff --summarize -r ${versionFrom}:${versionTo} | awk '{print NR,$0}'
		toolsLine
		svn diff --summarize -r ${versionFrom}:${versionTo} | sed -r 's%\\%\/%g' | sed -r 's%  +% %g' | cut -c 2-9999 | xargs -I {} echo "{}" >  ${dirTempFile} 
	fi 
	
	while read line;
	do
		#echo ${line}
		[ -z "${line}" ] && continue;
		fileFrom=""
		fileTo=""
		type=""
		
		t=${dirMakeBack}/${line}
		[ ! -d ${t%/*} ] && ( mkdir -p ${t%/*} )
		cp ${line} ${dirMakeBack}/${line} 
		if [[ "$line" =~ src\/main\/java.*.java ]]; then
			type=class 
			fileFrom=`echo ${line} | sed -r s%src\\/main\\/java%target\\/${moduleName}\\/WEB-INF\\/classes%g | sed -r s%\.java%.class%g `  
			fileTo=${dirMakeWebinf}/`echo ${line} | sed -r s%src\\/main\\/java%classes%g  | sed -r s%\.java%.class%g ` 
			cpclass ${fileFrom} ${fileTo} ${type}
		elif [[ "$line" =~ src\/main\/resources\/.* ]]; then
			type=res
			fileFrom=`echo ${line} | sed -r s%src\\/main\\/resources/target\\/${moduleName}\\/WEB-INF\\%classes%g ` 
			fileTo=${dirMakeWebinf}/`echo ${line} | sed -r s%src\\/main\\/resources%classes%g ` 
			cpfile ${fileFrom} ${fileTo}  ${type}
		else
			echo "other??? ${line}"
		fi  
		
	done < ${dirTempFile}
	toolsLine
	echo "svn files"
	toolsLine
	cat ${dirTempFile} | awk '{print NR,$0}'
	toolsLine
	echo "version package files"
	toolsLine
	cat ${dirFileList} | awk '{print NR,$0}'
	toolsLine
	echo ${moduleName} > ${lastModuleFile}
	
	waittime 3 'tar the package to gz package_svn_${versionFrom}_${versionTo}.tar.gz '
	#package_svn_1_3.tar.gz.before.tar.gz 
	cd ${dirMakeInput}/${packageName}
	doShell "tar -czf ../${packageName}.tar.gz  * "	#路径 问题 是否包含版本目录 
  
	outWarn "package ok at   ${dirMakeInput}/${packageName}.tar.gz  " 
	return 0
}