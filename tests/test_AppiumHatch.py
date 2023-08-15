#! python3
# -*- encoding: utf-8 -*-


import unittest
import os
from appuidriver import Cap, utils
from appuidriver.remote.AppiumHatch import Android
# from appuidriver.remote.AppiumJs import AppiumJs  # v1.2.3版本后弃用，请使用AppiumNonde
from appuidriver.remote.AppiumNode import AppiumNode
from webuidriver.remote.SeleniumJar import SeleniumJar


class TestAndroid(unittest.TestCase):

    def setUp(self):
        # platform_tools = r'C:\d_disk\auto\buffer\test\tools\android\platform-tools'
        # self._adb_exe_path = os.path.join(platform_tools, "adb.exe")
        # self._aapt_exe_path = os.path.join(platform_tools, "aapt.exe")
        self._apk_abs_path = r'C:\Python\ApiDemos-debug.apk'

        jar_path = r'C:\Python\selenium-server-standalone-3.14.0.jar'
        java_path = "java"
        self._hub = SeleniumJar(jar_path, java_path).hub(4444)

    def test_gen_capabilities(self):
        # e.g.1 with apk file
        desired_cap = Android.gen_capabilities(apk_abs_path=self._apk_abs_path)
        # print("caps: ", desired_cap)
        self.assertIsInstance(desired_cap, dict)
        self.assertEqual(desired_cap["appium:app"], self._apk_abs_path)
        self.assertEqual(desired_cap["appium:appPackage"], None)
        self.assertEqual(desired_cap["appium:appWaitPackage"], None)
        self.assertEqual(desired_cap["appium:appActivity"], None)

        # e.g.2  without apk file
        desired_cap = Android.gen_capabilities(app_package='com.android.settings', app_activity='.Settings')
        self.assertEqual(desired_cap["appium:app"], None)
        self.assertEqual(desired_cap["appium:appPackage"], 'com.android.settings')
        self.assertEqual(desired_cap["appium:appActivity"], '.Settings')

    def test_get_devices(self):
        devices = Android.get_devices()
        print("devices:", devices)

        if devices:
            for prop in ("serial", "model", "linux_version", "ip", "cpu", "android_version", "pad_version"):
                self.assertIn(prop, devices[0])
        else:
            self.assertIsInstance(devices, dict)

    def test_gen_remote_driver(self):
        # 连接设备, 配置capabilities
        desired_cap = Cap().android.with_pkg(
            package='com.android.settings',
            activity='.Settings'
        ).to_dict()

        devices = utils.android.detect_info()
        desired_cap["deviceName"] = devices[0]["model"]
        desired_cap["platformVersion"] = devices[0]["android_version"]

        # 配置节点
        node = AppiumNode()
        current_ip = "192.168.146.13"
        file_save_to = r'C:\Python'

        """ appium 2+ Grid 3
        1. java -jar C:\Python\selenium-server-standalone-3.14.0.jar -role hub
        2. appium server --nodeconfig C:\Python\nodeconfig.json --base-path=/wd/hub
        """
        # node.set_node_config(node_host=current_ip, file_path=file_save_to)
        # print("Please manually start server with command: ", node.command)
        # self.assertIsInstance(node.command, str)
        # executor = Android.get_executor("localhost", 4723, base_url=True)
        # driver = Android.gen_remote_driver(executor=executor, capabilities=desired_cap)
        # driver.quit()

        """ appium 2+ Grid 4
        1. appium server -p 4723
        2. java -jar C:\Python\selenium-server-4.11.0.jar hub --host 192.168.146.13
        3. java -jar C:\Python\selenium-server-4.11.0.jar node --config C:\Python\node.toml
        """
        node.set_toml(appium_host=current_ip, file_path=file_save_to)
        print("Please manually start server with command: ", node.command)
        self.assertIsInstance(node.command, str)
        executor = Android.get_executor("localhost", 4723, base_url=False)  # 没有base url
        driver = Android.gen_remote_driver(executor=executor, capabilities=desired_cap)
        driver.quit()


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestAndroid("test_gen_capabilities"))
    # print(suite.countTestCases())
    # # unittest.TextTestRunner(verbosity=2).run(suite)

