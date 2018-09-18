#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_driver,  v1.0 2018年9月18日
    FROM:   2018年9月18日
********************************************************************
======================================================================

Provide a function for the automation test

'''

#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_driver,  v1.0 2018年8月20日
    FROM:   2018年8月20日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest, os
from rtsf.p_executer import TestRunner
from rtsf.p_applog import logger
from appuidriver.driver import LocalDriver,RemoteDriver
from appuidriver.remote.AppiumJs import AppiumJs
from webuidriver.remote.SeleniumJar import SeleniumJar

class TestDriver(unittest.TestCase):
    '''
    @note:  adb version 1.0.39;  %ANDROID_HOME% = D:\auto\buffer\test\test_rtsf_web\android; 天天模拟器 v2.5.6
    '''
    @classmethod
    def setUpClass(cls):
        cls.case_file = r'data\test_case.yaml'
        cls.jar_path =  r'C:\d_disk\auto\buffer\test\tools\seleniumjar\selenium-server-standalone-3.14.0.jar'
        cls.java_path = "java"
        
        platform_tools = r'C:\d_disk\auto\buffer\test\tools\android\platform-tools'  
        cls._adb_exe_path = os.path.join(platform_tools, "adb.exe")  
        cls._aapt_exe_path = os.path.join(platform_tools, "aapt.exe")
        cls._apk_abs_path = r'C:\d_disk\auto\buffer\test\tools\android\ApiDemos-debug.apk'
        cls._app_package = 'io.appium.android.apis'
        cls._app_activity = '.ApiDemos'

    
    def test_LocalDriver(self):
        LocalDriver._adb_exe_path  = self._adb_exe_path
        LocalDriver._aapt_exe_path = self._aapt_exe_path
        LocalDriver._apk_abs_path  = self._apk_abs_path
        LocalDriver._app_package   = self._app_package
        LocalDriver._app_activity  = self._app_activity
        
        server = AppiumJs(port = 4723).bind_device(device_id = "127.0.0.1:6555", platform_version = "4.4.4")
        server.start_server()
        
        runner = TestRunner(runner = LocalDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
        
        server.stop_server()
        
    def test_RemoteDriver(self):
        RemoteDriver._aapt_exe_path = self._aapt_exe_path
        RemoteDriver._apk_abs_path  = self._apk_abs_path
        RemoteDriver._app_package   = self._app_package
        RemoteDriver._app_activity  = self._app_activity


        hub = SeleniumJar(self.jar_path, self.java_path).hub(4444)
        hub.start_server()
        
        node = AppiumJs(port = 4723).bind_device(device_id = "127.0.0.1:6555", platform_version = "4.4.4").node("localhost", hub_address=("localhost", 4444))
        node.start_server()        
        
        runner = TestRunner(runner = RemoteDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))
        
        node.stop_server()
        hub.stop_server()
        
if __name__ == "__main__":
#     logger.setup_logger("debug")
#     unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestDriver("test_LocalDriver"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    
    
    
    