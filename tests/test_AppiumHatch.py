#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_AppiumHatch

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      tests.test_AppiumHatch,v 1.0 2018年9月9日
    FROM:   2018年9月9日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import unittest
from appuidriver.remote.AppiumHatch import Android
from appuidriver.remote.AppiumJs import AppiumJs

class TestAndroid(unittest.TestCase):
    
    def setUp(self):
        self._adb_exe_path = r'D:\auto\buffer\test\test_rtsf_web\android\adb.exe'
        self._aapt_exe_path = r'D:\auto\buffer\test\test_rtsf_web\android\aapt.exe'
        self._apk_abs_path = r'D:\auto\buffer\test\test_rtsf_web\ApiDemos-debug.apk'        
        
    def test_gen_capabilities(self):
        desired_cap = Android.gen_capabilities(self._apk_abs_path, self._aapt_exe_path)
        #print("caps: ",desired_cap)
        
        self.assertIsInstance(desired_cap, dict)
        self.assertEqual(desired_cap["app"], self._apk_abs_path)
        self.assertEqual(desired_cap["appPackage"], 'io.appium.android.apis')
        self.assertEqual(desired_cap["appWaitPackage"], 'io.appium.android.apis')
        self.assertEqual(desired_cap["appActivity"], 'io.appium.android.apis.ApiDemos')
        
        self.assertEqual(desired_cap["platformName"], "Android")
        self.assertEqual(desired_cap["deviceName"], None)
        self.assertEqual(desired_cap["platformVersion"], None)        
        
    def test_get_devices(self):
        devices = Android.get_devices(self._adb_exe_path)
        #print("devices:",devices)
        
        if devices:
            device_id, properties = devices.popitem()
            self.assertIsNotNone(device_id)
            for prop in ("model", "linux_version", "ip", "cpu", "android_version", "pad_version"):
                self.assertIn(prop, properties)            
        else:
            self.assertIsInstance(devices, dict)
            
    def test_gen_remote_driver(self):
        server = AppiumJs(port = 4723, timeout = 120000).bind_device(device_id = "127.0.0.1:5555")        
        server.start_server()
        
        desired_cap = Android.gen_capabilities(self._apk_abs_path, self._aapt_exe_path)
        self.assertIsInstance(desired_cap, dict)
        
        devices = Android.get_devices(self._adb_exe_path)
        self.assertIsInstance(devices, dict)
        
        device_id, properties = devices.popitem()
        desired_cap["deviceName"] = device_id
        desired_cap["platformVersion"] = properties.get('android_version')
        
        driver = Android.gen_remote_driver(executor = Android.get_remote_executor("localhost", 4723), capabilities = desired_cap)
        driver.quit()        
        server.stop_server()
        
if __name__ == "__main__":
    unittest.main()