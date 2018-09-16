#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_AppiumJs

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_AppiumJs,  v1.0 2018年9月7日
    FROM:   2018年9月7日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest,os
from appuidriver.remote.AppiumJs import AppiumJs 

class TestAppiumJs(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.server = AppiumJs(port = 4723)
            
    def tearDown(self):        
        self.server.stop_server()
    
    def test_AppiumJs_bind_device_1(self):
        # device is connected
        self.server.bind_device(device_id = "127.0.0.1:6555")
        
        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)
        
        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)
    
    def test_AppiumJs_bind_device_2(self):
        # device is not connected
        self.server.bind_device(device_id = "rock test")
        
        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)
        
        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)
        
    def test_AppiumJs_node(self):
        self.server.bind_device(device_id = "127.0.0.1:6555").node("192.168.16.204", hub_address=("192.168.16.204", 4444))
        self.assertTrue(os.path.isfile('nodeconfig.json'))
        
        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)
        
        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)
                    
if __name__ == "__main__":
    unittest.main()
        
        