#! python3
# -*- encoding: utf-8 -*-
'''
Current module: appuidriver.remote.AppiumHatch

Rough version history:
v1.0    Original version to use
V2.0    Change name from AppiumClient to AppiumHatch

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      appuidriver.remote.AppiumHatch,v 1.0 2018年9月9日
    FROM:   2017年2月3日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import os,re
from appium import webdriver

class IOS(object):
    ''' @todo: Methods for ios system. '''   
    pass

class Android(object):
    ''' Methods for adndroid system.
        1. generate capabilities for android
        2. get android devices
        3. generate appium webdriver
        ...
    '''
    
    @classmethod
    def gen_capabilities(cls, apk_abs_path, aapt_exe_4path = "aapt"):
        ''' generate capabilities from android apk
        @param apk_abs_path:  absolute android package path  
        @param aapt_exe_4path: absoulte file path of `aapt.exe`, default is `aapt`  if ENV have been set
        @return: desired capabilities         
        '''
        capabilities = {}
        if not os.path.isfile(apk_abs_path):
            return capabilities
        
        regx_pkg_info = re.compile('([\w]*)=\'([\w\.]*)\'')
        pkg_info_lines = list(cls.__command(r'%s dump badging %s' %(aapt_exe_4path, apk_abs_path)))
        
        # e.g. {'package': {'versionCode': '', 'name': 'io.appium.android.apis', 'versionName': ''}}
        apk_package = {"package":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "package:" in line}        
                
        # e.g. {'launchable': {'label': '', 'name': 'io.appium.android.apis.ApiDemos', 'icon': ''}}
        apk_launchable = {"launchable":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "launchable-activity:" in line}
                    
        capabilities = {
            'platformName': 'Android',
            'deviceName': None,
            'platformVersion': None,
            'app': apk_abs_path,
            'appPackage': apk_package["package"]["name"],
            'appWaitPackage': apk_package["package"]["name"],
            'appActivity': apk_launchable["launchable"]["name"],
        }
        return capabilities

    @classmethod
    def get_devices(cls, adb_exe_full_path="adb"):
        ''' parsed commands to get android devices infomation. 
        @param adb_exe_full_path: full path of executable `adb.exe`, default is `adb` if ENV have been set.
        @return: dict of devices infomation. formation is {device_id: device_info}
        '''
        
        os.popen(adb_exe_full_path + " start-server").close()
        device_ids = cls.__command(adb_exe_full_path + " devices")[1:-1]        
        if not device_ids:
            print("No device is connected.")
            return {}
        
        devices_info = {}                  
        regx_prop = re.compile('([\w\.]+)=(.*)')        
        for i in device_ids:
            deviceId,deviceStatus = i.split()        
            if deviceStatus != "device":
                print("Waring: %s" %i)
                continue
            
            properties = {}
            lines = cls.__command('%s -s %s shell cat /system/build.prop' %(adb_exe_full_path, deviceId))            
            _ = [properties.update(prop) for prop in [dict(regx_prop.findall(line)) for line in lines if "=" in line]]
            pad_ip = properties.get("dhcp.wlan0.ipaddress")
            pad_type = properties.get("ro.product.model")
            pad_version = properties.get("ro.build.display.id")
            pad_cpu = properties.get("ro.product.cpu.abi")
            android_version = properties.get("ro.build.version.release")
            android_api_version = properties.get("ro.build.version.sdk") 
            
            ver = cls.__command('%s -s %s shell cat /proc/version' %(adb_exe_full_path, deviceId), readlines=False)
            linux_version = ver.strip()
            
            devices_info[deviceId] ={
                'ip':pad_ip,
                'model':pad_type,
                'cpu':pad_cpu,
                'pad_version':pad_version,            
                'android_version':android_version,
                'android_api_version':android_api_version,
                'linux_version':linux_version,
                }
        return devices_info
    
    @staticmethod
    def get_remote_executor(hub_ip, port = 4723):
        ''' Get remote hosts from Selenium Grid Hub Console
        @param hub_ip: hub ip of appium server ip
        @param port: hub port of appium server port
        '''
        return "http://{}:{}/wd/hub".format(hub_ip, port)
    
    @staticmethod
    def gen_remote_driver(executor, capabilities):
        ''' Generate remote drivers with desired capabilities(self.__caps) and command_executor
        @param executor: command executor for appium remote driver
        @param capabilities: A dictionary of capabilities to request when starting the appium session.
        @return: remote driver
        '''         
        firefox_profile = capabilities.pop("firefox_profile",None)
        return webdriver.Remote(command_executor = executor, desired_capabilities=capabilities, browser_profile = firefox_profile)
    
    @classmethod
    def __command(cls, cmd, readlines = True):
        ''' just execute the command '''
        with os.popen(cmd) as f:
            if readlines:
                result = f.readlines()
            else:
                result = f.read()
        return result
