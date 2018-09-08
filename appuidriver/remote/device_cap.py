#! python3
# -*- encoding: utf-8 -*-
'''
Current module: appuidriver.remote.device_cap

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      appuidriver.remote.device_cap,  v1.0 2018年9月8日
    FROM:   2018年9月8日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import os, re

class Android(object):
    
    @classmethod
    def gen_capabilities(cls, apk_abs_path, aapt_exe_4path = "aapt"):
        ''' generate capabilities from android apk
        @param apk_abs_path:  absolute android package path  
        @param aapt_exe_4path: absoulte file path of `aapt.exe`, default is `aapt`  if ENV have been set         
        '''
        capabilities = {}
        if not os.path.isfile(apk_abs_path):
            return capabilities
        
        regx_pkg_info = re.compile('([\w]*)=\'([\w\.]*)\'')
        pkg_info_lines = list(cls.__command(r'%s dump badging %s' %(aapt_exe_4path, apk_abs_path)))
        apk_package = {"package":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "package:" in line}
        apk_launchable = {"launchable":dict(regx_pkg_info.findall(line)) for line in pkg_info_lines if "launchable-activity:" in line}
                    
        capabilities = {
            'platformName': 'Android',
            'deviceName': None,
            'platformVersion': None,
            'app': apk_abs_path,
            'appPackage': apk_package["name"],
            'appWaitPackage': apk_package["name"],
            'appActivity': apk_launchable["name"],
        }
        return capabilities

    @classmethod
    def get_devices(cls, adb_exe_full_path="adb"):
        ''' get devices id form parsed command `adb devices`
        @param adb_exe_full_path: full path of executable adb, default is adb if ENV have been set. 
            
        '''
        devices = []
        # 读取设备 id
        cmd_start_server = adb_exe_full_path + " start-server"
        cmd_devices = adb_exe_full_path + " devices"        
        
        cls.__command(cmd_start_server)
        device_ids = cls.__command(cmd_devices)[1:-1]        
        if not device_ids:
            print("No device is connected.")
            return devices
        
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
    
    @classmethod
    def __command(cls, cmd, readlines = True):
        with os.popen(cmd) as f:
            if readlines:
                result = f.readlines()
            else:
                result = f.read()
        return result