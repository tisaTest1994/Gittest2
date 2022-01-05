from Function.web_common_function import *
import platform
import allure
import os


class webFunction:

    @staticmethod
    def launch_web(url):

        # os.path.abspath()获得绝对路径
        path = os.path.abspath(os.path.dirname(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')

        # 指定浏览器的分辨率
        options.add_argument('--window-size=1920,1080')
        # 无界面运行
        # options.add_argument('--headless')
        # 判断运行环境
        if 'mac' in str(platform.platform()):
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_mac", chrome_options=options)
        else:
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_liunx", chrome_options=options)
        driver.get(url)
        return driver

    @staticmethod
    def login_web(driver, account=get_json()['web'][get_json()['env']]['account'], password=get_json()['web'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert check_web(driver, 'loginPage', 'signinForm'), '未打开登录页面'
        with allure.step("输入账号"):
            operate_element(driver, 'loginPage', 'username', type='clean')
            operate_element(driver, 'loginPage', 'username', type='input', input=account)
        with allure.step("输入密码"):
            operate_element(driver, 'loginPage', 'sign_password_input', type='clean')
            operate_element(driver, 'loginPage', 'sign_password_input', type='input', input=password)
        with allure.step("点击sign in"):
            operate_element(driver, 'loginPage', 'login_login')
            sleep(2)
        with allure.step("确定已经登录成功到首页"):
            assert check_web(driver, 'assetPage', 'Cabital Logo'), '已经成功登录'
            sleep(2)

    # 登出 web
    @staticmethod
    def logout_web(driver):
        with allure.step("点击登出"):
            operate_element(driver, 'assetPage', 'header-btn-hi-nickname')
            operate_element(driver, 'assetPage', 'header-btn-user-signout')





