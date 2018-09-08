# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiappium.AppiumServer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.AppiumServer,v 2.0 2017年2月7日
    FROM:   2017年1月25日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import subprocess,requests
from rtsf.p_common import  IntelligentWaitUtils

class AppiumServer:
    
    def __init__(self, appium_js_full_path, node_exe_full_path = "node", port = 4725, loglevel = "info:info"):  
        '''
        @note: 安装 appium命令行
            1. 下载安装node.js
            2. 安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
            3. 安装appium: cnpm install appium -g
            4. 启动appium: appium.cmd --command-timeout 120000 -p 4723 -U device_id_1
            5。 appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U device_id_1
        @param appium_js_full_path: npm安装appium后，window默认位置-> %appdata%\npm\node_modules\appium\build\lib\main.js
        @param node_exe_full_path:  absolute file path of executable `node`
        @param port:  appium server监听的端口, 通过该端口 , appium client使用 Remote连接，进行远程控制。 如， http://127.0.0.1:4723/wd/hub, http://192.168.0.1:4723/wd/hub
        @param loglevel: appium的日志级别    
        '''
        self.__port = port        
        self.appium_cmd = [node_exe_full_path, appium_js_full_path, "-p", str(port), "-bp", str(port + 1), "--log-level", loglevel]
    
    def bind_device(self, device_id, timeout = 120000,):
        ''' appium server bind to device.
        @param device_id:  连接的设备uuid, appium server通过 uuid保持对已连接到当前机器的设备，进行自动化控制
        @param timeout: 超时时间， case脚本与appium创建的session，此时间后，超时
        '''
        self.appium_cmd.extend(["--udid", device_id, "--command-timeout", str(timeout), "--no-reset"])
        return self
    
    def start_server(self):
        """start the appium server."""
        self.__subp = subprocess.Popen(self.appium_cmd)        
        print("\tappium server pid[%s] is running." %self.__subp.pid)
        IntelligentWaitUtils.wait_for_connection(port = self.__port)
        
    def stop_server(self):
        """stop the appium Server"""
        self.__subp.kill()
        print("\tappium server pid[%s] is stopped." %self.__subp.pid)
        
    def re_start_server(self):
        """reStart the appium server"""
        self.stop_server()
        self.start_server()
    
    def is_runnnig(self):
        """Determine whether appium server is running
        @return: True or False
        """
        resp = None
        try:
            resp = requests.get("http://127.0.0.1:%s/wd/hub/status" %self.__port)
            
            if resp.status_code == 200:
                return True
            else:
                return False
        except:
            return False
    
