#! python3
# -*- encoding: utf-8 -*-
'''
Current module: appuidriver.driver

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      appuidriver.driver,  v1.0 2018年9月10日
    FROM:   2018年9月10日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import re
from rtsf.p_executer import Runner
from rtsf.p_common import CommonUtils,ModuleUtils,FileSystemUtils
from rtsf.p_exception import FunctionNotFound,VariableNotFound
from appuidriver.remote.AppiumHatch import Android
        
class _Driver(Runner):     
    def __init__(self, is_local_driver = True):
        super(_Driver,self).__init__()
        self._local_driver = is_local_driver
    
    def run_test(self, testcase_dict, variables, driver_map):
        fn, fn_driver = driver_map        
        parser = self.parser        
        tracer = self.tracers[fn]
        
        _Actions = ModuleUtils.get_imported_module("appuidriver.actions")
        _Actions.App.driver = _Actions.Web.driver = fn_driver
                            
        functions = {}
        app_functions = ModuleUtils.get_callable_class_method_names(_Actions.App)
        app_element_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppElement)
        app_context_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppContext)
        app_wait_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppWait)
        app_verify_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppVerify)
        app_touch_action_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppTouchAction)
        app_actions_functions = ModuleUtils.get_callable_class_method_names(_Actions.AppActions)
        functions.update(app_functions)
        functions.update(app_element_functions)
        functions.update(app_context_functions)
        functions.update(app_wait_functions)
        functions.update(app_verify_functions)
        functions.update(app_touch_action_functions)
        functions.update(app_actions_functions)
        parser.bind_functions(functions)
        
        _Actions.AppContext.glob.update(variables)
        parser.update_binded_variables(_Actions.AppContext.glob)        
         
        case_name = FileSystemUtils.get_legal_filename(parser.eval_content_with_bind_actions(testcase_dict["name"]))
        tracer.start(self.proj_info["module"], case_name, testcase_dict.get("responsible","Administrator"), testcase_dict.get("tester","Administrator"))        
        tracer.section(case_name)
        
        try:
            tracer.normal("**** bind glob variables")                
            glob_vars = parser.eval_content_with_bind_actions(testcase_dict.get("glob_var",{}))
            tracer.step("set global variables: {}".format(glob_vars))                
            _Actions.AppContext.glob.update(glob_vars)            
             
            tracer.normal("**** bind glob regular expression")
            globregx = {k: re.compile(v) for k,v in testcase_dict.get("glob_regx",{}).items()}
            tracer.step("set global regular: {}".format(globregx))            
            _Actions.AppContext.glob.update(globregx)
                             
            tracer.normal("**** precommand")
            precommand = testcase_dict.get("pre_command",[])    
            parser.eval_content_with_bind_actions(precommand)
            for i in precommand:
                tracer.step("{}".format(i))
             
            tracer.normal("**** steps")
            steps = testcase_dict["steps"]
            for step in steps:
                #print("---")
                if not "appdriver" in step:
                    continue
                
                if not step["appdriver"].get("action"):
                    raise KeyError("appdriver.action")            
                
                #print(step)
                if step["appdriver"].get("by"):
                    by = parser.eval_content_with_bind_actions(step["appdriver"].get("by"))
                    tracer.normal("preparing: by -> {}".format(by))
                    
                    value = parser.eval_content_with_bind_actions(step["appdriver"].get("value"))
                    tracer.normal("preparing: value -> {}".format(value))
                    
                    index = parser.eval_content_with_bind_actions(step["appdriver"].get("index", 0))
                    tracer.normal("preparing: index -> {}".format(index))
                    
                    timeout = parser.eval_content_with_bind_actions(step["appdriver"].get("timeout", 10))
                    tracer.normal("preparing: timeout -> {}".format(timeout))                           
                
                    prepare =parser.get_bind_function("SetControl")
                    prepare(by = by, value = value, index = index, timeout = timeout)
                                
                result = parser.eval_content_with_bind_actions(step["appdriver"]["action"])
                #print(":",result)           
                if result == False:
                    tracer.fail(step["appdriver"]["action"])
                else:
                    tracer.ok(step["appdriver"]["action"])
                        
            tracer.normal("**** postcommand")
            postcommand = testcase_dict.get("post_command", [])        
            parser.eval_content_with_bind_actions(postcommand)
            for i in postcommand:
                tracer.step("{}".format(i))
            
            tracer.normal("**** verify")
            verify = testcase_dict.get("verify",[])
            result = parser.eval_content_with_bind_actions(verify)
            for v, r in zip(verify,result):
                if r == False:
                    tracer.fail(u"{} --> {}".format(v,r))
                else:
                    tracer.ok(u"{} --> {}".format(v,r))
                        
        except KeyError as e:
            tracer.error("Can't find key[%s] in your testcase." %e)
        except FunctionNotFound as e:
            tracer.error(e)
        except VariableNotFound as e:
            tracer.error(e)
        except Exception as e:
            tracer.error("%s\t%s" %(e,CommonUtils.get_exception_error()))
        finally:
            #tracer.normal("globals:\n\t{}".format(parser._variables)) 
            tracer.stop()
        return tracer         

class LocalDriver(_Driver):
    ''' O-O one local pc that running one appium connect one devices '''
    
    _adb_exe_path = 'adb'
    _aapt_exe_path = 'aapt'
    _apk_abs_path = None
    _app_package = None
    _app_activity = None
        
    def __init__(self):
        super(LocalDriver,self).__init__(is_local_driver = True)
        desired_cap = Android.gen_capabilities(apk_abs_path = LocalDriver._apk_abs_path, app_package= LocalDriver._app_package, 
                                               app_activity=LocalDriver._app_activity,aapt_exe_4path = LocalDriver._aapt_exe_path)
        
        devices = Android.get_devices(LocalDriver._adb_exe_path)        
        device_id, properties = devices.popitem()
        desired_cap["deviceName"] = device_id
        desired_cap["platformVersion"] = properties.get('android_version')
        
        self._default_drivers = [("", Android.gen_remote_driver(executor = Android.get_executor("localhost", 4723), capabilities = desired_cap))]
        
        
class RemoteDriver(_Driver):
    ''' M-M some pc that running some appium connect some devices, each pc at most 20 devices '''
    _aapt_exe_path = 'aapt'
    _apk_abs_path = None
    _app_package = None
    _app_activity = None
    
    _remote_ip = "localhost"
    _remote_port = 4444
    
    def __init__(self):
        super(RemoteDriver,self).__init__(is_local_driver = False)
        desired_cap = Android.gen_capabilities(apk_abs_path = RemoteDriver._apk_abs_path, app_package= RemoteDriver._app_package, 
                                               app_activity=RemoteDriver._app_activity,aapt_exe_4path = RemoteDriver._aapt_exe_path)
        self._default_devices =[]
        self._default_drivers = []
        executors = Android.get_remote_executors(hub_ip = RemoteDriver._remote_ip, port = RemoteDriver._remote_port)
        for udid, udversion, executor in executors:
            fn = FileSystemUtils.get_legal_filename(executor)
            self._default_devices.append(fn)
            
            cap = desired_cap.copy()
            cap["deviceName"] = udid
            cap["platformVersion"] = udversion            
            self._default_drivers.append((fn, Android.gen_remote_driver(executor = executor, capabilities = cap)))
            
            