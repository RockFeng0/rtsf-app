#! python3
# -*- encoding: utf-8 -*-
'''
Current module: tests.test_actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      tests.test_actions,  v1.0 2018年9月12日
    FROM:   2018年9月12日
********************************************************************
======================================================================

Provide a function for the automation test

'''

import unittest, os, re

from appuidriver.remote.AppiumJs import AppiumJs
from appuidriver.remote.AppiumHatch import Android
from appuidriver.actions import AppWait,AppElement,AppContext,AppVerify,App,AppActions,AppTouchAction

class TestActions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''
        @note:  adb version 1.0.39;  %ANDROID_HOME% = D:\auto\buffer\test\test_rtsf_web\android
        '''        
        platform_tools = r'C:\d_disk\auto\buffer\test\tools\android\platform-tools'
        cls._adb_exe_path = os.path.join(platform_tools, "adb.exe")
        cls._aapt_exe_path = os.path.join(platform_tools, "aapt.exe")
        cls._apk_abs_path = r'C:\d_disk\auto\buffer\test\tools\android\ApiDemos-debug.apk'
                
        cls.server = AppiumJs(port = 4723).bind_device(device_id = "127.0.0.1:6555")
        cls.server.start_server()
        
        devices = Android.get_devices(cls._adb_exe_path)
        device_id, properties = devices.popitem()
        
        desired_cap = Android.gen_capabilities(cls._apk_abs_path, cls._aapt_exe_path)
        desired_cap["deviceName"] = device_id
        desired_cap["platformVersion"] = properties.get('android_version')           
#         desired_cap = {
#             'platformName': 'Android',
#             'deviceName': '127.0.0.1:6555',
#             'platformVersion': '4.4.4',
#             'app': 'C: \\d_disk\\auto\\buffer\\test\\tools\\android\\ApiDemos-debug.apk',
#             'appPackage': 'io.appium.android.apis',
#             'appWaitPackage': 'io.appium.android.apis',
#             'appActivity': 'io.appium.android.apis.ApiDemos',
#             'unicodeKeyboard': True,
#             'resetKeyboard': True,
#             'newCommandTimeout':120000,
#         }
        App.driver = Android.gen_remote_driver(executor = Android.get_remote_executor("127.0.0.1", 4723), capabilities = desired_cap)
    
    @classmethod
    def tearDownClass(cls):
        App.QuitApp()
        cls.server.stop_server()
                   
    def test_AppElement(self):
        control = {"by":"111", "value" : "!!!", "index":22, "timeout":10}
        AppElement.SetControl(**control)
        self.assertEqual(AppElement.GetControl(), control)
        
        AppElement.SetControl(index = 0)
        self.assertEqual(AppElement.GetControl().get("index"), 0)
        
    def test_AppContext(self):
        app_package = 'io.appium.android.apis'
        app_activity = '.animation.BouncingBalls'
        bar_title = 'Animation/Bouncing Balls'
        
        App.StartActivity(app_package, app_activity)
        AppContext.DyPackageData('var_dy_app_package')
        self.assertEqual(AppContext.GetVar("var_dy_app_package"), app_package)        
        AppContext.DyActivityData('var_dy_app_activity')
        self.assertEqual(AppContext.GetVar("var_dy_app_activity"), app_activity)        
        
        AppContext.SetVar("var_app_package", app_package)        
        self.assertEqual(AppContext.GetVar("var_app_package"), app_package)        
        AppContext.SetVar("var_app_activity", app_activity)        
        self.assertEqual(AppContext.GetVar("var_app_activity"), app_activity)
        
        AppContext.DyStrData("var_bar_title", re.compile(bar_title))
        self.assertEqual(AppContext.GetVar("var_bar_title"), bar_title)
        
        AppElement.SetControl(by = "id", value = "android:id/action_bar_title")
        AppContext.DyAttrData("var_text", "text")
        self.assertEqual(AppContext.GetVar("var_text"), bar_title)        
        AppContext.DyAttrData("var_class_name", "className")
        self.assertEqual(AppContext.GetVar("var_class_name"), 'android.widget.TextView')
        App.CloseApp()
        
    def test_AppWait(self):
        App.StartActivity('io.appium.android.apis','.ApiDemos')        
        AppWait.TimeSleep(2)
        
        AppElement.SetControl(by = '-android uiautomator', value = 'text("Animation")')
        self.assertTrue(AppWait.WaitForAppearing())
        self.assertTrue(AppWait.WaitForVisible())
        App.CloseApp()
        
    def test_AppVerify(self):
        app_package = 'io.appium.android.apis'
        app_activity = '.animation.BouncingBalls'
        
        App.StartActivity(app_package, app_activity)
        self.assertTrue(AppVerify.VerifyAppInstalled(app_package))
        self.assertTrue(AppVerify.VerifyCurrentActivity(app_activity))
        
        AppElement.SetControl(by = '-android uiautomator', value = 'text("Animation/Bouncing Balls")')
        self.assertTrue(AppVerify.VerifyElemEnabled())
        self.assertTrue(AppVerify.VerifyElemVisible())
        self.assertTrue(AppVerify.VerifyElemAttr('text', 'Animation/Bouncing Balls'))
        self.assertTrue(AppVerify.VerifyElemAttr('clickable', 'false'))
        self.assertTrue(AppVerify.VerifyText("Animation/Bouncing Balls"))
        
        AppElement.SetControl(by = 'id', value = 'io.appium.android.apis:id/container')
        AppTouchAction.Draw()
        App.CloseApp()
        
    def test_AppTouchAction(self):
        App.StartActivity('io.appium.android.apis','.view.Controls1')
        
        AppElement.SetControl(by = 'id', value = 'io.appium.android.apis:id/edit')
        AppActions.SendKeys(u'你好    appium')
        
        AppElement.SetControl(by = '-android uiautomator', value = 'text("Checkbox 1")')
        AppTouchAction.Tap()
        AppVerify.VerifyElemAttr('checkable', "true")
        AppVerify.VerifyElemAttr('checked', "true")        
        AppTouchAction.Tap()
        AppVerify.VerifyElemAttr('checked', "false")
        
        AppTouchAction.Swipe("up", times = 1)        
        AppElement.SetControl(by = 'id', value = 'android:id/text1')
        AppTouchAction.Tap()        
        AppElement.SetControl(by = '-android uiautomator', value = 'text("Earth")')
        AppTouchAction.Tap()
        
        App.Back()
        
        App.StartActivity('io.appium.android.apis','.graphics.TouchPaint')
        AppTouchAction.Draw()
        
        App.StartActivity('io.appium.android.apis','.view.DragAndDropDemo')
        AppElement.SetControl(by = 'id', value = 'io.appium.android.apis:id/drag_dot_1')
        AppTouchAction.LongPress()
        
        AppElement.SetControl(by = 'id', value = 'io.appium.android.apis:id/drag_dot_2')
        AppTouchAction.MoveTo()
        AppTouchAction.Release()        
        
        App.CloseApp()
                
    def test_App(self):
        App.StartActivity('io.appium.android.apis','.ApiDemos')
        
        AppTouchAction.Swipe("up", times = 2)
        AppElement.SetControl(by = "-android uiautomator", value = 'text("Views")', index = 0, timeout = 10)
        AppTouchAction.Tap()
        
        AppTouchAction.Swipe("up", times = 10)
        AppElement.SetControl(by = "-android uiautomator", value = 'text("WebView")', index = 0, timeout = 10)
        AppTouchAction.Tap()
        
        # web-view
        App.SwitchToNewContext()
        self.assertEqual(App.driver.current_url, "data:text/html,<a href='x'>Hello World! - 1</a>")
        
        AppElement.SetControl(by = "css selector", value = "a")                
        self.assertEqual(AppVerify.VerifyText('Hello World! - 1'), True)
        
        # native
        App.SwitchToDefaultContext()
        App.Back()
        
        AppElement.SetControl(by = "-android uiautomator", value = 'text("WebView")', index = 0, timeout = 10)
        self.assertEqual(AppVerify.VerifyText("WebView"), True)
        AppTouchAction.Tap()
                        
        AppContext.DyPackageData("pkg")
        self.assertEqual(AppContext.GetVar('pkg'),'io.appium.android.apis')
        
        AppContext.DyActivityData("web_view_active")
        self.assertEqual(AppContext.GetVar('web_view_active'),'.view.WebView1')
        App.CloseApp()
        
        App.StartActivity(AppContext.GetVar('pkg'), '.view.Buttons1')
        self.assertEqual(AppVerify.VerifyCurrentActivity('.view.Buttons1'), True)
        
        App.StartActivity(AppContext.GetVar('pkg'), AppContext.GetVar('web_view_active'))
        self.assertEqual(AppVerify.VerifyCurrentActivity('.view.WebView1'), True)        
        App.CloseApp()    

if __name__ == "__main__":
    unittest.main()
#     suite = unittest.TestSuite()
#     suite.addTest(TestActions("test_AppTouchAction"))
#     runner = unittest.TextTestRunner(verbosity=2)
#     runner.run(suite)
    
    
    