#! python3
# -*- encoding: utf-8 -*-


import unittest
import os
import time
from appuidriver.remote.AppiumJs import AppiumJs
from webuidriver.remote.SeleniumJar import SeleniumJar


class TestAppiumJs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.server = AppiumJs(port=4723)

    def tearDown(self):
        self.server.stop_server()

    def test_AppiumJs_bind_device_1(self):
        # device is connected
        self.server.bind_device(device_id="127.0.0.1:6555")

        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)

        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)

    def test_AppiumJs_bind_device_2(self):
        # device is not connected
        self.server.bind_device(device_id="rock test")

        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)

        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)

    def test_AppiumJs_node(self):
        jar_path = r'C:\d_disk\auto\buffer\test\tools\seleniumjar\selenium-server-standalone-3.14.0.jar'
        java_path = "java"
        hub = SeleniumJar(jar_path, java_path).hub(4444)
        hub.start_server()
        self.assertEqual(hub.is_runnnig(), True)

        self.server.bind_device(device_id="127.0.0.1:6555", platform_version="4.4.4").node("localhost", hub_address=("localhost", 4444))
        self.assertTrue(os.path.isfile('nodeconfig.json'))
        self.assertEqual(self.server._cap.get('udid'), "127.0.0.1:6555")
        self.assertEqual(self.server._cap.get('udversion'), "4.4.4")

        self.server.start_server()
        self.assertEqual(self.server.is_runnnig(), True)

        self.server.re_start_server()
        self.assertEqual(self.server.is_runnnig(), True)

        hub.stop_server()


if __name__ == "__main__":
    unittest.main()

