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

from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
from appium.webdriver.common.mobileby import MobileBy

from webuidriver.actions import Web, WebActions, WebContext, WebElement, WebVerify, WebWait


class App(Web):
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
    def Shake():
        ''' 模拟设备摇晃 '''
        App.driver.shake()            
    
    @staticmethod
    def Lock(seconds):
        ''' Lock the device for a certain period of time. iOS only '''
        App.driver.lock(seconds)
    
    @staticmethod
    def BackgroundApp(seconds):
        '''应用会被放到后台特定时间,然后应用会重新回到前台 '''        
        App.driver.background_app(seconds)
    
    @staticmethod
    def OpenNotifications():
        ''' 打开通知栏 '''
        App.driver.open_notifications()        
            
    @staticmethod
    def RemoveApp(app_package):
        ''' 卸载app '''
        App.driver.remove_app(app_package)
        
            
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
        
class AppElement(WebElement):
        
    @classmethod
    def _is_selector(cls):
        '''
        override method
        @note:  MobileBy.ANDROID_UIAUTOMATOR   e.g.
            driver.find_elements_by_android_uiautomator('text("Views")');  driver.find_elements_by_android_uiautomator('new UiSelector().text("Views")')
            
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
        by = ('CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'NAME', 'PARTIAL_LINK_TEXT', 'TAG_NAME', 'XPATH')
        mobile_by = ('ACCESSIBILITY_ID', 'ANDROID_UIAUTOMATOR', 'IMAGE', 'IOS_CLASS_CHAIN', 'IOS_PREDICATE', 'IOS_UIAUTOMATION')
        all_selectors = (getattr(MobileBy, i) for i in by + mobile_by)
                        
        if cls._control["by"] in all_selectors:
            return True
        
        print("Warning: selector[%s] should be in %s" %(cls._control["by"],all_selectors))
        return False
               
                
class AppContext(WebContext, AppElement):  
    
    @classmethod
    def DyActivityData(cls,name):
        cls.glob.update({name:App.driver.current_activity})
    
    @classmethod
    def DyPackageData(cls,name):
        cls.glob.update({name:App.driver.current_package})
                
    
         
class AppWait(WebWait, AppElement):    
    pass

class AppVerify(WebVerify, AppElement):    
    
    @classmethod
    def VerifyAppInstalled(cls,app_package):
        return App.driver.is_app_installed(app_package)
    
    @classmethod
    def VerifyCurrentActivity(cls, app_activity):        
        if App.driver.current_activity == app_activity:
            return True
        else:
            return False      
                    
class AppTouchAction(AppElement):
    
    @classmethod
    def Tap(cls):
        try:
            TouchAction(App.driver).tap(cls._element()).perform()
        except:
            return False
    
    @classmethod
    def LongPress(cls):
        try:
            TouchAction(App.driver).long_press(cls._element()).perform()
        except:
            return False
            
    @classmethod
    def Press(cls):
        try:
            TouchAction(App.driver).press(cls._element()).perform()
        except:
            return False   
            
    @classmethod
    def MoveTo(cls):
        try:
            TouchAction(App.driver).move_to(cls._element()).perform()
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
            action1 = TouchAction(App.driver).press(x=150, y=275).release()
            action2 = TouchAction(App.driver).press(x=550, y=275).release()            
            action3 = TouchAction(App.driver).press(x=150, y=475).move_to(x=250, y=500).move_to(x=350, y=525).move_to(x=450, y=500).move_to(x=550, y=475).release()
            m_action = MultiAction(App.driver)
            m_action.add(action1, action2, action3)
            m_action.perform()
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
            
class AppActions(WebActions, AppElement):
    
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
    
    ####  inherit selenium's methods
    @classmethod
    def SendKeys(cls, value):
        '''
        @param value: 文本框，输入的文本
        '''
        if value == "":
            return
        try:
            element = cls._element()
            element.clear()        
            element.send_keys(value)
        except:
            return False
    
    @classmethod
    def Click(cls):
        ''' 左键 点击 1次   '''
        try:
            cls._element().click()
        except:
            return False
        