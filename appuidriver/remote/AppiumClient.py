# -*- encoding: utf-8 -*-
'''
Current module: pyrunner.drivers.uiappium.AppiumClient

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:    lkf20031988@163.com
    RCS:      rock4.softtest.pad.uiappium.AppiumClient,v 2.0 2017年2月7日
    FROM:   2017年2月3日
********************************************************************

======================================================================

UI and Web Http automation frame for python.

'''

from appium import webdriver
from multiprocessing import Pool,freeze_support
   

class RunPool:
    @classmethod
    def Start(cls,callable_function,drivers):
        #freeze_support()
        pool = Pool(len(drivers))
        # for i in executers:
            # result = pool.apply_async(runnCase, args=(params,));#异步
            # print result.get()
        pool.map(callable_function, drivers.items());#并行
        pool.close()
        pool.join()
        
class AppiumClient:
    
    def __init__(self):
        self.__caps = {}
        self.__devs = {}
            
    def set_desired_capabilities(self,desired, port = 4725):
        '''
        Paramerter:
            desired    --> the value is form getAndroidDeviceDesiredInfo()
            port       --> the same value with AppiumServer's port
        Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_desired_capabilities()
            print a.get_desired_devices()
        '''
        devices = desired.get("devices")
        cap = desired.get("capabilities")
        caps = {}
        devs = {}
        for device in devices:
            device_id = device.pop('id',None)
            if device_id:
                devs[device_id] = device
                
                actual_cap = cap.copy()                
                actual_cap["deviceName"],actual_cap["platformVersion"] = device.get('id'),device.get('android_version')
                actual_cap["tmp_executer"] = "http://localhost:%d/wd/hub" %port
                caps[device_id] = actual_cap
                port += 1
        self.__caps = caps 
        self.__devs = devs       
    
    def get_desired_capabilities(self):
        return self.__caps
    
    def get_desired_devices(self):
        return self.__devs
        
    def get_remote_driver(self,device_id):
        ''' Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_remote_driver("127.0.0.1:6555")
        '''
        self.__generate_remote_drivers(device_id)
        return self.__drivers.get(device_id)
    
    def get_remote_drivers(self):
        ''' Usage:
            desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
            a=AppiumClient()
            a.set_desired_capabilities(desired)
            print a.get_remote_drivers()
        '''
        self.__generate_remote_drivers()
        return self.__drivers
    
    def __generate_remote_drivers(self, device_id=None):
        ''' Generate remote drivers with desired capabilities(self.__caps)
        Only this divice_id's driver will be generated if specified the device_id.        
        '''
        drivers = {}
        caps = self.__caps
        
        if device_id:
            cap = self.__caps.get(device_id)
            if not cap:
                self.__drivers = drivers
                return
            else:
                caps = {device_id:cap}            
            
        for devid,cap in caps.items():
            command_executor=cap.pop("tmp_executer",None)
            try:
                driver = None
                driver = webdriver.Remote(command_executor,cap)
            except Exception,e:                
                print "--->Waring: %s[%s] %s" %(self.__devs[devid]["model"], devid, e)        
            
            if driver:
                drivers[devid] = driver
        self.__drivers = drivers

### 示例  一
def simple_example_1():
    import time
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    driver = client.get_remote_driver("127.0.0.1:6555")
    
    time.sleep(5)
    driver.find_elements('name',"NFC")[0].click()
    time.sleep(5)
    driver.quit()

### 示例 二
def case(driver_raw):
    import time
    devid,driver = driver_raw[0],driver_raw[1]
    print "!!! %s" %devid
    time.sleep(5)
    driver.find_elements('name',"NFC")[0].click()
    time.sleep(5)
    driver.quit()
        
def simple_example_2():
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    drivers = client.get_remote_drivers()
    RunPool.Start(case,drivers)   
    
### 示例 三
def case2(driver_raw):
    import time
    from rock4.common import p_env
    from actions import MobileApp,MobileElement as App 
    devid,p_env.MOBILE = driver_raw[0],driver_raw[1]
    print "!!! %s-%s" %(devid,p_env.MOBILE)
    
    (App.by,App.value) = ("ID","android:id/text1")
    App.ScrollDown()
    time.sleep(5)
    (App.by,App.value) = ("NAME","Views")
    App.Click()
    time.sleep(5)
    (App.by,App.value) = ("NAME","Controls")
    App.Click()
    time.sleep(5)
    MobileApp.QuitApp()
        
def simple_example_3():    
    desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
    client = AppiumClient()
    client.set_desired_capabilities(desired)    
    drivers = client.get_remote_drivers()
    RunPool.Start(case2,drivers)
      
if __name__ == "__main__":    
#     desired = getAndroidDeviceDesiredInfo(r"D:\auto\python\app-autoApp\demoProject\apps\ApiDemos\ApiDemos-debug.apk")
#     a=AppiumClient()
#     a.set_desired_capabilities(desired)
#     print a.get_desired_capabilities()
#     print a.get_desired_devices()

#     desired = getAndroidDeviceDesiredInfo()
#     print desired
    simple_example_1()
