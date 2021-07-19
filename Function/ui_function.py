from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


class UiFunction:

    # 点击
    @staticmethod
    def click(text):
        wait(poco(text), timeout=20, interval=0.5, intervlfunc=None)
        poco(text).click()

    @staticmethod
    def login(account, password):
        poco('Log In').click()
        sleep(2)
        assert poco('Welcome Back').exists(), "没到输入密码界面"
        poco(text='Account').click()
        text(account, enter=False)
        sleep(2)
        poco(text='Password').click()
        text(password)
        sleep(2)
        poco('Log In').click()

