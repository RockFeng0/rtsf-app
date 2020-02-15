#! python3
# -*- encoding: utf-8 -*-
'''
Current module: appuidriver.cli

Rough version history:
v1.0    Original version to use

********************************************************************
    @AUTHOR:  Administrator-Bruce Luo(罗科峰)
    MAIL:     luokefeng@163.com
    RCS:      appuidriver.cli,  v1.0 2018年9月18日
    FROM:   2018年9月18日
********************************************************************
======================================================================

Provide a function for the automation test

'''


import argparse
from rtsf.p_applog import color_print,logger
from rtsf.p_executer import TestRunner
from appuidriver.driver import LocalDriver, RemoteDriver
from appuidriver.remote.AppiumHatch import Android
from appuidriver.remote.AppiumJs import AppiumJs
from appuidriver.__about__ import __version__
    

def tools_main_run():
    parser = argparse.ArgumentParser(description="Get devices info and get apk info.")
        
    parser.add_argument(
        '--apk',
        help="apk file path.")
    
    parser.add_argument(
        '--adb', default = 'adb',
        help="set the `adb` path if ANDROID_HOME not configured. default: adb ")
    
    parser.add_argument(
        '--aapt', default = 'aapt',
        help="set the `aapt` path if ANDROID_HOME not configured. default: aapt ")
    
    color_print("appuidriver {}".format(__version__), "GREEN")
    
    args = parser.parse_args()    
    
    if args.apk:
        print(Android.gen_capabilities(apk_abs_path = args.apk, aapt_exe_4path = args.aapt))
    else:
        devices = Android.get_devices(args.adb)
        print(devices)
            
def appium_main_run():
    
    parser = argparse.ArgumentParser(description="appium server command line.")
    
    parser.add_argument(
        'address',
        help="appium server address, loopback address not suggest to use if grid mode.  e.g. 192.168.1.1:4723")
    
    parser.add_argument(
        '--device-name', 
        help="android device name. bind device to appium. e.g. HuaWei p10 plus")
    
    parser.add_argument(
        '--device-version', 
        help="android device platform version. bind device platform version to appium. e.g. 4.4.4")  
    
    parser.add_argument(
        '--hub-ip', 
        help="hub ip address in grid mode. register current appium to hub.")
    
    parser.add_argument(
        '--hub-port', type = int, default = 4444,
        help="hub port in grid mode. register current appium to hub. default: 4444")
    
    parser.add_argument(
        '--chromedriver-executable',
        help="ChromeDriver executable full path for webview. See https://github.com/appium/appium/blob/master/docs/en/writing-running-appium/web/chromedriver.md for more detail")
    
    color_print("appuidriver {}".format(__version__), "GREEN")
    
    args = parser.parse_args()    
    if len(args.address.split(":",1)) < 2:
        return "command parameter error."
    ip, port = args.address.split(":",1)
    server = AppiumJs(port = int(port))
    
    if args.chromedriver_executable:
        server.appium_cmd.extend(["--chromedriver-executable", args.chromedriver_executable])    
    
    if args.device_name:
        server.bind_device(device_id = args.device_name, platform_version = args.device_version)
    
    if args.hub_ip:
        server.node(ip, hub_address=(args.hub_ip, args.hub_port)).start_server()
        
    server.start_server()
    
def local_main_run():
    
    parser = argparse.ArgumentParser(description="Tools for web ui test. Base on rtsf.")
    
    parser.add_argument(
        'case_file', 
        help="yaml testcase file")
    
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    
    parser.add_argument(
        '--log-file',
        help="Write logs to specified file path.")
    
    
    parser.add_argument(
        '--package',
        help="app package name under test.")
    
    parser.add_argument(
        '--activity',
        help="app activity name. ")
    
    parser.add_argument(
        '--apk', 
        help="apk file path.")
    
    parser.add_argument(
        '--adb', default = 'adb',
        help="set the `adb` path if ANDROID_HOME not configured. default: adb ")
    
    parser.add_argument(
        '--aapt', default = 'aapt',
        help="set the `aapt` path if ANDROID_HOME not configured. default: aapt ")
        
    color_print("appuidriver {}".format(__version__), "GREEN")
    args = parser.parse_args()
    logger.setup_logger(args.log_level, args.log_file)
    
    result1 = True if args.apk else False
    result2 = True if args.package and args.activity else False
    if result1 or result2:
        LocalDriver._apk_abs_path  = args.apk
        LocalDriver._app_package   = args.package
        LocalDriver._app_activity  = args.activity
        LocalDriver._aapt_exe_path = args.adb
        LocalDriver._aapt_exe_path = args.aapt
        
        runner = TestRunner(runner = LocalDriver).run(args.case_file)
        html_report = runner.gen_html_report()
        color_print("report: {}".format(html_report))
    else:
        print("The parameter must include either an apk or package&activity.")
        return
    
def remote_main_run():
    
    parser = argparse.ArgumentParser(description="Tools for web ui test. Base on rtsf.")
    
    parser.add_argument(
        'case_file', 
        help="yaml testcase file")
    
    parser.add_argument(
        '--log-level', default='INFO',
        help="Specify logging level, default is INFO.")
    
    parser.add_argument(
        '--log-file',
        help="Write logs to specified file path.")
    
    
    parser.add_argument(
        '--package',
        help="app package name under test.")
    
    parser.add_argument(
        '--activity',
        help="app activity name.")
    
    parser.add_argument(
        '--apk',
        help="apk file path.")
        
    parser.add_argument(
        '--aapt', default = 'aapt',
        help="set the `aapt` path if ANDROID_HOME not configured. default: aapt ")
    
    parser.add_argument(
        '--ip',default = "localhost",
        help="remote hub ip. default: localhost")
    
    parser.add_argument(
        '--port', type = int, default = 4444,
        help="remote hub port. default: 4444")
    
    color_print("appuidriver {}".format(__version__), "GREEN")
    args = parser.parse_args()
    logger.setup_logger(args.log_level, args.log_file)    
    
    result1 = True if args.apk else False
    result2 = True if args.package and args.activity else False
    if result1 or result2:
        RemoteDriver._apk_abs_path  = args.apk
        RemoteDriver._app_package   = args.package
        RemoteDriver._app_activity  = args.activity
        RemoteDriver._aapt_exe_path = args.aapt
        RemoteDriver._remote_ip = args.ip
        RemoteDriver._remote_port = args.port
        
        runner = TestRunner(runner = RemoteDriver).run(args.case_file)
        html_report = runner.gen_html_report()
        color_print("report: {}".format(html_report))
    else:
        print("The parameter must include either an apk or package&activity.")
        return
    
    
    
    
    
    
