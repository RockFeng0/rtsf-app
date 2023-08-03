#! python3
# -*- encoding: utf-8 -*-

import os
import json
from selenium.webdriver import DesiredCapabilities


class _Capabilities:
    """ 全球公认的功能列表 """

    def __init__(self):
        self.capabilities = {
            'platformName': 'Android',  # The type of platform hosting the app or browser
            'appium:automationName': 'UiAutomator2',  # The name of the Appium driver to use

            'browserName': None,  # 手机端浏览器名称，如果是应用，则空值
            'appium:app': None,  # 安装包的绝对路径，如果指定了appActivity和appWaitPackage，Android则不需要此参数。与browserName不兼容
            'appium:deviceName': None,  # 手机型号类型
            'appium:platformVersion': None,  # 手机操作系统版本
            'appium:newCommandTimeout': 120000,  # 等待一条命令超时时间单位为秒
            'appium:noReset': False,  # 在当前session下不会重置应用状态，默认False
            'appium:fullReset': False,  # 重置应用(会删除应用数据，session结束后卸载),默认False
            'appium:eventTimings': False,  # Appium驱动收集事件计时，默认False
            'appium:printPageSourceOnFindFailure': False,  # 如果为true，则收集页面源代码，并在查找元素的请求失败时将其打印到Appium日志(默认为false)
        }

    def to_json(self):
        return json.dumps(self.capabilities)

    def to_dict(self):
        return self.capabilities


class _IOSCapabilities(object):
    """ Methods for ios system. """
    pass


class _AndroidCapabilities(_Capabilities):
    def __init__(self):
        _Capabilities.__init__(self)
        self.capabilities.update(
            {
                'appium:appPackage': None,
                'appium:appActivity': None,
                'appium:appWaitPackage': None,
                'appium:unicodeKeyboard': True,  # 支持中文输入; 如果Unicodekeyboard为true，那么在开始运行脚本的时候，会帮你安装appium自带的输入法，这个输入法是没有UI的
                'appium:resetKeyboard': True,  # 支持中文输入,两条都必须配置; 只有当你的用例是正常执行完毕，没被外界打断的情况下，而且resetkeyboard也为true的情况下，appium会帮你复原输入法
                'appium:udid': None,  # 绑定的设备ID
            }
        )
        # 剔除手机端浏览器参数(browserName)，该参数与APP应用参数（app、appPackage、appActivity） 不兼容
        self.capabilities.pop("browserName")

    def with_app(self, apk_abs_path):
        if os.path.isfile(apk_abs_path):
            self.capabilities["appium: app"] = apk_abs_path

        return self

    def with_pkg(self, package, activity):
        """
        from adbutils import adb
        print(adb.device().app_current())
        """
        self.capabilities["appium:appPackage"] = package
        self.capabilities["appium:appWaitPackage"] = activity
        self.capabilities["appium:appActivity"] = activity
        return self


class MobileDesiredCapabilities(DesiredCapabilities):
    android = _AndroidCapabilities()
    ios = _IOSCapabilities()


if __name__ == "__main__":
    android = MobileDesiredCapabilities.android
    print(android.to_dict())
    print(android.with_pkg("uk.co.aifactory.chessfree", "uk.co.aifactory.chessfree.ChessFreeActivity").to_json())
