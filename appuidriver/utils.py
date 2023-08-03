#! python3
# -*- encoding: utf-8 -*-

import json
from adbutils import adb


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


android = _AndroidDevices()

if __name__ == "__main__":
    print(android.detect_info())
    print(android.current_activity())
