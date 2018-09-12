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

import unittest

from appuidriver.remote.AppiumJs import AppiumJs
from appuidriver.remote.AppiumHatch import Android
from appuidriver.actions import AppWait,AppElement,AppContext,AppVerify,App,AppActions,AppTouchAction,AppSelActions

class TestActions(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        '''
        @note:  adb version 1.0.32;  %ANDROID_HOME% = C:\d_disk\auto\buffer\test\tools\android\platform-tools
        '''
        cls._adb_exe_path = r'C:\d_disk\auto\buffer\test\tools\android\platform-tools\adb.exe'
        cls._aapt_exe_path = r'C:\d_disk\auto\buffer\test\tools\android\platform-tools\aapt.exe'
        cls._apk_abs_path = r'C:\d_disk\auto\buffer\test\tools\android\ApiDemos-debug.apk'
        
        cls.server = AppiumJs(port = 4723, timeout = 120000).bind_device(device_id = "127.0.0.1:6555")
        cls.server.start_server()
        
        cls.executor = Android.get_remote_executor("localhost", 4723)        
        cls.desired_cap = Android.gen_capabilities(cls._apk_abs_path, cls._aapt_exe_path)
        devices = Android.get_devices(cls._adb_exe_path)
        
        device_id, properties = devices.popitem()
        cls.desired_cap["deviceName"] = device_id
        cls.desired_cap["platformVersion"] = properties.get('android_version')           
#         desired_cap = {
#             'platformName': 'Android',
#             'deviceName': '127.0.0.1: 6555',
#             'platformVersion': '4.4.4',
#             'app': 'C: \\d_disk\\auto\\buffer\\test\\tools\\android\\ApiDemos-debug.apk',
#             'appPackage': 'io.appium.android.apis',
#             'appWaitPackage': 'io.appium.android.apis',
#             'appActivity': 'io.appium.android.apis.ApiDemos',
#             'unicodeKeyboard': True,
#             'resetKeyboard': True
#         }
        
    
    def tearDown(self):
        AppWait.TimeSleep(5)
        App.QuitApp()
        self.server.stop_server()
        
    def test_pp(self):        
        App.driver = Android.gen_remote_driver(executor = self.executor, capabilities = self.desired_cap)
        AppTouchAction.Swipe("up", times = 2)
        AppElement.SetControl(by = "-android uiautomator", value = 'text("Views")', index = 0, timeout = 10)
        AppTouchAction.Tap()
    
    
        
#     def test_WebWait(self):
#         WebWait.SetControl(by = "id", value = 'kw', index = 0, timeout = 5)
#         self.assertEqual(WebWait.TimeSleep(1), None)
#         self.assertEqual(WebWait.WaitForDisappearing(), False)
#         self.assertEqual(WebWait.WaitForAppearing(), True)
#         self.assertEqual(WebWait.WaitForVisible(), True)
#     
#     def test_WebElement(self):
#         control = {"by":"111", "value" : "!!!", "index":22, "timeout":10}
#         WebElement.SetControl(**control)
#         self.assertEqual(WebElement.GetControl(), control)
#         
#         WebElement.SetControl(index = 0)
#         self.assertEqual(WebElement.GetControl().get("index"), 0)
#     
#     def test_WebContext(self):
#         url = "https://www.baidu.com"
#         WebContext.SetVar("url", url)        
#         self.assertEqual(WebContext.GetVar("url"), url)
#         
#         Web.NewTab(url)
#         
#         title = "百度一下，你就知道"
#         WebContext.DyStrData("title", re.compile(title))        
#         
#         WebElement.SetControl(by = "id", value = "su")        
#         WebContext.DyAttrData("su", "value")
#         
#         Web.NavigateTo("http://bztest.djtest.cn/background/pass/247686389303191")        
#         WebContext.DyJsonData("desc", "desc")
#         
#         self.assertEqual(WebContext.glob, {'url': 'https://www.baidu.com', 'title': '百度一下，你就知道', 'su': '百度一下', 'desc': '成功'})        
#         Web.WebClose()
#     
#     def test_WebVerify(self):
#         Web.NewTab('https://www.baidu.com')
#         
#         self.assertEqual(WebVerify.VerifyURL("https://www.baidu.com/"), True)
#         self.assertEqual(WebVerify.VerifyTitle("百度一下，你就知道"), True)
#         
#         WebElement.SetControl(by = "id", value = "su", index = 0, timeout = 10)
#         self.assertEqual(WebVerify.VerifyElemAttr("value", "百度一下"), True)
#         self.assertEqual(WebVerify.VerifyElemCounts(1), True)
#         self.assertEqual(WebVerify.VerifyElemEnabled(), True)
#         self.assertEqual(WebVerify.VerifyElemNotEnabled(), False)
#         self.assertEqual(WebVerify.VerifyElemVisible(), True)
#         self.assertEqual(WebVerify.VerifyElemNotVisible(), False)
#         
#         WebElement.SetControl(by = "id", value = "form")
#         self.assertEqual(WebVerify.VerifyElemInnerHtml("百度一下"), True)        
#         Web.WebClose()
#             
#     def test_App(self):
#         Web.NewTab('https://www.sina.com.cn')        
#         Web.Maximize()
#         self.assertEqual(WebVerify.VerifyURL("https://www.sina.com.cn/"), True)
#         WebWait.TimeSleep(1)
#          
#         Web.SetWindowSize(500, 500)
#         Web.ScrollTo(0, 10000)
#         WebWait.TimeSleep(1)
#            
#         Web.Refresh()
#         Web.NavigateTo("https:/www.baidu.com")
#         self.assertEqual(WebVerify.VerifyTitle("百度一下，你就知道"), True)
#         WebWait.TimeSleep(1)
#            
#         Web.Back()
#         WebWait.TimeSleep(1)
#            
#         Web.Forward()
#         WebWait.TimeSleep(1)
#          
#         p = os.path.join(self.test_tmp_path, "t.png")
#         Web.ScreenShoot(p)
#         self.assertEqual(os.path.isfile(p), True)      
#          
#         Web.WebClose()
#         m = re.search("百度一下，你就知道", Web.PageSource())
#         self.assertIsNotNone(m)
#     
#     def test_WebAction(self):
#         Web.NavigateTo('https:/www.sina.com')
#         Web.ScrollTo(0, 1000)
#         WebWait.TimeSleep(1)
#         Web.Refresh()
#         
#         Web.NewTab('https://www.baidu.com')
#         WebActions.SetControl(by = "css selector", value = "#kw")
#         WebActions.SendKeys("123456")
#         WebWait.TimeSleep(1)
#         Web.WebClose()
#     
#     def test_WebAction_rtsf(self):  
#         Actions = ModuleUtils.get_imported_module("webuidriver.actions")
#         Actions.Web.driver = self.driver
#             
#         functions = {}
#         web_functions = ModuleUtils.get_callable_class_method_names(Actions.Web)
#         web_element_functions = ModuleUtils.get_callable_class_method_names(Actions.WebElement)
#         web_context_functions = ModuleUtils.get_callable_class_method_names(Actions.WebContext)
#         web_wait_functions = ModuleUtils.get_callable_class_method_names(Actions.WebWait)
#         web_verify_functions = ModuleUtils.get_callable_class_method_names(Actions.WebVerify)
#         web_actions_functions = ModuleUtils.get_callable_class_method_names(Actions.WebActions)
#         functions.update(web_functions)
#         functions.update(web_element_functions)
#         functions.update(web_context_functions)
#         functions.update(web_wait_functions)
#         functions.update(web_verify_functions)
#         functions.update(web_actions_functions)  
#         self.assertNotEqual(functions, {})        
#         
#         print(functions)
#         functions.get("NavigateTo")("http://www.baidu.com")
#         functions.get("SetControl")(by = 'id', value = "kw")
#         functions.get("SendKeys")(123456)
#         time.sleep(1)
#         functions.get("WebClose")()
#         functions.get("WebQuit")()

if __name__ == "__main__":
    unittest.main()