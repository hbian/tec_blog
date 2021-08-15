## Disable NetworkManager
踩坑，
在centos7中如果修改了dns配置/etc/resolve.conf 之前没有disable NetworkManager 会导致配置在重启后被还原，所以配置vm时一定要Disable NetworkManager。
原因是Centos7的网络配置服务已经替换成NetworkManager， 在centos6中不需要disbale

## Http_proxy in /etc/bash_profile
踩坑，服务器上的服务访问一个地址例如http://www.test.com/ping, 但使用wget或者curl测试总是返回访问到一个固定ip例如10.72.11.100 8088而且访问失败， 检查过/etc/resolve.conf并不是dns的配置问题，后来发现是在/etc/bash_profile中配置了http_proxy, 导致所有http请求都到了10.72.11.100 8088。 由于该服务上转发服务down了，所以导致访问失败。切记，注意不要随意设置全局的http_proxy, 这样很容易增加问题排查难度 


## 进程管理调试相关
### Kill
Kill -1 pid 可以用来重载进程

### LSOF
lsof -p pid 查看进程打开的文件
lsof -p pid|grep tcp 查看进程的tcp连接信息
lsof file_path 查看文件被哪些进程使用
lsof -i port 查看端口使用信息

### strace
strace -p pid 进程的系统调用