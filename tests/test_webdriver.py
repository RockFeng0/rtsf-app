#! python3
# -*- encoding: utf-8 -*-


import appuidriver as webdriver
from appuidriver import Cap, utils

# 开启服务器，命令行:  appium server --allow-cors
appium_server_url = 'http://localhost:4723'

android_info = utils.android.detect_info()
pkg_info = utils.android.current_activity()
print("package info:", pkg_info.package, pkg_info.activity)

cap = Cap().android.with_pkg(
    package="com.android.settings",
    activity=".Settings"
)

print("capabilities info:", cap.to_json())
driver = webdriver.Remote(appium_server_url, cap.to_dict())

elm = driver.until_find.element_by_android_uiautomation('new UiSelector().text("Wi‑Fi")')
elm.click()

elm = driver.until_find.element_by_xpath('//android.widget.ImageButton[@content-desc="Menu"]')
elm.click()
driver.quit()

