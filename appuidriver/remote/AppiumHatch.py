#! python3
# -*- encoding: utf-8 -*-

import re
import requests
from rtsf.p_common import IntelligentWaitUtils
from appium import webdriver


class Android(object):
    """ Methods for adndroid system.
        1. generate capabilities for android
        2. get android devices
        3. generate appium webdriver
        ...
    """

    @staticmethod
    def get_executor(server_ip, server_port=4723):
        """
        @param server_ip: hub ip of appium server ip
        @param server_port: hub port of appium server port
        """
        return "http://{}:{}/wd/hub".format(server_ip, server_port)

    @staticmethod
    def get_remote_executors(hub_ip, port=4444):
        """ Get remote hosts from Selenium Grid Hub Console
        @param hub_ip: hub ip of selenium grid hub
        @param port: hub port of selenium grid hub
        """
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

