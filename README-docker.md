## docker
多服务器节点自动批量化安装、启停、监控工具

#### 结构
镜像 Image = class? 安装包
仓库 Repository = mvn 管理 Image 各个安装包版本管理
容器 Container = instance? Image 实例 
主机 Host 控制中心 控制所有节点
客户端 Client 每一台节点上 安装客户端

#### 环境

```powershell
wget https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker walker # 非root用户添加docker组

# sudo apt-get purge docker-ce #卸载
# sudo rm -rf /var/lib/docker #清理文件
```

#### 使用

##### 仓库管理
中心仓库 
https://hub.docker.com/
可注册个人账号管理自己的镜像 stars

```
docker login/logout
```

##### 管理镜像
```powershell
docker --help
docker search ubuntu  # 搜索镜像 
docker pull/push ubuntu  # 手动下载上传镜像 
# 新建镜像
vi Dockefile
	FROM nginx # 基线
	ARG NAME=hello VERSION=1.0 # 上下文变量 参数
	ENV JAVA_HOME=/home/java7 # 目标容器环境变量
	VOLUME /home/walker/nginx # 数据卷 默认匿名卷 容器重启丢失? 避免容器扩大
	EXPOSE 6379 6389 # 声明端口
	WORKDIR /home/walker/workdir # 工作目录 须提前建好 每一个 RUN 指令 每一层镜像都存在
	USER walker:usergrp # 指定用户组 须已存在
	HEALTHCHECK NONE # 屏蔽基线的健康检查

	RUN echo 'h' > ${JAVA_HOME}/hello.txt && echo 'w' > /${NAME}/test.txt # 每次指令都会封装一层 镜像膨胀 减少行数!!!
	#所有指令均支持两种写法
	RUN ['echo', 'hello'] # build 阶段执行
	COPY --chown=walker:rootgrp /home/root/* /home/walker/	
	ADD # 同 COPY 自动解压!
	
	ONBUILD echo 'from this onbuild' # 同 RUN 被依赖基线 from 时 build 时执行

	ENTRYPOINT ["nginx", "-c"] # 定参 类似 CMD 但不会被 命令参数覆盖
	CMD ["/etc/nginx/nginx.conf"]  # 变参 同 RUN run 阶段执行 只最后一行生效!!! 一般变参使用
	# 不传参数时 docker run nginx:test  			     => nginx -c /etc/nginx/nginx.conf
	#   传参数时 docker run nginx:test -c hello.conf  => nginx -c hello.conf
	
docker build -t nginx:v2 . # 将本路径一起打包上传

# 容器快照提交镜像
docker commit  ${id} ${name}:v2
	-m="my new dk" # commit 描述信息
	-a="walker" # autho 作者
	test/ubuntu:v2 # 镜像目标位置 ${tag}
	
docker images ls #本地镜像清单
docker tag ${id} # 标签 命名

# 管理网络 域名?命名空间 容器互联
docker network create -d bridge test-net 
			   -d bridge / overlay 网络模型
docker network ls # 网络列表
#宿主机配置所有容器统一dns
cat /etc/docker/daemon.json
	{
		"dns":["114.114.114.114"]
	}

# 实例化镜像 创建容器
docker run ubuntu:15.10 /bin/echo "Hello world"
	run # (安装)启动 容器
	-i # 开启交互 输入 输出 
	-t #交互终端模式
	-d # 后台模式 返回 id ctrl+z?
	-P # 随机映射高端口主机?
	-p 127.0.0.1:5000:5000/tcp # 指定ip端口映射
	-v /home/walker/ubu # 指定卷 挂载点 VOLUMN
	--rm # 退出容器时 自动清理文件系统
	--hostname=HOSTNAME # 主机名 /etc/hosts  /etc/hostname
	--name ubuntu1510  # 命名
	--build-arg NAME=name # ARG 上下文变量替换
	--dns=114.114.114.114  # 指定 dns
	--network test-net # 加入网络 bash 中 可 ping ${tag} 即可 ping 通
	ubuntu：15.10 # 镜像 ${tag} : 版本
	/bin/echo "Hello world" # 容器中执行指令
```
##### 管理容器
```powershell
docker ps -a  # = ps jobs
	-l last 最后一次创建的容器
	status 状态 created restarting running/up paused exited dead 

docker start ${id}/${name}  
	start/stop/restart
	port # 端口映射查看
	inspect # 容器信息详情
	logs -f  # tail -f 跟踪标准输出 stdout
	attach # 前台容器 fg? 退出即关闭
	exec -it ${id} /bin/bash  # 前台容器 临时接管 不能关闭
	export ${id} > ubuntu15.tar  # 导出快照
cat ubuntu15.tar | docker import - test/ubuntu:v1  # 导入快照
docker import http://xxxx/xxx example/imgerepo
docker container prune  # 清理终止状态的容器

```

##### 项目环境 多容器配置依赖 YML 工具 Docker Compose 
##### 集群环境 海量服务器管理 Docker Machine
多服务器批量操作
启动、检查、停止、重启、托管、升级(docker)
```shell

docker-machine create --driver virtualbox test #创建
	
docker-machine ${action} ${name}
	ls
	ip
	stop/start/restart/upgrade/rm/kill/env
	inspect #详情
	ssh/scp

```