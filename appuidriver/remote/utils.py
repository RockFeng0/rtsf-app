#! python3
# -*- encoding: utf-8 -*-

import os
import json
import zipfile
from adbutils import adb
from adbutils._utils import APKReader
from apkutils2.manifest import Manifest
from apkutils2.axml.axmlparser import AXML


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


class _Capabilities:

    def __init__(self):
        """
        :param app_package: appPackage
        :param app_activity: appActivity
        """
        self._capabilities = {
            'platformName': 'Android',
            'platformVersion': None,
            'deviceName': None,
            # 'app': None,
            'appPackage': None,
            'appActivity': None,
            'appWaitPackage': None,

            'unicodeKeyboard': True,  # 支持中文输入; 如果Unicodekeyboard为true，那么在开始运行脚本的时候，会帮你安装appium自带的输入法，这个输入法是没有UI的
            'resetKeyboard': True,  # 支持中文输入,两条都必须配置; 只有当你的用例是正常执行完毕，没被外界打断的情况下，而且resetkeyboard也为true的情况下，appium会帮你复原输入法
            'newCommandTimeout': 120000,  # appium命令 --command-timeout 无效，使用cap中的 newCommandTimeout替代,单位 秒
        }

    def from_apk(self, apk_abs_path):
        """ generate capabilities from android apk
        :param apk_abs_path:  absolute android package path
        """

        if not os.path.isfile(apk_abs_path):
            return {}

        with open(apk_abs_path, 'rb') as fp:
            ar = _APKReaderInfo(fp)
            pkg_info = ar.dump_info()

            # capabilities["app"] = apk_abs_path
            self._capabilities["appPackage"] = pkg_info["package"]
            self._capabilities["appWaitPackage"] = pkg_info["package"]
            self._capabilities["appActivity"] = pkg_info["main-activity"]

        return self

    def from_app(self, package, activity):
        self._capabilities["appPackage"] = package
        self._capabilities["appWaitPackage"] = activity
        self._capabilities["appActivity"] = activity
        return self

    def to_json(self):
        return json.dumps(self._capabilities)

    def to_dict(self):
        return self._capabilities

    def _w3c_webdriver_spec(self):
        self._w3c_spec =

class _Devices:

    def __init__(self):
        self._devices = []

    def from_adb(self):
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
        return self

    def to_json(self):
        return json.dumps(self._devices)

    def to_dict(self):
        return self._devices


cap = _Capabilities()
dev = _Devices()

if __name__ == "__main__":
    print(dev.from_adb().to_json())
    print(cap.from_app("package", "activity").to_json())
