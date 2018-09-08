#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_AppiumServer

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_AppiumServer,  v1.0 2018年9月7日
    FROM:   2018年9月7日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest
from appuidriver.remote.AppiumServer import AppiumServer 

class TestAppiumServer(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls._adb_full_path = r'C:\d_disk\auto\buffer\test\tools\android\adb.exe'
        cls._appium_js_full_path = r'C:\Users\58-pc\AppData\Roaming\npm\node_modules\appium\build\lib\main.js'
        cls._node_exe_full_path = r'C:\Program Files\nodejs\node.exe'
        
        cls.server = AppiumServer(node_exe_full_path = cls._node_exe_full_path, appium_js_full_path=cls._appium_js_full_path, port = 4723)
        
    @classmethod
    def tearDownClass(cls):
        cls.server.stop_server()
                
    def test_AppiumServer(self):
        self.server.bind_device(device_id = "127.0.0.1:6555", timeout = 120000)
        
        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)
                
        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)
    
    def test_get_devices_id(self):
        devices = AppiumServer.get_devices_id(self._adb_full_path)
        self.assertIsInstance(devices, (list,tuple))
        print("all devices:",devices)
        
if __name__ == "__main__":
    unittest.main()
        
        