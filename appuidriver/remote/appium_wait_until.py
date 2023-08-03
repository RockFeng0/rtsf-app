#! python3
# -*- encoding: utf-8 -*-


from webuidriver.remote.wait_until import WaitUntil, UntilFind
from appium.webdriver.common.appiumby import AppiumBy


class AppiumWaitUntil(WaitUntil):

    def __init__(self):
        WaitUntil.__init__(self)
        self._until_find = AppiumUntilFind(self)

    @property
    def until_find(self):
        """
        :Returns:
            - UntilFind: an object containing all options for dynamically waiting and finding elements.

        :Usage:
            element = driver.until_find.element_by_id('#username')
            element.send_keys("admin")
        """
        return self._until_find


class AppiumUntilFind(UntilFind):
    LOC = list(UntilFind.LOC)
    LOC.extend([
        AppiumBy.IOS_PREDICATE,
        AppiumBy.IOS_UIAUTOMATION,
        AppiumBy.IOS_CLASS_CHAIN,
        AppiumBy.ANDROID_UIAUTOMATOR,
        AppiumBy.ANDROID_VIEWTAG,
        AppiumBy.ANDROID_DATA_MATCHER,
        AppiumBy.ANDROID_VIEW_MATCHER
    ])

    def __init__(self, driver):
        UntilFind.__init__(self, driver)

        self._driver = driver
        self.element_by_ios_predicate = self._element(AppiumBy.IOS_PREDICATE)
        self.element_by_ios_uiautomation = self._element(AppiumBy.IOS_UIAUTOMATION)
        self.element_by_ios_class_chain = self._element(AppiumBy.IOS_CLASS_CHAIN)
        self.element_by_android_uiautomation = self._element(AppiumBy.ANDROID_UIAUTOMATOR)
        self.element_by_android_viewtag = self._element(AppiumBy.ANDROID_VIEWTAG)
        self.element_by_android_datamatcher = self._element(AppiumBy.ANDROID_DATA_MATCHER)
        self.element_by_android_viewmatcher = self._element(AppiumBy.ANDROID_VIEW_MATCHER)

        self.elements_by_ios_predicate = self._element(AppiumBy.IOS_PREDICATE)
        self.elements_by_ios_uiautomation = self._element(AppiumBy.IOS_UIAUTOMATION)
        self.elements_by_ios_class_chain = self._element(AppiumBy.IOS_CLASS_CHAIN)
        self.elements_by_android_uiautomation = self._element(AppiumBy.ANDROID_UIAUTOMATOR)
        self.elements_by_android_viewtag = self._element(AppiumBy.ANDROID_VIEWTAG)
        self.elements_by_android_datamatcher = self._element(AppiumBy.ANDROID_DATA_MATCHER)
        self.elements_by_android_viewmatcher = self._element(AppiumBy.ANDROID_VIEW_MATCHER)
