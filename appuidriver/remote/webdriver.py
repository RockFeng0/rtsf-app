#! python3
# -*- encoding: utf-8 -*-

from appuidriver.remote.appium_wait_until import AppiumWaitUntil
from appium.webdriver import Remote


class WebDriver(Remote, AppiumWaitUntil):
    def __init__(self, *args, **kwargs):
        Remote.__init__(self, *args, **kwargs)
        AppiumWaitUntil.__init__(self)

