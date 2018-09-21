# rtsf-app
基于rtsf测试框架，关键字驱动Android UI,进行自动化的功能测试


# 环境准备

## window安装 appium.js
1. [下载安装node.js](https://nodejs.org/en)
2. 执行命令，安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
3. 执行命令，安装appium: cnpm install appium -g
4. 安装完成后，验证appium: appium.cmd --command-timeout 120000 -p 4723 -U DEVICE_ID

> appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U DEVICE_ID

## 设置ANDROID_HOME环境变量
1. [下载simple_android_home](https://github.com/RockFeng0/rtsf-app/releases/tag/v1.0.39)
2. 解压文件android_home.zip，新增环境变量 ANDROID_HOME，为解压后的根目录的路径
3. 在环境变量path中，追加 %ANDROID_HOME%\platform-tools

> 如果你安装了  android SDK，并设置了 ANDROID_HOME, 确保 adb 和 aapt命令可以被调用

## 安装git 

在安装rtsf-app的时候，一些依赖需要安装，但是这些依赖并未放到pip中，所以临时使用了git安装的方案，安装一下就好。[下载git](https://git-scm.com/downloads/)

## 下载selenium-server-standalone.jar

> 参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)项目，环境准备栏，给出的下载链接

## 安装rtsf-app
python setup.py install
 

# 命令介绍

## 工具命令
1. 查看设备信息, 格式: 设备id:设备属性     ,设备属性中，android_version就是设备版本，即android device platform version

```
# PC中，执行ainfo命令，打印该PC连接的所有设备信息及设备属性
> ainfo
{'127.0.0.1:6555': {'ip': None, 'model': 'SAMSUNG-SM-N900A', 'cpu': 'x86', 'pad_version': 'hlteatt-userdebug 4.4.4 tt eng.jenkins.20171226.140228 release-keys', 'android_version': '4.4.4', 'android_api_version': '19', 'linux_version': 'Linux version 3.10.0+ (ttvm@TianTian-Dev) (gcc version 4.6 20120106 (prerelease) (GCC) ) #13 SMP PREEMPT Mon Dec 18 11:26:12 CST 2017'}}
```

2. 查看apk信息，其中主要关注，appPackage和appActivity 

```
# PC中，执行ainfo --apk APK_FILE 命令，查看apk信息
> ainfo --apk C:\ApiDemos-debug.apk
{'platformName': 'Android', 'deviceName': None, 'platformVersion': None, 'app': 'C:\\d_disk\\auto\\buffer\\test\\tools\\android\\ApiDemos-debug.apk', 'appPackage': 'io.appium.android.apis', 'appWaitPackage': 'io.appium.android.apis', 'appActivity': 'io.appium.android.apis.ApiDemos', 'unicodeKeyboard': True, 'resetKeyboard': True, 'newCommandTimeout': 120000}
```

## 场景一  本地测试

一般情况下，就是一台PC，连接一台设备的测试场景，步骤如下

**测试场景假设**

```
 apk(待测试的apk): C:\ApiDemos-debug.apk
 case(自动化测试用例): C:\test_case.yaml

 PC_A_IP(本机): 192.168.1.1
 PC_A_Android_Device_ID(天天模拟器): 127.0.0.1:6555
```

1. 开启appium server,并绑定待测设备

```
#  PC_A，监听4723端口，该端口绑定  id为127.0.0.1:6555并且版本为4.4.4的设备；注意，监听端口+1也会被占用
> appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4

```

2. aldriver驱动测试

```
# aldriver命令执行本地测试，该命令主动连接本地PC_A的4723端口，并驱动adb连接的第一个设备进行测试
# 这就是为什么，在假设场景中，要求appserver使用PC_A使用本机IP和4723端口，并绑定名字是 127.0.0.1:6555 的设备
> aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk

# 如果，你没有apk,但是通过 工具命令，获取到 appPackage和appActivity，可以使用下述命令；原理相当于appium中的，start_activity(package, activity)
#> aldriver C:\test_case.yaml --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos

# 当然，也可以补全所有参数
#> aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos
```

3. 释放端口占用， ctrl + c 结束端口占用

## 场景二 远程控制测试-Selenium Grid Mode

背景: 比如，手上有1000条相对独立的测试case，一台PC一台设备的方式完成这些case的验证，效率较低。那么，并行测试是最好的解决办法

分析: 
- 多台PC连接多台设备的测试场景假设,其原理是基于selenium RC，使用selenium Grid的方式，使得appium server作为node节点，进行分布式测试
- 可是，即使是分布式测试，它的过程也是一个并发的过程，每台设备分别都要测试1000条case。好比很多车在支路上跑，汇入的主干道却只有一条
- 需要做的，就是让这1000条case，分配给这些设备，让它们并行测试。解决方法：多重hub

**测试场景假设**

- apk(待测试的apk): C:\ApiDemos-debug.apk
- case1(自动化测试用例): C:\test_case1.yaml
- case2(自动化测试用例): C:\test_case2.yaml
- ...

- PC_Server_IP(Grid Hub端): 192.168.1.254

- PC_A_IP(本机): 192.168.1.1
- PC_A_Android_Device_ID(天天模拟器): 127.0.0.1:6555
- ...

- PC_B_IP(远端机): 192.168.1.2
- PC_B_Android_Device_ID(天天模拟器): 127.0.0.1:6555
- ...

并行测试，PC_A连接的所有机器，测试case1;PC_B连接的所有机器,测试case2

注意: adb.exe最多支持每台pc链接20台设备

1. 开启selenium grid hub, 命令详解，参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)

```
# PC_Server设置PC_A的hub
> wrhub C:\selenium-server-standalone-3.14.0.jar --port 4444

# PC_Server设置PC_B的hub
> wrhub C:\selenium-server-standalone-3.14.0.jar --port 5555
```

2. 开启appium server node,并绑定待测设备

```
# PC_A  4723端口绑定设备，并注册node节点 ； 注意，远程控制模式，可以注册多台机器
> appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 4444

# PC_A  4725端口绑定设备，并注册node节点 
> appserver 192.168.1.1:4725 --device-name DEVICE_ID --device-version DEVICE_VERSION --hub-ip 192.168.1.254 --hub-port 4444

...

# PC_B, 同理
> appserver 192.168.1.2:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 5555

...
```

3. ardriver驱动测试

注意:
- 如果使用 --apk参数，那么 确保 PC A 和 PC B,在该指定的文件路径中，存在这个apk。
- 如果使用 --package和--activity参数，那么确保，连接到PC的手机，已经装了这个apk
- aldriver 与 ardriver的区别就在于: ardriver支持 ip和port参数，允许grid模式

```
# ardriver本身是个并发驱动测试，但是，每次使用都会开一个进程，并发的过程，就采用多次执行命令吧
# PC_A执行case1，执行case1的测试验证
> ardriver C:\test_case1.yaml --apk C:\ApiDemos-debug.apk --ip 192.168.1.254 --port 4444

# PC_B的所有设备，执行case2的测试验证
> ardriver C:\test_case2.yaml --apk C:\ApiDemos-debug.apk --ip 192.168.1.254 --port 5555

```



