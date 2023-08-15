#! python3
# -*- encoding: utf-8 -*-

import os
import json
from appuidriver import Cap, utils


class AppiumNode:
    def __init__(self):
        utils.check_appium_installed()
        self.file_path = ""
        self.command = ""

    def set_node_config(self, node_host, node_port=4723, hub_ip="localhost", hub_port=4444, file_path=None):
        """ appium 2+, Using Selenium Grid 3
        1. appium server --nodeconfig /path/to/nodeconfig.json --base-path=/wd/hub

        """
        self.command = "appium server --nodeconfig {} --base-path=/wd/hub"
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
        self.file_path = os.path.abspath(file_path)
        self.command = self.command.format(self.file_path)

    def set_toml(self, appium_host, appium_port=4723, file_path=None):
        """ appium 2+, Using Selenium Grid 4
        1. appium server -p 4723
        2. appium server -p 4733
        3. java -jar /path/to/selenium.jar node --config node1.toml
        4. java -jar /path/to/selenium.jar node --config node2.toml
        5. java -jar /path/to/selenium.jar hub

        """
        self.command = "java -jar {} node --config {}"

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
        self.file_path = os.path.abspath(file_path)
        self.command = self.command.format("{}", self.file_path)


if __name__ == '__main__':
    node = AppiumNode()
    node.set_node_config(node_host="192.168.146.13", file_path=r'C:\Python')
    print("Please manually start server with command: ", node.command)

    node.set_toml(appium_host="192.168.146.13", file_path=r'C:\Python')
    print("Please manually start server with command: ", node.command)
