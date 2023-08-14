#! python3
# -*- encoding: utf-8 -*-

import os
import re
import time
import json
import subprocess
import json
from rtsf.p_common import IntelligentWaitUtils
from rtsf.p_exception import NotFoundError
from appuidriver import Cap


class Server(object):
    def __init__(self, command, port=4723):
        self.command = command
        self._sub_proc = None
        self.port = port

    def start_server(self):
        """start the appium server."""
        self._sub_proc = subprocess.Popen(self.command)
        # print("\tappium server pid[%s] is running." %self._sub_proc.pid)
        IntelligentWaitUtils.wait_for_connection(port=self.port)
        time.sleep(2)

    def stop_server(self):
        """stop the appium Server"""
        self._sub_proc.kill()
        # print("\tappium server pid[%s] is stopped." %self._sub_proc.pid)
        time.sleep(2)

    def re_start_server(self):
        """reStart the appium server"""
        self.stop_server()
        self.start_server()

    def is_runnnig(self, timeout=2):
        """ Determine whether appium server is running """

        # try:
        #     resp = requests.get("http://127.0.0.1:%s/wd/hub/status" % self._port)
        #
        #     if resp.status_code == 200:
        #         return True
        #     else:
        #         return False
        # except:
        #     return False
        return IntelligentWaitUtils.wait_for_connection(port=self.port, timeout=timeout)


class AppiumNode:

    @staticmethod
    def get_node_config(node_host, node_port=4723, hub_ip="localhost", hub_port=4444, file_path=None):
        """ appium 2+, Using Selenium Grid 3
        1. appium server --nodeconfig /path/to/nodeconfig.json --base-path=/wd/hub

        """

        if node_host in ('localhost', "127.0.0.1"):
            print("Waring: loopback ip not suggest to use in grid mode. remoteHost is loopback address!!!")

        _nodeconfig = {
            "capabilities": [Cap().android.to_dict()],
            "configuration": {
                "role": "node",
                "remoteHost": "http://{}:{}".format(node_host, node_port),

                "url": "http://{}:{}/wd/hub".format(node_host, node_port),
                "host": node_host,
                "port": node_port,

                "hub": "http://{}:{}/grid/register".format(hub_ip, hub_port),
                "hubHost": hub_ip,
                "hubPort": hub_port,

                "proxy": "org.openqa.grid.selenium.proxy.DefaultRemoteProxy",
                "cleanUpCycle": 2000,
                "maxSession": 1,
                "register": True,
                "registerCycle": 5000,
                "timeout": 30000
            }
        }
        file_path = os.path.join(file_path, 'nodeconfig.json') if file_path else 'nodeconfig.json'
        with open(file_path, 'w') as f:
            f.write(json.dumps(_nodeconfig))

        # usage: appium server --nodeconfig /path/to/nodeconfig.json --base-path=/wd/hub
        return os.path.abspath(file_path)

    @staticmethod
    def get_toml(appium_host, appium_port=4723, file_path=None):
        """ appium 2+, Using Selenium Grid 4
        1. appium server -p 4723
        2. appium server -p 4733
        3. java -jar /path/to/selenium.jar node --config node1.toml
        4. java -jar /path/to/selenium.jar node --config node2.toml
        5. java -jar /path/to/selenium.jar hub

        """

        toml = """
# node1.toml
[server]
port = 5555

[node]
detect-drivers = false

[relay]
url = "http://{0}:{1}"
status-endpoint = "/status"
configs = [
    "1", {2}
]
        """.format(appium_host, appium_port, json.dumps(Cap().android.to_json()))

        file_path = os.path.join(file_path, 'node.toml') if file_path else 'node.toml'
        with open(file_path, 'w') as f:
            f.write(toml)
        # usage: java -jar /path/to/selenium.jar node --config node.toml
        return os.path.abspath(file_path)

    @staticmethod
    def check_appium_installed():
        """ parse npm command to get `node` and `appium` absolute path.
        @note: node-npm just like python-pip
        @note: 安装 appium命令行
            1. 下载安装node.js, 默认安装后，设置了环境变量
            2. 安装cnpm: npm install -g cnpm --registry=https://registry.npm.taobao.org
            3. 安装appium: cnpm install appium -g
        # appium 1.x:
        #   appium.cmd --command-timeout 120000 -p 4723 -U 127.0.0.1:6555 --no-reset
        #   appium.cmd其实就是:  node "%appdata%\npm\node_modules\appium\build\lib\main.js" --command-timeout 120000 -p 4723 -U device_id_1
        # appium2.0后，管理driver和plugin路径不在 node模块库里边，而默认在%userprofile%/.appium
        #   appium server -p 4723 --allow-cors
        """

        regx_prefix = re.compile('.*prefix = (.*)')
        with os.popen('npm config list') as f:
            npm_config = f.readlines()

        if not npm_config:
            raise KeyError("Invalid command: `npm config list`. node.js should be installed before use npm command.")

        # e.g. prefix = "C:\\Users\\RockFeng\\AppData\\Roaming\\npm"  npm本地安装路径的前缀
        for line in npm_config:
            found = regx_prefix.findall(line)
            if found:
                npm_prefix_path = found[0]
                break

        # npm list appium --depth=0 --global  查看是否安装 appium
        regx_list_appium = re.compile('`-- (appium@.*)\n\n')
        with os.popen('npm list appium --depth=0 --global') as f:
            npm_list_appium = f.read()
        versions = regx_list_appium.findall(npm_list_appium)
        if not versions:
            raise NotFoundError('Not foud js module: `appium`. Use command to install appium: cnpm install appium -g')
        return versions


if __name__ == '__main__':
    print(AppiumNode.check_appium_installed())
    node_config_file = AppiumNode.get_node_config(node_host="192.168.146.13", file_path=r'C:\Python')
    print(node_config_file)
    tom_config_file = AppiumNode.get_toml(appium_host="192.168.146.13", file_path=r'C:\Python')
    print(tom_config_file)
