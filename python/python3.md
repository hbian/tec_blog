## Python3 && Pipenv
https://blog.csdn.net/zongzhengyingzhe/article/details/84568352

```
sudo yum -y groupinstall development

yum install https://mirrors.tuna.tsinghua.edu.cn/ius/ius-release-el7.rpm -y

yum install python36u-pip -y

yum install python3-devel 

pip3.6 install pipenv  -i https://pypi.tuna.tsinghua.edu.cn/simple 

```


```
mkdir project
cd project
pipenv install
```

初始化好虚拟环境后，会在项目目录下生成2个文件Pipfile和Pipfile.lock。为pipenv包的配置文件，代替原来的 requirement.txt。
将pipenv源替换为阿里云
```
sed -i 's|pypi.org|mirrors.aliyun.com/pypi|g' Pipfile
```
激活虚拟环境： pipenv shell