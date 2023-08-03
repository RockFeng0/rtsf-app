#! python3
# -*- encoding: utf-8 -*-


""" Selenium Grid
    # 在主机上运行（hub）以下命令，启动服务, 默认是4444端口，可以使用参数 -p 4444
    java -jar selenium-server-4.4.0.jar hub
    # 在从机上运行（node）以下命令，启动从机服务
    java -jar selenium-server-4.4.0.jar node --hub 10.1.5.212
    # 如果想在主机上也开一个node，则执行以下命令
    java -jar selenium-server-4.4.0.jar node
"""


import appuidriver as webdriver
from appuidriver import Cap, utils
from appium.webdriver.common.appiumby import AppiumBy


appium_server_url = 'http://localhost:4723'

android_info = utils.android.detect_info()
pkg_info = utils.android.current_activity()
print("package info:", pkg_info.package, pkg_info.activity)

cap = Cap.android.with_pkg(
    package="com.cmcc.hebao",
    activity="com.cmcc.wallet.mocam.activity.home.WalletHomeActivity"
)

print("capabilities info:", cap.to_json())

driver = webdriver.Remote(appium_server_url, cap.to_dict())
driver.find_element(AppiumBy.ACCESSIBILITY_ID)



