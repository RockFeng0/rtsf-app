#! python3
# -*- encoding: utf-8 -*-


import unittest
import os
from appuidriver.driver import LocalDriver, RemoteDriver
from appuidriver.remote.AppiumNode import AppiumNode
from webuidriver.remote.SeleniumJar import SeleniumJar
from rtsf.p_executer import TestRunner
from rtsf.p_applog import logger


class TestDriver(unittest.TestCase):
    """
    @note:  adb version 1.0.39;  %ANDROID_HOME% = D:\auto\buffer\test\test_rtsf_web\android; 天天模拟器 v2.5.6
    """
    @classmethod
    def setUpClass(cls):
        # tool_path = r'D:\auto\buffer\test\test_rtsf_web'
        __tool_path = r'C:\Python'

        cls.case_file = r'data\test_case.yaml'
        cls.data_driver_case = r'data\data_driver.yaml'

        cls.jar_path = os.path.join(__tool_path, "seleniumjar", "selenium-server-standalone-3.14.0.jar")
        cls.java_path = "java"

        cls._apk_abs_path = os.path.join(__tool_path, "ApiDemos-debug.apk")
        cls._app_package = 'io.appium.android.apis'
        cls._app_activity = '.ApiDemos'

        """ appium 2+ Grid 3
        1. java -jar C:\Python\selenium-server-standalone-3.14.0.jar -role hub
        2. appium server --nodeconfig C:\Python\nodeconfig.json --base-path=/wd/hub
        """
        node = AppiumNode()
        current_ip = "192.168.146.13"
        file_save_to = r'C:\Python'
        node.set_node_config(node_host=current_ip, file_path=file_save_to)
        print("Please manually start server with command: ", node.command)

    def test_LocalDriver(self):
        LocalDriver._apk_abs_path = self._apk_abs_path
        LocalDriver._app_package = self._app_package
        LocalDriver._app_activity = self._app_activity

        runner = TestRunner(runner=LocalDriver).run(self.case_file)

        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))

    def test_LocalDriver_with_datadriver(self):
        LocalDriver._apk_abs_path = self._apk_abs_path
        LocalDriver._app_package = self._app_package
        LocalDriver._app_activity = self._app_activity

        runner = TestRunner(runner = LocalDriver).run(self.data_driver_case)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))

    def test_RemoteDriver(self):
        RemoteDriver._apk_abs_path = self._apk_abs_path
        RemoteDriver._app_package = self._app_package
        RemoteDriver._app_activity = self._app_activity

        runner = TestRunner(runner=RemoteDriver).run(self.case_file)
        html_report = runner.gen_html_report()
        print(html_report)
        self.assertIsInstance(html_report, (list, tuple))


if __name__ == "__main__":
    # logger.setup_logger("debug")
    # unittest.main()
    suite = unittest.TestSuite()
    suite.addTest(TestDriver("test_LocalDriver_with_datadriver"))
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)


