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

## 下载selenium-server-standalone.jar

> 参见[rtsf-web](https://github.com/RockFeng0/rtsf-web)项目，环境准备栏，给出的下载链接

