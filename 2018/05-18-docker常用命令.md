# docker常用命令

- 作者：codehackfox@gmail.com
- 时间：2018-05-18 14:29:58

> ### 0x00、常用命令

* 查看容器重启次数
    * docker inspect -f "{{ .RestartCount }}" container_id
* 查看容器最后一次的启动时间
    * docker inspect -f "{{ .State.StartedAt }}” container_id
* commit一个镜像
    * docker run --name="python_env_l" -it image_name /bin/bash
    * docker commit -m="msg" -a="user_name" 4631e1627784 image_name:2.1
    * docker tag  image_name:2.1 image_name:latest
    * docker push image_name
* Docker构建镜像
    * docker build -t imageName .
* 打标签 
    * Docker tag image user/newName:tag
* 批量删除无用镜像
    * docker image rm `docker images|grep none|awk {'print $3'}`
* 批量删除无用容器
    * sudo docker rm `sudo docker ps -a |grep Exited| awk {'print $1'}`
