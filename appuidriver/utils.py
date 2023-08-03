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


android = _AndroidDevices()

if __name__ == "__main__":
    print(android.detect_info())
    print(android.current_activity())
    print(android.parse_apk("/buffer/some.apk"))
