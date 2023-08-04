#! python3
# -*- encoding: utf-8 -*-

import os
import re
import requests
import subprocess
from appium import webdriver
from rtsf.p_common import IntelligentWaitUtils
from appuidriver import utils,Cap

class IOS(object):
    pass


class Android(object):

    @classmethod
    def gen_capabilities(cls, apk_abs_path=None, app_package=None, app_activity=None, aapt_exe_4path=None):
        """ aapt_exe_4path 参数在 rtsf v1.2.3 之后版本 弃用 """

        if os.path.isfile(apk_abs_path):
            cap = Cap.android.with_app(apk_abs_path)
        else:
            cap = Cap.android.with_pkg(
                package=app_package,
                activity=app_activity
            )

        return cap.to_dict()

    @classmethod
    def get_devices(cls, adb_exe_full_path=None):
        """ adb_exe_full_path 参数在 rtsf v1.2.3 之后版本 弃用 """

        return utils.android.detect_info()

    @staticmethod
    def get_executor(server_ip, server_port=4723, base_url=None):
        """appium server 2.x 以上版本没有base_url,  1.x版本  需要base_url /wd/hub
        :param server_ip: hub ip or appium server ip
        :param server_port: hub port or appium server port
        :param base_url: /wd/hub or None
        :return:
        """
        if base_url:
            # appium 1.x
            return "http://{}:{}/wd/hub".format(server_ip, server_port)
        return "http://{}:{}".format(server_ip, server_port)  # appium 2.x

    @staticmethod
    def get_remote_executors(hub_ip, port=4444):
        """ 不支持 selenium Grid 4+ """
        print("‘get_remote_executors’ is deprecated at selenium Grid 4+")

        def req_remote_host():
            resp = requests.get("http://%s:%s/grid/console" % (hub_ip, port))

            remote_hosts = ()
            if resp.status_code == 200:
                remote_hosts = re.findall("udid: ([\w/\.:]+).*udversion: ([\\w/\\.:]*).*remoteHost: ([\w/\.:]+)", resp.text)
            return [(udid, udversion, host + "/wd/hub") for udid, udversion, host in remote_hosts]

        try:
            return IntelligentWaitUtils.until(req_remote_host, 10)
        except:
            return ()

    @staticmethod
    def gen_remote_driver(executor, capabilities):
        """ Generate remote drivers with desired capabilities(self.__caps) and command_executor
        @param executor: command executor for appium remote driver
        @param capabilities: A dictionary of capabilities to request when starting the appium session.
        @return: remote driver
        """
        firefox_profile = capabilities.pop("firefox_profile", None)
        return webdriver.Remote(command_executor=executor, desired_capabilities=capabilities, browser_profile=firefox_profile)

    @classmethod
    def __command(cls, cmd, readlines=True):
        """ just execute the command, usage:
            pkg_info = cls.__command('aapt.exe dump badging xxx.apk')
            properties = __command('adb.exe -s emulator-5554 shell cat /system/build.prop')
            linux_version = cls.__command('adb.exe -s emulator-5554 shell cat /proc/version', readlines=False)
        """
        subp = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if readlines:
            byte_result = subp.stdout.readlines()
            try:
                result = [i.decode('utf-8') for i in byte_result]
            except:
                result = [i.decode('cp936') for i in byte_result]
        else:
            byte_result = subp.stdout.read()
            try:
                result = byte_result.decode('cp936')
            except:
                result = byte_result.decode('utf-8')

        return result

