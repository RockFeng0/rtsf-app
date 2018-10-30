# rtsf-app
基于rtsf测试框架，关键字驱动Android UI,进行自动化的功能测试


# 环境准备

## window安装 appium.js
1. [下载安装node.js](https://nodejs.org/en)
2. 执行命令，安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
3. 执行命令，安装appium: cnpm install appium -g
4. 安装完成后，验证appium: appium.cmd --command-timeout 120000 -p 4723 -U DEVICE_ID

> appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U DEVICE_ID

![appium-cmd.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/appium-cmd.png)

## 设置ANDROID_HOME环境变量
1. [下载simple_android_home](https://github.com/RockFeng0/rtsf-app/releases/tag/v1.0.39)
2. 解压文件android_home.zip，新增环境变量 ANDROID_HOME，为解压后的根目录的路径
3. 在环境变量path中，追加 %ANDROID_HOME%\platform-tools

> 如果你安装了  android SDK，并设置了 ANDROID_HOME, 确保 adb 和 aapt命令可以被调用

![android-tools.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/android-tools.png)

## 下载selenium-server-standalone.jar

> 参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)项目，环境准备栏，给出的下载链接

## 安装rtsf-app
pip install rtsf-app 

# 命令介绍

## 工具命令
1. 查看设备信息, 格式: 设备id:设备属性     ,设备属性中，android_version就是设备版本，即android device platform version

```
# PC中，执行ainfo命令，打印该PC连接的所有设备信息及设备属性
> ainfo
{'127.0.0.1:6555': {'ip': None, 'model': 'SAMSUNG-SM-N900A', 'cpu': 'x86', 'pad_version': 'hlteatt-userdebug 4.4.4 tt eng.jenkins.20171226.140228 release-keys', 'android_version': '4.4.4', 'android_api_version': '19', 'linux_version': 'Linux version 3.10.0+ (ttvm@TianTian-Dev) (gcc version 4.6 20120106 (prerelease) (GCC) ) #13 SMP PREEMPT Mon Dec 18 11:26:12 CST 2017'}}
```

![ainfo-cmd.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/ainfo-cmd.png)

2. 查看apk信息，其中主要关注，appPackage和appActivity 

```
# PC中，执行ainfo --apk APK_FILE 命令，查看apk信息
> ainfo --apk C:\ApiDemos-debug.apk
{'platformName': 'Android', 'deviceName': None, 'platformVersion': None, 'app': 'C:\\d_disk\\auto\\buffer\\test\\tools\\android\\ApiDemos-debug.apk', 'appPackage': 'io.appium.android.apis', 'appWaitPackage': 'io.appium.android.apis', 'appActivity': 'io.appium.android.apis.ApiDemos', 'unicodeKeyboard': True, 'resetKeyboard': True, 'newCommandTimeout': 120000}
```

## 场景一  本地测试

一般情况下，就是一台PC，连接一台设备的测试场景，步骤如下

**1.测试场景假设**

```
 apk(待测试的apk): C:\ApiDemos-debug.apk
 case(自动化测试用例): C:\test_case.yaml

 PC_A_IP(本机): 192.168.1.1
 PC_A_Android_Device_ID(天天模拟器): 127.0.0.1:6555
```

**2.开启appium server,并绑定待测设备**

```
#  PC_A，监听4723端口，该端口绑定  id为127.0.0.1:6555并且版本为4.4.4的设备；注意，监听端口+1也会被占用
> appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4

```

**3.aldriver驱动测试**

```
# aldriver命令执行本地测试，该命令主动连接本地PC_A的4723端口，并驱动adb连接的第一个设备进行测试
# 这就是为什么，在假设场景中，要求appserver使用PC_A使用本机IP和4723端口，并绑定名字是 127.0.0.1:6555 的设备
> aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk

# 如果，你没有apk,但是通过 工具命令，获取到 appPackage和appActivity，可以使用下述命令；原理相当于appium中的，start_activity(package, activity)
#> aldriver C:\test_case.yaml --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos

# 当然，也可以补全所有参数
#> aldriver C:\test_case.yaml --apk C:\ApiDemos-debug.apk --package io.appium.android.apis --activity io.appium.android.apis.ApiDemos
```

**4.释放端口占用**

> ctrl + c 结束端口占用

![scene-1.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/scene-1.png)

## 场景二 远程控制测试-Selenium Grid Mode

**测试背景及分析**

```
背景: 
    比如，手上有1000条相对独立的测试case，一台PC一台设备的方式完成这些case的验证，效率较低。那么，并行测试是最好的解决办法

分析: 
    1.多台PC连接多台设备的测试场景假设,其原理是基于selenium RC，使用selenium Grid的方式，使得appium server作为node节点，进行分布式测试
    2.可是，即使是分布式测试，它的过程也是一个并发的过程，每台设备分别都要测试1000条case。好比很多车在支路上跑，汇入的主干道却只有一条
    3.需要做的，就是让这1000条case，分配给这些设备，让它们并行测试。解决方法：多重hub
```

多台PC,连接多台设备,并行测试case场景，步骤如下

**1.测试场景假设**

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

![grid-hub.png](https://raw.githubusercontent.com/RockFeng0/img-folder/master/rtsf-app-img/grid-hub.png)

**2.开启selenium grid hub**

命令详解，参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)

```
# PC_Server设置PC_A的hub
> wrhub C:\selenium-server-standalone-3.14.0.jar --port 4444

# PC_Server设置PC_B的hub
> wrhub C:\selenium-server-standalone-3.14.0.jar --port 5555
```

**3.开启appium server node**

```
# PC_A  4723端口绑定设备，并注册node节点 
> appserver 192.168.1.1:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 4444

# PC_A  4725端口绑定设备，并注册node节点 
> appserver 192.168.1.1:4725 --device-name DEVICE_ID --device-version DEVICE_VERSION --hub-ip 192.168.1.254 --hub-port 4444
...

# PC_B, 同理
> appserver 192.168.1.2:4723 --device-name 127.0.0.1:6555 --device-version 4.4.4 --hub-ip 192.168.1.254 --hub-port 5555
...
```

**4.ardriver驱动测试**

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

## 测试报告及日志

> 执行结束后，测试用例所在路径，就是report生成的路径


# 编写测试用例，模板基于rtsf

> 变量引用-> $var    关键字(函数)引用-> ${function}

- 常量的定义， glob_var 和  glob_regx
- 模板常用的关键字，参见 [rtsf](https://github.com/RockFeng0/rtsf)介绍

## 基本用例

基本用例，是指没有分层的情况下，简单的测试用例

```
# test_case.yaml
# yaml测试用例，模型示例:
- project:
    name: xxx App
    module: xxx模块-功能测试
    
- case:
    # id desc 选填，非约定字段 
    id: ATP-1
    desc: 测试用例-模板格式的设计-模板（全字段）
    
    # name 必填，需确保唯一性
    name: android_app_ui_auto_test_demo_1
    
    # responsible 选填
    responsible: rockfeng0
    
    # tester 选填
    tester: rockfeng0
    
    # 定义正则表达式, 定义的字符串不会解析
    glob_regx:
        rex_bar_title: 'Views/Controls/(.*)'
    
    # 定义变量， 效果同 SetVar(name, value)
    glob_var:
        app_package: io.appium.android.apis
        app_main_activity: .ApiDemos
        app_view_webview_activity: .view.WebView1
        app_view_button_activity: .view.Buttons1
        app_view_control_activity: .view.Controls1
        app_view_dragdrop_activity: .view.DragAndDropDemo
        app_graphic_paint_activity: .graphics.TouchPaint
        app_animation_activity: .animation.BouncingBalls
        
    # pre_command 选填
    pre_command:
        - ${StartActivity($app_package, $app_view_control_activity)}
        - ${DyStrData(var_bar_title, $rex_bar_title)}
        - ${VerifyVar(var_bar_title, 1. Light Theme)}  
        
    # steps 必填
    steps:      
    
        # 在appdriver中，定位元素
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
                           
    # post_command 选填
    post_command:
        - ${Back()}
        - ${CloseApp()}

```

## 分层用例

- 分层用例，是指模块功能测试的时候，对测试用例进行分层，最小的单元为api，其次为suite，最后组成用例
- 其存放路径、编写规则等，详见 [rtsf](https://github.com/RockFeng0/rtsf)相关介绍
- 示例可以，参见[rtsf-http](https://github.com/RockFeng0/rtsf-http)相关介绍


# 封装的关键字(内置函数)

关键字的使用，在前面，有介绍，规则如下
> 变量引用-> $var    关键字(函数)引用-> ${function}

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


##  AppElement methods --> 元素定位相关操作

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

## 自定义，关键字(函数、变量)
> 在case同级目录中，创建  preference.py, 该文件所定义的 变量、函数，可以被动态加载和引用

执行用例的时候，可以使用 变量引用 或者关键字引用的方法，调用，自定义的函数和变量

```
# preference.py 示例

test_var = "hello rtsf."
def test_func():
    return "nihao rtsf."
 
