# rtsf-app
基于rtsf测试框架，关键字驱动Android UI,进行自动化的功能测试


安装 appium命令行
1. 下载安装node.js
2. 安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
3. 安装appium: cnpm install appium -g
4. 启动appium: appium.cmd --command-timeout 120000 -p 4723 -U device_id_1
5。 appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U device_id_1

安装android sdk， 或者 我这里打包好的 tools,包含 adb.exe 和aapt.exe