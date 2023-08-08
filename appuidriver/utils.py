#! python3
# -*- encoding: utf-8 -*-

import os
import re
import json
import zipfile
import requests
from bs4 import BeautifulSoup
from adbutils import adb
from adbutils._utils import APKReader
from apkutils2.manifest import Manifest
from apkutils2.axml.axmlparser import AXML

from rtsf.p_common import IntelligentWaitUtils


class _APKReaderInfo(APKReader):

    def dump_info(self):
        zf = zipfile.ZipFile(self._fp)
        raw_manifest = zf.read("AndroidManifest.xml")
        axml = AXML(raw_manifest)
        if not axml.is_valid:
            print("axml is invalid")
            return
        am = Manifest(axml.get_xml())
        return {
            "package": am.package_name,
            "main-activity": am.main_activity,
            "version-name": am.version_name,
            "version-code": am.version_code
        }


class _Devices:

    def __init__(self):
        self._devices = []

    def to_json(self):
        return json.dumps(self._devices)


class _IOSDevices(object):
    """ Methods for ios system. """
    pass


class _AndroidDevices(_Devices):

    def __init__(self):
        _Devices.__init__(self)

    def detect_info(self):
        """ parsed commands to get android devices infomation.
        @return: dict of devices infomation. formation is {device_id: device_info}
        """

        devices = adb.device_list()
        if not devices:
            print("No device is connected.")
            return self

        for d in devices:
            device_id = d.get_serialno()
            pad_ip = d.prop.get("dhcp.wlan0.ipaddress")
            pad_type = d.prop.get("ro.product.model")  # 型号 d.prop.model
            pad_version = d.prop.get("ro.build.display.id")  # 系统版本号
            pad_cpu = d.prop.get("ro.product.cpu.abi")
            android_version = d.prop.get("ro.build.version.release")  # Android版本
            android_api_version = d.prop.get("ro.build.version.sdk")  # SDK版本

            ver = d.shell("cat /proc/version")
            linux_version = ver.strip()

            self._devices.append({
                "serial": device_id,
                'ip': pad_ip,
                'model': pad_type,  # 型号
                'cpu': pad_cpu,
                'pad_version': pad_version,
                'android_version': android_version,
                'android_api_version': android_api_version,
                'linux_version': linux_version
            })
        return self._devices

    @staticmethod
    def current_activity():
        return adb.device().app_current()

    @staticmethod
    def parse_apk(apk_abs_path):
        """ python -m adbutils --parse some.apk """
        if not os.path.isfile(apk_abs_path):
            return

        with open(apk_abs_path, 'rb') as fp:
            ar = _APKReaderInfo(fp)
            return ar.dump_info()


class GridNodes(object):

    def __init__(self, hub_ip="localhost", hub_port=4444):
        """ 不区分Grid版本, 给hub ip 和 端口，探测 node节点"""
        self._host = hub_ip
        self._port = hub_port

    def list(self):
        checked = self._check_grid_response()
        if checked is None:
            return []

        tag = checked["tag"]
        response = checked["obj"]
        if tag == "graphql":
            # selenium grid 4+
            remote_hosts = response.json()
            # [('3aaf8978-9b47-4371-bf67-a70f7c9a981c', '4.11.0 (revision 3df8b70)', 'http://192.168.116.116:5556')]
            return [
                (node["id"], node["version"], node["uri"])
                for node in remote_hosts["data"]["nodesInfo"]["nodes"] if node["status"] == "UP"
            ]
        elif tag == "console":
            # selenium grid < 4
            cmp_1 = r"id: ([\w/\.:]+)"
            cmp_2 = r"udversion: ([\w/\\.:]*)"
            cmp_3 = r"remoteHost: ([\w/\\.:]+)"
            ll = []

            sp = BeautifulSoup(markup=response.text, features="html.parser")
            for node in sp.find_all(attrs={"type": "config", "class": "content_detail"}):
                _text = node.get_text(separator=" ")
                _id = re.findall(cmp_1, _text) if re.findall(cmp_1, _text) else [""]
                udversion = re.findall(cmp_2, _text) if re.findall(cmp_2, _text) else [""]
                _remote_host = re.findall(cmp_3, _text) if re.findall(cmp_3, _text) else [""]
                ll.extend(tuple(zip(_id, udversion, map(lambda x: x + "/wd/hub", _remote_host))))
            # if response.status_code == 200:
            #     remote_hosts = re.findall("udid: ([\w/\.:]+).*udversion: ([\\w/\\.:]*).*remoteHost: ([\w/\.:]+)", response.text)
            # return [(udid, udversion, host + "/wd/hub") for udid, udversion, host in remote_hosts]
            # [('http://192.168.116.116:5556', '', 'http://192.168.116.116:5556/wd/hub')]
            return ll
        else:
            return []

    def _check_grid_response(self):
        if not IntelligentWaitUtils.wait_for_connection(self._host, self._port, timeout=5):
            print("grid hub not connected.")
            return

        # selenium grid 4+
        url_graphql = "http://{}:{}/graphql".format(self._host, self._port)
        # selenium grid < 4
        url_console = "http://{}:{}/grid/console".format(self._host, self._port)

        payload = json.dumps({
            "operationName": "GetNodes",
            "variables": {},
            "query": "query GetNodes {\n  nodesInfo {\n    nodes {\n      id\n      uri\n      status\n      maxSession\n      slotCount\n      stereotypes\n      version\n      sessionCount\n      osInfo {\n        version\n        name\n        arch\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}"
        })

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url_graphql, headers=headers, data=payload)
        if response.status_code == 200:
            return {
                "tag": "graphql",
                "obj": response
            }

        response = requests.get(url_console)
        if response.status_code == 200:
            return {
                "tag": "console",
                "obj": response
            }
        return


android = _AndroidDevices()

if __name__ == "__main__":
    # nodes = GridNodes()
    # print(nodes.list())
    print(android.detect_info())
    print(android.current_activity())
    print(android.parse_apk("/buffer/some.apk"))
