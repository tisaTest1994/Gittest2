from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


class UiFunction:

    @staticmethod
    def login(account, password):
        UiFunction.logout(account)
        sleep(5)
        assert poco('Move your 1st step towards digital assets with Cabital').exists(), "没到注册登录页面"
        poco('Log In').click()
        assert poco('Welcome Back').exists(), "没到输入密码界面"
        poco(text='Account').click()
        text(account)
        poco(text='Password').click()
        text(password)
        poco('Login').click()
        sleep(5)

    @staticmethod
    def logout(account):
        if poco('Splash').exists():
            sleep(5)
        if poco('Portfolio').exists():
            poco('Portfolio').click()
            if poco(account).exists():
                poco(account).click()
            else:
                click(0.36, 0.025)
            poco('退出登录').click()

