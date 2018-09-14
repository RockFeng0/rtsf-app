# -*- encoding: utf-8 -*-
'''
Current module: rock4.softtest.pad.uiappium.actions

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.actions,v 1.0 2017年2月8日
    FROM:   2017年2月8日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

import time,re

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.mobileby import MobileBy

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

class App(object):
    driver = None    
    
    @staticmethod
    def LaunchApp():
        ''' use current session to launch and active the app'''        
        App.driver.launch_app()
        
    @staticmethod
    def StartActivity(app_package ,app_activity, timeout=10):
        ''' Only support android.  start an activity and focus to it
        @param app_package: app package name
        @param app_activity: activity name you want to focus to        
        '''
        App.driver.start_activity(app_package,app_activity)
        return App.driver.wait_activity(app_activity,timeout)
    
    @staticmethod
    def PageSource():
        ''' page source for this activity '''
        return App.driver.page_source
    
    @staticmethod
    def Forward():
        App.driver.forward()
       
    @staticmethod
    def Back():
        App.driver.back()
    
    @staticmethod
    def Shake():
        ''' 模拟设备摇晃 '''
        App.driver.shake()            
    
    @staticmethod
    def Lock(seconds):
        App.driver.lock(seconds)
    
    @staticmethod
    def BackgroundApp(seconds):
        '''应用会被放到后台特定时间,然后应用会重新回到前台 '''        
        App.driver.background_app(seconds)
    
    @staticmethod
    def OpenNotifications():
        App.driver.open_notifications()        
            
    @staticmethod
    def RemoveApp(app_package):
        ''' 卸载app '''
        App.driver.remove_app(app_package)
        
    @staticmethod
    def SwitchToDefaultContext():        
        try:
            App.driver.switch_to.context(App.driver.contexts[0])
        except:
            return False
        
    @staticmethod
    def SwitchToNewContext():
        try:
            WebDriverWait(App.driver, 10).until(lambda driver: len(driver.contexts) >= 2)
            new_context = App.driver.contexts[-1]
            App.driver.switch_to.context(new_context)       
        except Exception as e:
            print("@@@!!!", e)            
            print("Waring: Timeout at 10 seconds. New context Not Found.")
            return False
        
    @staticmethod
    def Reset():
        '''重置app, 即先closeApp然后在launchAPP '''
        App.driver.reset()
        
    @staticmethod
    def CloseApp():
        ''' only close app . keep the session'''        
        App.driver.close_app()
    
    @staticmethod
    def QuitApp():
        ''' will close the session '''
        try:
            App.driver.quit()            
        except:
            pass
        finally:
            App.driver = None  
        
class AppElement(object):
    
    __control = {
        "by":None,
        "value":None, 
        "index":0,
        "timeout":10,
        } 
                
    @classmethod
    def SetControl(cls,**kwargs):
        cls.__control.update(kwargs)
    
    @classmethod
    def GetControl(cls):
        return cls.__control
        
    @classmethod
    def _element(cls):
        '''   find the element with controls '''
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.__control["by"])
        
        driver = App.driver
        try:
            print("by: ", cls.__control["by"], "value: ",cls.__control["value"])            
            elements = WebDriverWait(driver, cls.__control["timeout"]).until(lambda driver: getattr(driver,"find_elements")(cls.__control["by"], cls.__control["value"]))
        except:                        
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.__control["timeout"],cls.__control["by"]))
        
        if len(elements) < cls.__control["index"] + 1:                    
            raise Exception("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.__control["index"]))
        
        if len(elements) > 1:              
            print("Element [%s]: There are [%d] elements, choosed index=%d" %(cls.__name__,len(elements),cls.__control["index"]))
        
        elm = elements[cls.__control["index"]]
        cls.__control["index"] = 0        
        return elm
    
    @classmethod
    def _elements(cls):
        '''   find the elements with controls '''
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.__control["by"])
        
        driver = App.driver
        try:            
            elements = WebDriverWait(driver, cls.__control["timeout"]).until(lambda driver: getattr(driver,"find_elements")(cls.__control["by"], cls.__control["value"]))
        except:            
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.__control["timeout"],cls.__control["by"]))
            
        return elements
       
    
    @classmethod
    def __is_selector(cls):
        '''
        @note: only web-view support:  MobileBy.CSS_SELECTOR, MobileBy.LINK_TEXT, MobileBy.NAME, MobileBy.PARTIAL_LINK_TEXT, MobileBy.TAG_NAME
        @note:  MobileBy.ANDROID_UIAUTOMATOR  
        
        e。g.  driver.find_elements_by_android_uiautomator('text("Views")');  driver.find_elements_by_android_uiautomator('new UiSelector().text("Views")')        
UiSelector的基本方法
        文本方面的方法：
　　1.text(String text) 文本
　　2.textContains(String text) 文本包含
　　3.textMatches(String regex) 文本正则
　　4.textStartsWith(String text) 文本开始字符 

描述方面的方法：
　　1.description(String desc) 描述
　　2.descriptionContains(String desc) 描述包含
　　3.descriptionMatches(String regex) 描述正则
　　4.descriptionStartsWith(String desc) 描述开始字符
 
类名方面的方法：
　　1.childSelector(UiSelector selector) 子类
　　2.className(String  className) 类名
 
索性、实例方面的方法：
　　1.index(int index) 编号
　　2.instance(int instantce) 索引

特有属性：
　　1.checked(boolean val) 选择属性
　　2.clickable(boolean val) 点击属性
　　3.enabled(boolean val) enabled属性
　　4.focusable(boolean val) 焦点属性
　　5.longClickable(boolean val) 长按属性
　　6.scrollable(boolean val) 滚动属性
　　7.selected(boolean val) 选择属性

包名方面的方法：
　　1.packageName(String name) 包名
　　2.packageNameMatches(String regex) 包名正则

资源ID方面的方法：
　　1.resourceId(String id) 资源ID
　　2.resourceIdMatches(String regex) 资源ID正则
        '''
        all_selectors = (MobileBy.ANDROID_UIAUTOMATOR, MobileBy.CLASS_NAME, MobileBy.ID, MobileBy.XPATH, MobileBy.CSS_SELECTOR, MobileBy.LINK_TEXT, MobileBy.NAME, MobileBy.PARTIAL_LINK_TEXT, MobileBy.TAG_NAME)
                        
        if cls.__control["by"] in all_selectors:
            return True
        
        print("Warning: selector[%s] should be in %s" %(cls.__control["by"],all_selectors))
        return False
               
                
class AppContext(AppElement):
    
    glob = {}
            
    @classmethod
    def SetVar(cls, name, value):
        ''' set static value
        :param name: glob parameter name
        :param value: parameter value
        '''
        cls.glob.update({name:value})
                
    @classmethod
    def GetVar(cls, name):
        return cls.glob.get(name)     
    
    @classmethod
    def DyActivityData(cls,name):
        cls.glob.update({name:App.driver.current_activity})
    
    @classmethod
    def DyPackageData(cls,name):
        cls.glob.update({name:App.driver.current_package})
    
    @classmethod
    def DyStrData(cls, name, regx, index = 0):
        ''' set dynamic value from the string data of response  
        @param name: glob parameter name
        @param regx: re._pattern_type
            e.g.
            DyStrData("a",re.compile('123'))
        '''
        text = App.PageSource()
        if not text:
            return
        if not isinstance(regx, re._pattern_type):
            raise Exception("DyStrData need the arg which have compiled the regular expression.")
            
        values = regx.findall(text)
        result = ""
        if len(values)>index:
            result = values[index]        
        cls.glob.update({name:result})
        
    @classmethod
    def DyAttrData(cls,name, attr):
        ''' node attribute '''
        attr_value = cls._element().get_attribute(attr)
        cls.glob.update({name:attr_value})
    
    @classmethod
    def DyXmlData(cls,name, sequence):
        ''' to do '''
        return
                
    @classmethod
    def GetText(cls):
        ''' node attribute: text '''
        return cls._element().text
    
         
class AppWait(AppElement):    
    
    @classmethod
    def TimeSleep(cls, seconds):
        time.sleep(seconds)
        
    @classmethod
    def WaitForAppearing(cls):        
        try:
            result = True if cls._element() else False                            
        except:
            result = False
        return result
        
    @classmethod
    def WaitForDisappearing(cls):        
        try:
            result = False if cls._element() else True
        except:
            result = True
        return result
        
    @classmethod
    def WaitForVisible(cls):
        try:
            result = cls._element().is_displayed()
        except:
            result = False        
        return result

class AppVerify(AppElement):
    
    
    @classmethod
    def VerifyAppInstalled(cls,app_package):
        return App.driver.is_app_installed(app_package)            
    
    @classmethod
    def VerifyCurrentActivity(cls, app_activity):        
        if App.driver.current_activity == app_activity:
            return True
        else:
            return False    
    
    @classmethod
    def VerifyText(cls, text):
        # 当前页面的title
        if cls._element().text == text:
            return True
        else:
            return False
            
    @classmethod
    def VerifyElemEnabled(cls):
        try:
            result = cls._element().is_enabled()                          
        except:
            result = False
        return result   
    
    @classmethod
    def VerifyElemNotEnabled(cls):
        try:
            result = False if cls._element().is_enabled() else True                          
        except:
            result = True
        return result   
    
    @classmethod
    def VerifyElemVisible(cls):
        ''' 仅限 Selenium，appium是否实现了类似功能不是太确定, 适用如，混合应用中，潜入了web的情况'''
        try:
            result = cls._element().is_displayed()
        except:
            result = False
        return result
    
    @classmethod
    def VerifyElemNotVisible(cls):
        ''' 仅限 Selenium，appium是否实现了类似功能不是太确定, 适用如，混合应用中，潜入了web的情况'''
        try:
            result = False if cls._element().is_displayed() else True
        except:
            result = True
        return result       
        
    @classmethod
    def VerifyElemAttr(cls, attr_name, expect_value):
        '''
        @note:  verify content of attribute is expected content
        @param attr_name: name of element attribute 
        @param expet_value: expect attribute value
        '''
        if expect_value in cls._element().get_attribute(attr_name):
            return True
        else:
            return False
    
    @classmethod
    def VerifyElemCounts(cls, num):        
        if len(cls._elements()) == num:
            return True
        else:
            return False
        
class AppTouchAction(AppElement):
    
    @classmethod
    def Tap(cls):
        element = cls._element()
        try:
            TouchAction(App.driver).tap(element).perform()
        except:
            return False
    
    @classmethod
    def LongPress(cls):
        element = cls._element()
        try:
            TouchAction(App.driver).long_press(element).perform()
        except:
            return False
            
    @classmethod
    def Press(cls):        
        element = cls._element()
        try:
            TouchAction(App.driver).press(element).perform()
        except:
            return False   
            
    @classmethod
    def MoveTo(cls):
        element = cls._element()
        try:
            TouchAction(App.driver).move_to(element).perform()
        except:
            return False
    
    @classmethod        
    def Release(cls):        
        try:
            TouchAction(App.driver).release().perform()
        except:
            return False   
                
    @classmethod
    def Draw(cls):
        ''' 模拟多个动作，这里，画了个笑脸   '''
        try:
            MultiAction(App.driver).add(TouchAction().press(x=150, y=100).release(),
                                        TouchAction().press(x=250, y=100).release(),
                                        TouchAction().press(x=110, y=200).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=2, y=1).release(),
                ).perform()
        except:
            return False
    
    @classmethod
    def Swipe(cls, direction, times = 1):
        ''' swipe screen
        @param direction: up, down, left, right
        '''
        size = App.driver.get_window_size()
        unit_width = size["width"] / 4
        unit_height = size["height"] / 4
        
        for _ in range(int(times)):
            if direction.lower() == "left":
                App.driver.swipe(unit_width *3, unit_height *2, unit_width *1, unit_height *2, 500)
            
            elif direction.lower() == "right":
                App.driver.swipe(unit_width *1, unit_height *2, unit_width *3, unit_height *2, 500)
            
            elif direction.lower() == "up":
                App.driver.swipe(unit_width *2, unit_height *3, unit_width *2, unit_height *1, 500)
            
            elif direction.lower() == "down":
                App.driver.swipe(unit_width *2, unit_height *1, unit_width *2, unit_height *3, 500)
            
class AppActions(AppElement):
    ''' selenium methods in appium
    @note: Waiting for improving
    '''
    
    @classmethod
    def Pinch(cls):
        try:
            App.driver.pinch(cls._element())
        except:
            return False
        
    @classmethod
    def Zoom(cls):
        try:
            App.driver.zoom(cls._element())
        except:
            return False
        
                
class AppSelActions(AppElement):
    ''' selenium methods in appium
    @note: Waiting for improving
    '''
            
    @classmethod
    def SendKeys(cls, value):
        '''
        @param value: 文本框，输入的文本
        '''
        if value == "":
            return
        
        element = cls._element()
        element.clear()        
        action = ActionChains(App.driver)
        action.send_keys_to_element(element, value)
        action.perform()
        
    @classmethod
    def Focus(cls):
        """        在指定输入框发送 Null， 用于设置焦点
        @note: key event ->  NULL
        """
        
        element = cls._element()
        #element.send_keys(Keys.NULL)        
        action = ActionChains(App.driver)
        action.send_keys_to_element(element, Keys.NULL)
        action.perform()
    
    @classmethod
    def Enter(cls):
        '''     在指定输入框发送回回车键
        @note: key event -> enter
        '''
        
        element = cls._element()        
        action = ActionChains(App.driver)
        action.send_keys_to_element(element, Keys.ENTER)
        action.perform()
            
        
   
        
    
'''
    
                        
        
def usage_for_appium():
    #app_path = os.path.dirname(__file__)
    app_path = r'D:\auto\python\app-autoApp\demoProject\apps\ApiDemos'
    PATH = lambda p: os.path.abspath(
        os.path.join(app_path, p)
    )
    
    desired_capabilities = {}
    desired_capabilities['platformName'] = 'Android'
    desired_capabilities['platformVersion'] = '4.4.2'
    desired_capabilities['deviceName'] = 'device'
    desired_capabilities['app'] = PATH("ApiDemos-debug.apk")
    #desired_capabilities['appPackage'] = 'io.appium.android.apis'
    #desired_capabilities['appActivity'] = '.ApiDemos'
            
    
    try:
        # Initial connection
        MobileApp.Init("appium", desired_capabilities, server_path = r'E:\android-sdk\Appium')
        
        #  Start activity
        MobileApp.NavigateTo("io.appium.android.apis", ".view.DragAndDropDemo")    
        
        #
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/drag_dot_3")
        MobileElement.PressAndHold()
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/drag_dot_2")
        MobileElement.MoveTo()
        time.sleep(2)
        MobileElement.ReleasePress()
        
        MobileApp.NavigateTo("io.appium.android.apis", ".ApiDemos")
        (MobileElement.by,MobileElement.value) = ("ID","android:id/text1")
        MobileElement.ScrollDown()
        
        (MobileElement.by,MobileElement.value) = ("NAME","Views")
        MobileElement.Click()
        
        (MobileElement.by,MobileElement.value) = ("NAME","Controls")
        MobileElement.Click()
        
        (MobileElement.by,MobileElement.value) = ("ID","android:id/list")
        MobileElement.Select("1. Light Theme")
        MobileApp.Back()    
        MobileElement.Set("1. Light Theme")
        print MobileApp.GetCurrentActivity();# 打印   u'.view.Controls1'
        
        (MobileElement.by,MobileElement.value) = ("ID","io.appium.android.apis:id/edit")
        MobileElement.TypeIn("Hello Android.")
        MobileElement.Set("Hello World!")
        
        print MobileElement.GetPageXML().encode("utf-8")
        print "edit is exist: ",MobileElement.IsExist()
        print "edit is visible: ",MobileElement.IsVisible()
        print "edit is enabled: ",MobileElement.IsEnabled()
        
        # 画个 笑脸
        MobileApp.NavigateTo("io.appium.android.apis", ".graphics.TouchPaint");# apidemos->Graphics->Touch Paint
        print MobileApp.GetCurrentActivity();# 打印   u'.graphics.TouchPaint'
        MobileElement.MultiDraw()
    except Exception,e:
        print "======================================end"
        print e
    finally:
        MobileApp.QuitApp()
        
if __name__ == "__main__":    
    usage_for_appium()
    
'''