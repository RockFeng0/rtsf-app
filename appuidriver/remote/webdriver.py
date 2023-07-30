#! python3
# -*- encoding: utf-8 -*-


from webuidriver.remote.wait_until import WaitUntil
from appium.webdriver import Remote


class WebDriver(Remote, WaitUntil):
    def __init__(self, *args, **kwargs):
        Remote.__init__(self, *args, **kwargs)
        WaitUntil.__init__(self)

