#! python3
# -*- encoding: utf-8 -*-


import unittest
import os
from appuidriver.remote.AppiumHatch import Android
from appuidriver.remote.AppiumJs import AppiumJs
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
        desired_cap = Android.gen_capabilities(app_package='io.appium.android.apis', app_activity='.animation.BouncingBalls')
        self.assertEqual(desired_cap["appium:app"], None)
        self.assertEqual(desired_cap["appium:appPackage"], 'io.appium.android.apis')
        self.assertEqual(desired_cap["appium:appActivity"], '.animation.BouncingBalls')

    def test_get_devices(self):
        devices = Android.get_devices()
        print("devices:", devices)

        if devices:
            for prop in ("serial", "model", "linux_version", "ip", "cpu", "android_version", "pad_version"):
                self.assertIn(prop, devices[0])
        else:
            self.assertIsInstance(devices, dict)

    def test_gen_remote_driver(self):
        server = AppiumJs(port=4723).bind_device(device_id="127.0.0.1:6555")
        server.start_server()

        desired_cap = Android.gen_capabilities(apk_abs_path=self._apk_abs_path)
        self.assertIsInstance(desired_cap, dict)

        devices = Android.get_devices()
        self.assertIsInstance(devices, list)

        desired_cap["deviceName"] = devices[0]["model"]
        desired_cap["platformVersion"] = devices[0]["android_version"]

        driver = Android.gen_remote_driver(executor=Android.get_executor("localhost", 4723), capabilities=desired_cap)
        driver.quit()
        server.stop_server()

    def test_gen_remote_driver_grid(self):
        self._hub.start_server()

        device_name = "127.0.0.1:6555"
        device_version = "4.4.4"
        node_ip = "localhost"
        port = 4723
        # todo 调试
        server = AppiumJs(port = port).bind_device(device_id = device_name, platform_version = device_version).node(node_ip, hub_address=("localhost", 4444))
        server.start_server()

        drivers = []
        desired_cap = Android.gen_capabilities(apk_abs_path = self._apk_abs_path, aapt_exe_4path = self._aapt_exe_path)
        executors = Android.get_remote_executors(hub_ip = "localhost", port = 4444)
        for udid, udversion, executor in executors:
            cap = desired_cap.copy()
            cap["deviceName"] = udid
            cap["platformVersion"] = udversion

            driver = Android.gen_remote_driver(executor = executor, capabilities = cap)
            drivers.append(driver)
            driver.quit()

        self.assertEqual(len(drivers), 1)
        self.assertEqual(udid, device_name)
        self.assertEqual(udversion, device_version)
        self.assertEqual(executor, "http://{}:{}/wd/hub".format(node_ip, port))

        server.stop_server()
        self._hub.stop_server()


if __name__ == "__main__":
    unittest.main()
    # suite = unittest.TestSuite()
    # suite.addTest(TestAndroid("test_gen_capabilities"))
    # runner = unittest.TextTestRunner(verbosity=2)
    # runner.run(suite)

