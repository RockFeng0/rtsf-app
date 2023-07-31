#! python3
# -*- encoding: utf-8 -*-

import os
import re
import time
import json
import subprocess
import requests
from rtsf.p_common import IntelligentWaitUtils
from rtsf.p_exception import NotFoundError
from selenium.webdriver import DesiredCapabilities


class AppiumJs:
    """  安装 appium命令行
        1. 下载安装node.js, 默认安装后，设置了环境变量
        2. 安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
        3. 安装appium: cnpm install appium -g
        4. 启动appium: appium.cmd --command-timeout 120000 -p 4723
    """

    def __init__(self, port, loglevel="info:info"):
        """

        :param port: appium server listen port(通过该端口 , appium client使用 Remote连接，进行远程控制)
        :param loglevel: appium的日志级别
        """
        self._cap = DesiredCapabilities.ANDROID.copy()
        self.__port = port
        self.appium_cmd = ["appium",
                           "--keep-alive-timeout", str(port),
                           "--callback-port", str(port + 1),
                           "--log-level", loglevel,
                           ]

    def node(self, ip, hub_address=("localhost", 4444)):
        """ appium -p 4723 -bp 4724 --log-level info:info --udid 127.0.0.1:6555 --no-reset --nodeconfig c:\test\nodeconfig.json
        @note: java -jar c:\selenium-server-standalone-3.14.0.jar -role hub
        @param ip:    appium server listen ip, loopback ip not suggest to use in grid mode
        @param hub_address: hub address which node will connect to
        """
        if ip in ('localhost', "127.0.0.1"):
            print("Waring: loopback ip not suggest to use in grid mode. remoteHost is loopback address!!!")

        (_hub_ip, _hub_port) = hub_address

        _nodeconfig = {
            "capabilities": [self._cap],
            "configuration": {
                "role": "node",
                "remoteHost": "http://{}:{}".format(ip, self.__port),

                "url": "http://{}:{}/wd/hub".format(ip, self.__port),
                "host": ip,
                "port": self.__port,

                "hub": "http://{}:{}/grid/register".format(_hub_ip,_hub_port),
                "hubHost": _hub_ip,
                "hubPort": _hub_port,

                "proxy": "org.openqa.grid.selenium.proxy.DefaultRemoteProxy",
                "cleanUpCycle": 2000,
                "maxSession": 1,
                "register": True,
                "registerCycle": 5000,
                "timeout": 30000
            }
        }

        with open('nodeconfig.json', 'w') as f:
            f.write(json.dumps(_nodeconfig))

        self.appium_cmd.extend(["--nodeconfig", os.path.abspath("nodeconfig.json")])
        return self

    def bind_device(self, device_id, platform_version=""):
        """ appium -p 4723 -bp 4724 --log-level info:info --udid 127.0.0.1:6555 --no-reset
        @param device_id:  连接的设备uuid, appium server通过 uuid保持对已连接到当前机器的设备，进行自动化控制
        @param platform_version:  android设备的platform_version信息
        @param timeout: 超时时间， case脚本与appium创建的session，此时间后，超时
        """
        self._cap["udid"] = device_id
        self._cap["udversion"] = platform_version
        self.appium_cmd.extend(["--udid", device_id, "--no-reset"])
        return self

    def start_server(self):
        """start the appium server."""
        self.__subp = subprocess.Popen(self.appium_cmd)
        # print("\tappium server pid[%s] is running." %self.__subp.pid)
        IntelligentWaitUtils.wait_for_connection(port = self.__port)
        time.sleep(2)

    def stop_server(self):
        """stop the appium Server"""
        self.__subp.kill()
        # print("\tappium server pid[%s] is stopped." %self.__subp.pid)
        time.sleep(2)

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
            resp = requests.get("http://127.0.0.1:%s/wd/hub/status" % self.__port)

            if resp.status_code == 200:
                return True
            else:
                return False
        except:
            return False
