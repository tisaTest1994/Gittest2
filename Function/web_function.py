from Function.web_common_function import *
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
        driver = WebChrome(executable_path=path + "/../Resource/chromedriver", chrome_options=options)
        driver.get(url)
        return driver

    # 登录 salesforce
    @staticmethod
    def login_salesforce(driver, account=get_json()['caas'][get_json()['env']]['account'], password=get_json()['caas'][get_json()['env']]['password']):
        if not check_web(driver=driver, text='logo'):
            assert False, '登录失败，未获取到输入账号页面'
        else:
            # 输入账号
            driver.find_element_by_id('username').clear()
            driver.find_element_by_id("username").send_keys(get_json()['caas'][get_json()['env']]['account'])
            # 输入密码
            driver.find_element_by_id('password').clear()
            driver.find_element_by_id("password").send_keys(get_json()['caas'][get_json()['env']]['password'])
            # 点击登录
            driver.find_element_by_id('Login').click()
            # 检查登录完成
            if not check_web(driver=driver, text='oneHeader'):
                assert False, '登录失败，没到主页'

    # 登录 web
    @staticmethod
    def login_web(driver, account=get_json()['caas'][get_json()['env']]['account'], password=get_json()['caas'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert driver.find_element_by_class_name('css-cedp0x').is_displayed(), '未打开登录页面'
        with allure.step("输入账号"):
            driver.find_element_by_id('username').clear()
            driver.find_element_by_id("username").send_keys(account)
        with allure.step("输入密码"):
            driver.find_element_by_id('password').clear()
            driver.find_element_by_id("password").send_keys(password)
        with allure.step("判断sign in 可被点击并且点击"):
            assert driver.find_element_by_class_name('css-c43lv').is_enabled(), 'sign in 可被点击'
            driver.find_element_by_class_name('css-c43lv').click()