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

from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import os,time

class App(object):
    driver = None    
    
    @staticmethod
    def LaunchApp():
        ''' use current session to launch and active the app'''        
        App.driver.launch_app()
        
    @staticmethod
    def StartActivity(app_package ,app_activity):
        ''' Only support android.  start an activity and focus to it
        @param app_package: app package name
        @param app_activity: activity name you want to focus to        
        '''
        App.driver.start_activity(app_package,app_activity)
    
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
            App.driver.switch_to.context(None)
        except:
            return False
        
    @staticmethod
    def SwitchToNewContext(context_name):
        try:
            WebDriverWait(App.driver, 10).until(lambda driver: getattr(driver,"switch_to.context")(context_name))          
        except:            
            print("Waring: Timeout at %d seconds.Context %s was not found." %context_name)
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
        
          
                
        
class MobileApp():    
    
        
    @classmethod
    def IsAppInstalled(cls,app_package):
        return getattr(p_env.MOBILE,"is_app_installed")(app_package)
            
    @classmethod
    def InstallApp(cls,app_abs_path):
        ''' install the app to mobile
        app_abs_path=r"c:\test.apk"        
        '''
        # // todo
        return getattr(p_env.MOBILE,"is_app_installed")(app_abs_path)
        
    
    @classmethod
    def GetCurrentContext(cls):        
        return getattr(p_env.MOBILE,"current_context")
    
    @classmethod
    def GetCurrentContexts(cls):        
        return getattr(p_env.MOBILE,"contexts")
    
    @classmethod
    def GetCurrentActivity(cls):        
        return getattr(p_env.MOBILE,"current_activity")
    
    @classmethod
    def GetAppString(cls):        
        return getattr(p_env.MOBILE,"app_strings")()
            
    
    
    @classmethod
    def Keyevent(cls,key_code_name):
        getattr(p_env.MOBILE,"keyevent")(key_code_name)
        
    
        
    @classmethod
    def Swipe(cls, startx, starty, endx, endy,duration=None):
        ''' 模拟用户滑动 '''
        getattr(p_env.MOBILE,"swipe'")(startx,starty,endx,endy,duration)
    
    @classmethod
    def SwipeLeft(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/4*3, height / 2, width / 4 *1, height / 2, 500)
            time.sleep(1)
    
    @classmethod
    def SwipeRight(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/4*1, height / 2, width / 4 *3, height / 2, 500)
            time.sleep(1)
    
    @classmethod
    def SwipeUp(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/2, height/4*3, width /2, height/4*1, 500)
            time.sleep(1)
            
    @classmethod
    def SwipeDown(cls,times):
        driver = p_env.MOBILE        
        width = driver.get_window_size()["width"]
        height = driver.get_window_size()["height"]
        for i in range(times):
            driver.swipe(width/2, height/4*1, width /2, height/4*3, 500)
            time.sleep(1)
                        
    @classmethod
    def Tap(cls,positions,duration=None):
        ''' 模拟用户点击 '''
        getattr(p_env.MOBILE,"tap'")(positions,duration)
         
    
            
    
    
class MobileElement():
    ''' Mobile App Element Test.(need appium API>=17)'''
    (by, value) = (None, None)
    (index,timeout) = (0,10)
    __glob = {}
    
    @classmethod
    def SetVar(cls, name, value):
        ''' set static value
        :param name: glob parameter name
        :param value: parameter value
        '''
        cls.__glob.update({name:value})
                
    @classmethod
    def GetVar(cls, name):
        return cls.__glob.get(name)
    
    @classmethod
    def TimeSleep(cls,seconds):
        time.sleep(seconds)
        
    @classmethod
    def GetElement(cls):
        element = None
        try:
            element = cls.__wait()
        except Exception,e:
            print e
        finally:
            return element
    
    @classmethod
    def Set(cls, value):
        if value == "":
            return
        
        if value == "SET_EMPTY":
            value = ""
                
        element = cls.__wait()
        
        if element.tag_name == "android.widget.ListView":
            cls.Select(value)        
        else:
            element.clear()
            action = ActionChains(p_env.MOBILE)
            action.send_keys_to_element(element, value)            
            action.perform()
            
            cls.__clearup()
    
    @classmethod
    def Select(cls, value):
        if value == "":
            return
                
        element = cls.__wait()        
        #### ListView ################
        if element.tag_name == "android.widget.ListView":
            elms = element.find_elements_by_name(value)            
            if elms:
                elms[0].click()
                        
        #### NOT Supported ################
        else:
            print "Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, element.tag_name)
        cls.__clearup()
    
    @classmethod
    def TypeIn(cls, value):
        '''
        input value without clear existed values
        '''
        if value == "": return
                
        element = cls.__wait()        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, value)
        action.perform()
        
        cls.__clearup()
        
    @classmethod
    def SelectByOrder(cls, order):
        if order == "":
            return
        
        order = int(order)
        
        element = cls.__wait()
        
        #### ListView ################
        if element.tag_name == "android.widget.ListView":
            elms = getattr(p_env.MOBILE,"find_elements")("xpath", "//android.widget.ListView[%s]/*" %(cls.index))
            
            if elms and order<len(elms):
                elms[order].click()
                        
        #### NOT Supported ################
        else:
            print "Element [%s]: Tag Name [%s] Not Support [Select]." % (cls.__name__, element.tag_name)
        cls.__clearup()
  
    @classmethod
    def ScrollDown(cls):
        ''' 
        Sample usage:
        (by,value)=(By.XPATH,"//android.widget.TextView")
        ScrollDown()
        '''
        cls.__wait()
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)        
        getattr(p_env.MOBILE,"scroll")(elements[len(elements)-1], elements[0])        
        cls.__clearup()
    
    @classmethod
    def ScrollUp(cls):
        '''
        Sample usage:
        (by,value)=(By.XPATH,"//android.widget.TextView")
        ScrollUp()
        '''
        cls.__wait()
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)        
        getattr(p_env.MOBILE,"scroll")(elements[0],elements[len(elements)-1])        
        cls.__clearup()
    
    @classmethod
    def Click(cls):
        element = cls.__wait()        
        element.click()
        cls.__clearup()
   
    @classmethod
    def LongPress(cls):
        element = cls.__wait()   
        action = TouchAction(p_env.MOBILE)
        action.long_press(element)
        action.perform()        
        cls.__clearup()
    
    @classmethod
    def PressAndHold(cls):        
        element = cls.__wait()
        action = TouchAction(p_env.MOBILE)
        action.press(element)
        action.perform()        
        cls.__clearup()    
    @classmethod
    def MoveTo(cls):
        
        element = cls.__wait()
        action = TouchAction(p_env.MOBILE)
        action.move_to(element)
        action.perform()
        cls.__clearup()    
    
    @classmethod        
    def ReleasePress(cls):
        action = TouchAction(p_env.MOBILE)
        action.release()
        action.perform()
                
    @classmethod
    def MultiDraw(cls):
        e1 = TouchAction()
        e1.press(x=150, y=100).release()

        e2 = TouchAction()
        e2.press(x=250, y=100).release()

        smile = TouchAction()
        smile.press(x=110, y=200).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=2, y=1)
#         smile.press(x=110, y=200).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=1, y=1).move_to(x=2, y=1).move_to(x=2, y=1).\
#             move_to(x=2, y=1).move_to(x=2, y=1).move_to(x=2, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=3, y=1).move_to(x=4, y=1).\
#             move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=4, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).move_to(x=5, y=1).\
#             move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=0).move_to(x=5, y=-1).\
#             move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=5, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).move_to(x=4, y=-1).\
#             move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=3, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).move_to(x=2, y=-1).\
#             move_to(x=2, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1).move_to(x=1, y=-1)
        smile.release()

        ma = MultiAction(p_env.MOBILE)
        ma.add(e1, e2, smile)
        ma.perform()
        
    @classmethod
    def SendEnter(cls):
        element = cls.__wait()        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, Keys.ENTER)
        action.perform()        
        cls.__clearup()
    
    @classmethod
    def GetFocus(cls):
        
        element = cls.__wait()   
        element.send_keys(Keys.NULL)        
        action = ActionChains(p_env.MOBILE)
        action.send_keys_to_element(element, Keys.NULL)
        action.perform()        
        cls.__clearup()    
    
    @classmethod
    def GetObjectsCount(cls):        
        cls.__wait_for_appearing()        
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)
        cls.__clearup()
        return len(elements)
        
    
        
    @classmethod
    def GetAttribute(cls, attr):        
        element = cls.__wait()        
        attr_value = element.get_attribute(attr)        
        cls.__clearup()
        return attr_value
                        
    @classmethod
    def WaitForAppearing(cls):
        result = cls.__wait_for_appearing()
        cls.__clearup()
        return result
           
    @classmethod
    def WaitForDisappearing(cls):
        result = cls.__wait_for_disappearing()
        cls.__clearup()
        return result
    
    @classmethod
    def WaitForVisible(cls):
        element = cls.__wait()
        result = element.is_displayed()
        cls.__clearup()
        return result
        
    @classmethod
    def IsEnabled(cls):
        element = cls.__wait()        
        if element.is_enabled():
            cls.__clearup()
            return True
        else:
            cls.__clearup()
            return False    
    
    @classmethod
    def IsExist(cls): 
        elements = getattr(p_env.MOBILE,"find_elements")(cls.by, cls.value)
        cls.__clearup()        
        if len(elements) > 0:
            return True
        else:
            return False
    
    @classmethod
    def IsVisible(cls):
        element = cls.__wait()
        if element.is_displayed():
            cls.__clearup()
            return True
        else:
            cls.__clearup()
            return False
          
    @classmethod
    def __wait(cls):
        if not cls.__is_selector():
            raise Exception("Invalid selector[%s]." %cls.by)
            
        driver = p_env.MOBILE
        try:            
            elements = WebDriverWait(driver, cls.timeout).until(lambda driver: getattr(driver,"find_elements")(cls.by, cls.value))
        except:            
            raise Exception("Timeout at %d seconds.Element(%s) not found." %(cls.timeout,cls.value))
        
        if len(elements) < cls.index + 1:                    
            raise Exception("Element [%s]: Element Index Issue! There are [%s] Elements! Index=[%s]" % (cls.__name__, len(elements), cls.index))
        
        if len(elements) > 1:              
            print "Element [%s]: There are [%d] elements, choosed index=%d" %(cls.__name__,len(elements),cls.index)
            
        return elements[cls.index]
                
    @classmethod
    def __wait_for_disappearing(cls):
        try:
            if cls.__wait():
                return False
            return True
        except:
            return True
    
    @classmethod
    def __wait_for_appearing(cls):
        try:
            if cls.__wait():
                return True
            return False
        except:
            return False
    
    @classmethod
    def __is_selector(cls):
        all_By_selectors = ['CLASS_NAME', 'CSS_SELECTOR', 'ID', 'LINK_TEXT', 'NAME', 'PARTIAL_LINK_TEXT', 'TAG_NAME', 'XPATH']
        all_selectors = [By.CLASS_NAME, By.CSS_SELECTOR, By.ID, By.LINK_TEXT, By.NAME, By.PARTIAL_LINK_TEXT, By.TAG_NAME, By.XPATH]
        
        if cls.by in all_By_selectors:
            cls.by = getattr(By, cls.by)
            return True
        
        if cls.by in all_selectors:
            return True
        
        print "Warning: selector[%s] should be in %s" %(cls.by,all_By_selectors)
        return False
        
    @classmethod
    def __clearup(cls):
        if cls.index != 0:
            
            print "Element [%s]: The Operation Element Index = [%s]." % (cls.__name__, cls.index)
        
        cls.index = 0
    
    ''' Useless Functions
    @classmethod
    def VerifyExistence(cls, trueORfalse):        
        if trueORfalse == True:
            cls.__wait_for_appearing()
        else:
            cls.__wait_for_disappearing()
        
        
        
        cls.__clearup()
        if len(elements) > 0:
            if trueORfalse == True:
                print "pass,Exists!"
            else:
                print "fail,Exists!"
        else:
            if trueORfalse == False:
                print "pass,Not Exists!"
            else:
                print "fail,Not Exists!"
    
    
    @classmethod
    def VerifyEnabled(cls, trueOrfalse):
        
        
        element = cls.__wait()
        
        
        if element.is_enabled():
            if trueOrfalse == True:
                
                print "Pass"
            else:
                
                print "Fail"
        else:
            if trueOrfalse == True:
                
                print "Fail"
            else:
                
                print "Pass"
        
        cls.__clearup()
    
  
    @classmethod
    def VerifyAttribute(cls, attr, contain_content):
        if contain_content == "": return
        
        
        
        element = cls.__wait()
        
        attr_value = element.get_attribute(attr)
        
        if contain_content == attr_value:
            
            print "Real attr_value=[%s]" % attr_value
        else:
            
            "Real attr_value=[%s]" % attr_value
        cls.__clearup()
    
    
    @classmethod
    def VerifyAttributeContains(cls, attr, contain_content):
        if contain_content == "": return
        
        element = cls.__wait()
        
        attr_value = element.get_attribute(attr)
        
                
        if contain_content in attr_value:            
            print "Real attr_value=[%s]" % attr_value
        else:            
            print "Real attr_value=[%s]" % attr_value
        
        cls.__clearup()
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
    