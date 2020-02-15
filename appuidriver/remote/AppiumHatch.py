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

import os,re, requests, subprocess
from rtsf.p_common import IntelligentWaitUtils
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
    def gen_capabilities(cls, apk_abs_path = None, app_package=None, app_activity=None, aapt_exe_4path = "aapt"):
        ''' generate capabilities from android apk
        
        @param apk_abs_path:  absolute android package path  
        @param app_package: app package name for `start_activity` first parameter.  if None, will grab from 'apk_abs_path'
        @param app_activity: app activity name for `start_activity` second parameter. if None, will grab from 'apk_abs_path'
        @param aapt_exe_4path: absoulte file path of `aapt.exe`, default is `aapt`  if ENV have been set
        @return: desired capabilities         
        '''
        capabilities = {
            'platformName': 'Android',
            'deviceName': None,
            'platformVersion': None,
            'app': None,
            'appPackage': None,
            'appWaitPackage': None,
            'appActivity': None,
            'unicodeKeyboard' : True , #支持中文输入; 如果Unicodekeyboard为true，那么在开始运行脚本的时候，会帮你安装appium自带的输入法，这个输入法是没有UI的
            'resetKeyboard' : True, #支持中文输入,两条都必须配置; 只有当你的用例是正常执行完毕，没被外界打断的情况下，而且resetkeyboard也为true的情况下，appium会帮你复原输入法
            'newCommandTimeout': 120000, # appium命令 --command-timeout 无效，使用cap中的 newCommandTimeout替代,单位 秒
        }
        
        if apk_abs_path != None and os.path.isfile(apk_abs_path):
            regx_pkg_info = re.compile('([\w]*)=\'([\w\.]*)\'')
            pkg_info_lines = list(cls.__command(r'%s dump badging %s' %(aapt_exe_4path, apk_abs_path)))
            
            # e.g. {'package': {'versionCode': '', 'name': 'io.appium.android.apis', 'versionName': ''}}
            apk_package = {"package":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "package:" in line}        
                    
            # e.g. {'launchable': {'label': '', 'name': 'io.appium.android.apis.ApiDemos', 'icon': ''}}
            apk_launchable = {"launchable":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "launchable-activity:" in line}
            
            capabilities["app"] = apk_abs_path
            capabilities["appPackage"] = apk_package["package"]["name"] if app_package is None else app_package
            capabilities["appWaitPackage"] = apk_package["package"]["name"] if app_package is None else app_package
            capabilities["appActivity"] = apk_launchable["launchable"]["name"] if app_activity is None else app_activity
        else:
            capabilities["appPackage"] = app_package
            capabilities["appWaitPackage"] = app_package
            capabilities["appActivity"] = app_activity            
            
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
    def get_executor(server_ip, server_port = 4723):
        '''  
        @param server_ip: hub ip of appium server ip
        @param server_port: hub port of appium server port
        '''
        return "http://{}:{}/wd/hub".format(server_ip, server_port)
    
    @staticmethod
    def get_remote_executors(hub_ip, port = 4444):
        ''' Get remote hosts from Selenium Grid Hub Console
        @param hub_ip: hub ip of selenium grid hub
        @param port: hub port of selenium grid hub
        '''        
        def req_remote_host():
            resp = requests.get("http://%s:%s/grid/console" %(hub_ip, port))
            
            remote_hosts = ()
            if resp.status_code == 200:
                remote_hosts = re.findall("udid: ([\w/\.:]+).*udversion: ([\\w/\\.:]*).*remoteHost: ([\w/\.:]+)",resp.text)
            return [(udid, udversion, host + "/wd/hub") for udid,udversion,host in remote_hosts]
        
        try:
            return IntelligentWaitUtils.until(req_remote_host, 10)
        except:
            return ()
    
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
