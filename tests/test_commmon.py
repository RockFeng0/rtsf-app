#! python3
# -*- encoding: utf-8 -*-


import appuidriver
from appuidriver.utils import android
from appuidriver import MobileDesiredCapabilities


appium_server_url = 'http://localhost:4723'
# print(android.current_activity())
capabilities = MobileDesiredCapabilities.ANDROID.pkg(
    package="com.cmcc.hebao",
    activity="com.cmcc.wallet.mocam.activity.home.WalletHomeActivity"
).to_dict()


driver = appuidriver.Remote(appium_server_url, capabilities)
