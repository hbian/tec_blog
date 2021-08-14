## Install
jenkins stable LTS war file
http://mirrors.jenkins.io/war-stable/2.176.4/
Jenkins有几种安装方式，docker, rpm, war,选用war的方式进行安装
更方便进行配置
```
useradd jenkins -g jenkins

#Jenkins 启动脚本
#!/bin/bash
java -Dcom.sun.akuma.Daemon=daemonized -Djava.awt.headless=true -DJENKINS_HOME=/data/jenkins -jar /data/jenkins/jenkins.war --logfile=/data/jenkins/log/jenkins.log --webroot=/data/jenkins/cache/war --daemon --httpPort=8080 --debug=5 --handlerCountMax=100 --handlerCountMaxIdle=20


```