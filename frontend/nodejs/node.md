### Node && NPM Installation
Node安装较为简单，基本下载以后配置相应的系统路径即可直接使用
```
wget https://nodejs.org/dist/v8.9.1/node-v8.9.1-linux-x64.tar.gz
tar xzvf node-v8.9.1-linux-x64.tar.gz
ln -s /data/softs/node-v8.9.1-linux-x64/bin/node  /usr/local/sbin/
ln -s /data/softs/node-v8.9.1-linux-x64/bin/npm  /usr/local/sbin
```


### NPM 
npm install -g 安转模块全局可用，否则只会是安装在当前项目的node_modules
目录下。

一个node package有两种依赖，一种是dependencies，一种是devDependencies，其中前者依赖的项该是正常运行该包时所需要的依赖项，而后者则是开发的时候需要的依赖项，像一些进行单元测试之类的包。
其实应该还有一种不常见的依赖optionalDependencies，表示可选依赖项，即使安装失败也不会导致项目运行失败的依赖项！！
默认会安装两种依赖，如果你只是单纯的使用这个包而不需要进行一些改动测试之类的，可以使用:npm install --production
如果npm install安装项目所以依赖时候，不想安装optionalDependencies中的可选依赖项，则可以使用以下命令：npm install --no-optional

查看已安装的top level的模块
```
npm ls --depth 0
```

###npm root
如果使用root调用npm的时候，npm会将uid修改成user account或者是在npm的config文件中找到user config然后用此时的user修改uid，如果这些值都没有，user的默认值是nobody.你可以通过设置--unsafe-perm=true使用root权限运行npm script命令.
当你使用root调用npm，只有在running package lifecycle script，npm才会将uid设置成nobody。对于其他的script，npm不会强制设置你的uid
果使用root执行npm install， 当你安装postinstall一个package，npm还会是用当前这个权限去运行这个package中的postinstall, 因此如果脚本中写了一些不利于操作系统的脚本，会直接broke你的电脑。

当你使用root执行npm install的时候，npm为了安全性考虑，将你的uid设置成nobody, nobody权限非常的低，因此postinstall里写的很多脚本nobody都没有权限执行，因此不会造成安全问题

虽然npm可以自动的帮助你在执行lifecycle script的时候降低权限到nobody, 但是如果你自己希望npm不要强制修改你的uid，你可以使用npm install --unsafe-perm



### package-lock.json

While the package.json file lists dependencies that tell us the suitable versions that should be installed for the project, the package-lock.json file keeps track of all changes in package.json or node_modules and tells us the exact version of the package installed. You usually commit this to your version controlled repository instead of node_modules, as it’s a cleaner representation of all your dependencies.

npm will check for a package-lock.json file to install the modules. If no lock file is available, it would read from the package.json file to determine the installations. It is usually quicker to install from package-lock.json, since the lock file contains the exact version of modules and their dependencies, meaning npm does not have to spend time figuring out a suitable version to install.