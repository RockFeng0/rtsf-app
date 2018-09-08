#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_device_cap

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      tests.test_device_cap,v 1.0 2018年9月8日
    FROM:   2018年9月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import unittest
from appuidriver.remote.device_cap import Android

class TestAndroid(unittest.TestCase):
    
    def setUp(self):
        self._adb_exe_path = r'D:\auto\buffer\test\test_rtsf_web\android\adb.exe'
        self._aapt_exe_path = r'D:\auto\buffer\test\test_rtsf_web\android\aapt.exe'
        self._apk_abs_path = r'D:\auto\buffer\test\test_rtsf_web\ApiDemos-debug.apk'        
        
    def test_gen_capabilities(self):
        desired_cap = Android.gen_capabilities(self._apk_abs_path, self._aapt_exe_path)
        print(desired_cap)
        
        self.assertIsInstance(desired_cap, dict)
        self.assertEqual(desired_cap["app"], self._apk_abs_path)
        self.assertEqual(desired_cap["appPackage"], 'io.appium.android.apis')
        self.assertEqual(desired_cap["appWaitPackage"], 'io.appium.android.apis')
        self.assertEqual(desired_cap["appActivity"], 'io.appium.android.apis.ApiDemos')
        
    def test_get_devices(self):
        devices = Android.get_devices(self._adb_exe_path)
        print(devices)
        
        if devices:
            device_id, properties = devices.popitem()
            self.assertIsNotNone(device_id)
            for prop in ("model", "linux_version", "ip", "cpu", "android_version", "pad_version"):
                self.assertIn(prop, properties)            
        else:
            self.assertIsInstance(devices, dict)
        
if __name__ == "__main__":
    unittest.main()

        
        
        

    