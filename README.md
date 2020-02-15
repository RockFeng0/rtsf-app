# rtsf-app
基于rtsf测试框架，关键字驱动Android UI,进行自动化的功能测试

1. 基本的使用，参见rtsf项目的 使用入门
2. rtsf-app遵循在rtsf项目高阶用法的约定
3. rtsf-app也就只做了3件事情
    - 设计APP UI自动化测试yaml用例，并重写Runner.run_test的执行规则
    - 封装常用的Appium方法，为用例提供yaml函数
    - 封装grid模式，支持命令行实现分布式部署
   
[查看rtsf项目用法](https://github.com/RockFeng0/rtsf)

# 环境准备

## window安装 appium.js
1. [下载安装node.js](https://nodejs.org/en)
2. 管理员权限，执行命令，安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
3. 管理员权限，执行命令，安装appium: cnpm install appium -g
4. 安装完成后，验证appium: appium.cmd --command-timeout 120000 -p 4723 -U DEVICE_ID

> appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U DEVICE_ID

命令启动，appium-server实例：
![appium-cmd.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/appium-cmd.png)

## 设置ANDROID_HOME环境变量
1. [下载simple_android_home](https://github.com/RockFeng0/rtsf-app/releases/tag/v1.0.39)
2. 解压文件android_home.zip，新增环境变量 ANDROID_HOME，为解压后的根目录的路径
3. 在环境变量path中，追加 %ANDROID_HOME%\platform-tools

> 如果你安装了  android SDK，并设置了 ANDROID_HOME, 确保 adb 和 aapt命令可以被调用

rtsf-app依赖的两个命令，如图：
![android-tools.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/android-tools.png)

## 下载selenium-server-standalone.jar

> 参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)项目，环境准备栏，给出的下载链接

## 安装rtsf-app
pip install rtsf-app 

# 命令介绍

安装完成后，有两个命令用于执行yaml测试用例: 
- aldriver命令，android localhost driver，一般情况下，都是用这个命令执行yaml用例
- ardriver命令，android remote driver， 分布式部署的grid模式下，使用该命令运行yaml用例，它可以指定任意hub中的所有node机器，并在所有这些机器上运行用例。

安装完成后，有两个部署appium服务的命令：
- wrhub命令，开启grid hub，具体参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)
- appserver命令，用于非grid模式下，启动appium server；在grid模式下，用于启动appium node

安装完成后，有一个工具命令：
- ainfo命令， 用于查看PC连接的android设备信息，以及查看待测试apk的报信息

## ainfo
1. 查看设备信息，其中注意关注， device_id 和  android_version(android device platform version)

格式为dict -> {device_id: {...}, device_id: {...}, 。。。} 
 
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

ainfo命令实例：
![ainfo-cmd.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/ainfo-cmd.png)

## wrhub
如果有，并行的测试需求，我们会用到Grid模式，wrhub开启一个grid hub，允许不同测试node节点的接入

具体参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)

## appserver

1. appserver提供简单的命令，为每一个待测试的手机，绑定一个端口，通过该端口，我们的测试用例，可以准确下发测试任务
2. appserver在绑定手机的同时，可以作为grid node接入grid模式

查看帮助: appserver -h
必填:
- 设置绑定设备监听的地址及端口：          e.g. 192.168.1.1:4723

选填：
- 设置绑定设备的device_id:         --device-name DEVICE_NAME
- 设置绑定设备的android_version:   --device-version DEVICE_VERSION
- grid模式，连接的hub iP:         --hub-ip HUB_IP
- grid模式，连接的hub port:       --hub-port HUB_PORT

appserver命令参数
![appserver-h.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/appserver-h.png)

## aldriver
1. aldriver命令执行本地测试，该命令主动连接本地的4723端口，并驱动adb连接的第一个设备进行测试

查看帮助: aldriver -h

选填：
- 指定测试apk的本地路径，该参数会给手机重装app:        --apk APK
- 手机已装app，指定测试app的package名字:          --package PACKAGE
- 手机已装app，指定测试app的activity名字:         --activity ACTIVITY

aldriver命令参数:

![aldriver-h.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/aldriver-h.png)

## ardriver
1. ardriver命令执行grid模式下，远程并行测试

注意:
- aldriver 与 ardriver的区别就在于: ardriver支持 ip和port参数，允许grid模式
- 在使用grid模式的时候， 如果使用 --apk参数，那么 确保该grid hub下的node手机,在该指定的文件路径中，存在这个apk。
- 在使用grid模式的时候，如果使用 --package和--activity参数，那么确保，连接到hub的node的手机，已经装了这个apk

ardriver命令参数:

![ardriver-h.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/ardriver-h.png)

# rtsf-app的约定

依据rtsf的yaml约定模板，我们在steps中，为rtsf-app约定了一个规则，以便识别为Android UI自动化测试， 如下

```
steps:
    - appdriver:
        by: 
        value:
        index:
        timeout:
        action:
    - appdriver:
        action:
    ...
```
> action必填，其他选填
NativeApp的话，支持：("id","xpath","class name",'-android uiautomator')，
WebView的话，支持selenium所用方式

# rtsf-app常用的yaml函数

<!-- 注释， 不建议 使用 SetControl定位元素

###  AppElement methods -- 元素定位相关操作

<table>
    <tr>
        <th>AppElement methods</th>
        <th>参数介绍</th>
        <th>描述</th>
    </tr>
    <tr>
        <td>GetControl()</td>
        <td> </td>
        <td>获取element controls,返回字典，如：{"by":None,"value":None,"index":0,"timeout":10}</td>
    </tr>
    <tr>
        <td rowspan="4">SetControl(by,value,index,timeout)</td>
        <td>by: 指appium的寻找元素的方式:NativeApp支持("id","xpath","class name",'-android uiautomator')，WebView支持selenium所用方式，默认为None</td>
        <td rowspan="4">
                    1.依据app当前context，设置element controls，用于app元素的定位和控制<br/>
                    2. -android uiautomator是appium使用uiautomator中的UiSelector来定位元素，常用来使用文本定位元素，value值如 text("xxxx")
        </td>
    </tr>
    <tr>
        <td>value: 与by配对使用，相应by的值</td>
    </tr>
    <tr>
        <td>index: 索引值，默认为0，即第一个， 如果by,value组合找到很多元素，通过索引index指定一个</td>
    </tr>
    <tr>
       <td>timeout: 超时时间，默认10，即10秒，如果by,value组合寻找元素超过10秒，超时报错</td>
   </tr>    
</table>

-->


## App functions --> android设备-测试相关常用操作

```
LaunchApp()                                     # use current session to launch and active the app        
StartActivity(app_package,app_activity,timeout) # Only support android.  start an activity and focus to it. default timeout is 10 seconds
PageSource()                                    # page source for this activity
Forward()                                       # 类似浏览器的 前进
Back()                                          # 类似浏览器的 后退
Shake()                                         # 模拟设备摇晃 
BackgroundApp(seconds)                          # 应用会被放到后台特定时间,然后应用会重新回到前台 
OpenNotifications()                             # 打开通知栏
RemoveApp(app_package)                          # 卸载app
SwitchToDefaultContext()                        # 切换到默认上下文 
SwitchToNewContext()                            # 切换到新的上下文
Reset()                                         # 重置app, 即先closeApp然后在launchAPP
CloseApp()                                      # only close app . keep the session
QuitApp()                                       # will close the session
```

## AppContext methods --> 用于上下文管理
```
DyAttrData(name,attr)                       # -> 属性-动态存储变量，适用于，保存UI元素属性值。name-变量名称，attr为UI元素的属性名称，**配合SetControl使用**
DyActivityData(name)                        # -> 使用变量,保存当前app activity name
DyPackageData(name)                         # -> 使用变量,保存当前app package name
DyStrData(name, regx, index)                # -> 字符串-动态存储变量，适用于，保存页面html中指定的值。 name-变量名称，regx已编译的正则表达式，index指定索引，默认0


GetVar(name)                                # -> 获取指定变量的值
SetVar(name,value)                          # -> 设置指定变量的值
```

## AppWait methods --> 用于时间的控制
```
TimeSleep(seconds)                   # -> 指定等待时间(秒钟)
WaitForAppearing()                   # -> 等待元素出现(可能是隐藏，不可见的)，**配合SetControl使用**
WaitForDisappearing()                # -> 等待元素消失，**配合SetControl使用**
WaitForVisible()                     # -> 等待元素可见，**配合SetControl使用**
```
        
## AppVerify methods --> 用于验证
```
VerifyVar(name, expect_value)                # -> 验证变量值，是期望的expect_value，返回True，否则返回False
VerifyAppInstalled(app_package)              # -> 验证app package name已经安装
VerifyCurrentActivity(app_activity)          # -> 验证当前app activity name是期望的app_activity
VerifyText(text)                             # -> 验证元素text属性值，为期望的text,**配合SetControl使用**
VerifyElemEnabled()                          # -> 验证元素是enabled，**配合SetControl使用**
VerifyElemNotEnabled()                       # -> 验证元素是Not Enabled, **配合SetControl使用**
VerifyElemVisible()                          # -> 验证元素是可见的， **配合SetControl使用**
VerifyElemNotVisible()                       # -> 验证元素是不可见的，**配合SetControl使用**
VerifyElemAttr(attr_name,expect_value)       # -> 验证元素属性attr_name的值，包含值expect_value,**配合SetControl使用**
VerifyElemCounts(num)                        # -> 验证元素数量为num,**配合SetControl使用**
```

## AppTouchAction methods --> 用于Android触摸操作
```
Tap()                        # -> 在指定元素上，轻触点击 1次，**配合SetControl使用**
LongPress()                  # -> 在指定元素上，长按，**配合SetControl使用**
Press()                      # -> 在指定元素上，按住不释放，**配合SetControl使用**
MoveTo()                     # -> 移动到指定元素上，**配合SetControl使用**
Release()                    # -> 在指定元素上，释放按住的操作，**配合SetControl使用**
Draw()                       # -> 在当前activity中，画画
Swipe(direction, times)      # -> 在当前activity中，滑动.direction滑动方向: up, down, left, right; times滑动次数，默认1次
```

## AppActions methods --> 用于Android常规操作
```
Pinch()                      # -> 在指定元素上缩小，**配合SetControl使用**
Zoom()                       # -> 在指定元素上放大，**配合SetControl使用**
SendKeys(value)              # -> 在指定元素上,输入文本值，**配合SetControl使用**, 继承自selenium，可用于WebView
click()                      # -> 在指定元素上，点击左键一次，**配合SetControl使用**, 继承自selenium,可用于WebView
```

> AppTouchAction和AppActions，封装较少的原因是考虑到Appium继承了selenium,因此有些appium提供的方法中,并不会同时兼容NativeApp和WebviewApp，同时，[rtsf-web](https://github.com/RockFeng0/rtsf-web)项目已经支持了selenium对web ui的测试。

# 自定义，yaml函数和变量

在case同级目录中，创建 preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用， 具体参见rtsf的介绍

# 数据驱动与分层用例

在[rtsf](https://github.com/RockFeng0/rtsf)项目中，已经有了详细的介绍，rtsf-web也适用

# 场景实例

依据rtsf和rtsf-app的约定， 做了几个app ui测试的示例

## 简单实例

1. 编写一个yaml文件

```
# test_case.yaml
- project:
    name: ApiDemos项目
    module: 简单实例
    
- case:    
    name: android_app_ui_auto_test_demo_1
    
    glob_regx:
        rex_bar_title: 'Views/Controls/(.*)'
    
    glob_var:
        app_package: io.appium.android.apis
        app_main_activity: .ApiDemos
        app_view_webview_activity: .view.WebView1
        app_view_button_activity: .view.Buttons1
        app_view_control_activity: .view.Controls1
        app_view_dragdrop_activity: .view.DragAndDropDemo
        app_graphic_paint_activity: .graphics.TouchPaint
        app_animation_activity: .animation.BouncingBalls
        
    pre_command:
        - ${StartActivity($app_package, $app_view_control_activity)}
        - ${DyStrData(var_bar_title, $rex_bar_title)}
        - ${VerifyVar(var_bar_title, 1. Light Theme)}  
        
    steps:      
    
        - appdriver:
            by: id
            value: io.appium.android.apis:id/edit
            index: 0
            timeout: 10
            action: ${SendKeys(你好  -  hello)}
            
        - appdriver:
            action: ${TimeSleep(1)}
        
        - appdriver:
            by: -android uiautomator
            value: text("Checkbox 1")
            index: 0
            timeout: 10
            action: ${Tap()}
                        
        - appdriver:
            action: ${VerifyElemAttr(checked, true)}
        
        - appdriver:
            action: ${Tap()}
            
        - appdriver:
            action: ${VerifyElemAttr(checked, false)}
        
        - appdriver:
            action: ${TimeSleep(1)} 
        
        - appdriver:
            action: ${Swipe(up, 1)}
                
        - appdriver:
            by: id
            value: android:id/text1            
            action: ${Tap()} 
            
        - appdriver:
            by: -android uiautomator
            value: 'text("Earth")'
            action: ${Tap()}
                           
    post_command:
        - ${Back()}
        - ${CloseApp()}
```

2. 执行这个文件

```
# Terminal 1 监听本机4723端口
appserver 192.168.1.200:4723 

# Terminal 2 本地执行该用例
aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk
```
[下载ApiDemos-debug.apk](https://github.com/RockFeng0/rtsf-app/releases/tag/v1.0.0)

## 详细实例 

### 场景一  本地测试

一般情况下，就是一台PC，连接一台设备的测试场景，步骤如下

1.测试场景假设

```
 apk(待测试的apk): C:\ApiDemos-debug.apk
 case(自动化测试用例): C:\test_case.yaml

 PC_A_IP(本机): 192.168.1.1
 PC_A_Android_Device_ID(天天模拟器): 127.0.0.1:6555
```

2.开启appium server,并绑定待测设备

```
# PC_A监听4723端口，绑定名字是127.0.0.1:6555并且版本为4.4.4的移动设备
# 注意，监听端口+1也会被占用
appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4
```

3.aldriver驱动测试


**aldriver命令执行本地测试，该命令主动连接本地PC_A的4723端口，并驱动adb连接的第一个设备进行测试, 这就是为什么，在假设场景中，PC_A使用本机IP和4723端口**

```
# --apk参数会在移动设备中重装
aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk
```

**你不想重装apk。通过ainfo获取到 appPackage和appActivity,执行下述命令**

```
# 原理相当于appium中的，start_activity(package, activity)
aldriver C:\test_case.yaml --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos
```

**当然，你可以补全所有参数**

```
aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos
```


4.释放端口占用

> ctrl + c 结束端口占用

场景一实例:
![scene-1.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/scene-1.png)

## 场景二 远程控制测试-Selenium Grid Mode

1.测试背景及分析

```
背景: 
    比如，手上有1000条相对独立的测试case，一台PC一台设备的方式完成这些case的验证，效率较低。那么，并行测试是最好的解决办法

分析: 
    1.多台PC连接多台设备的测试场景假设,其原理是基于selenium RC，使用selenium Grid的方式，使得appium server作为node节点，进行分布式测试
    2.可是，即使是分布式测试，它的过程也是一个并发的过程，每台设备分别都要测试1000条case。好比很多车在支路上跑，汇入的主干道却只有一条
    3.需要做的，就是让这1000条case，分配给这些设备，让它们并行测试。解决方法：多重hub
```

多台PC,连接多台设备,并行测试case场景，步骤如下

2.测试场景假设

```
 apk(待测试的apk): C:\ApiDemos-debug.apk
 case1(自动化测试用例): C:\test_case1.yaml
 case2(自动化测试用例): C:\test_case2.yaml
 ...

 PC_Server_IP(Grid Hub端): 192.168.1.254

 PC_A_IP(本机): 192.168.1.1
 PC_A_Android_Device_ID(天天模拟器): 127.0.0.1:6555
 ...

 PC_B_IP(远端机): 192.168.1.2
 PC_B_Android_Device_ID(天天模拟器): 127.0.0.1:6555
 ...

注意: adb.exe最多支持每台pc链接20台设备
并行测试: PC_A连接的所有机器，测试case1;PC_B连接的所有机器,测试case2
```

一个图，三种情况，理解分布式:
![grid-hub.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/grid-hub.png)

3.开启selenium grid hub

命令详解，参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)

```
# PC_Server设置PC_A的hub
wrhub C:\selenium-server-standalone-3.14.0.jar --port 4444

# PC_Server设置PC_B的hub
wrhub C:\selenium-server-standalone-3.14.0.jar --port 5555
```

4.开启appium server node

```
# PC_A  4723端口绑定设备，并注册node节点 
appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 4444

# PC_A  4725端口绑定设备，并注册node节点 
appserver 192.168.1.1:4725 --device-name DEVICE_ID --device-version DEVICE_VERSION --hub-ip 192.168.1.254 --hub-port 4444
...

# PC_B, 同理
appserver 192.168.1.2:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 5555
...
```

4.ardriver驱动测试

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

# 获取控件的工具
1. 如果是WebviewApp项目，工具推荐，就参考rtsf-web项目
2. 如果是NativeApp项目，您需要安装Android SDK, tools目录下，两个工具可以用于定位app元素:
    - uiautomatorviewer
    - hierarchyviewer

暂时没有 找到轻量好用的，用于定位的工具，如果您知道，请赐教
