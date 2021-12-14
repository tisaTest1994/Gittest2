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

    @staticmethod
    def login_web(driver, account=get_json()['web'][get_json()['env']]['account'], password=get_json()['web'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert driver.find_element_by_id('signinForm').is_displayed(), '未打开登录页面'
        with allure.step("输入账号"):
            driver.find_element_by_id('username').clear()
            driver.find_element_by_id("username").send_keys(account)
        with allure.step("输入密码"):
            driver.find_element_by_id('sign_password_input').clear()
            driver.find_element_by_id("sign_password_input").send_keys(password)
        with allure.step("判断sign in 可被点击并且点击"):
            assert driver.find_element_by_id('login_login').is_enabled()
            driver.find_element_by_id('login_login').click()
            sleep(2)
        with allure.step("确定已经登录成功到assets页面"):
            assert driver.find_element_by_xpath('//*[@class="MuiBox-root css-i9gxme"]').is_displayed(), '已经成功登录'
            sleep(2)

    # 登出 web
    @staticmethod
    def logout_web(driver):
        with allure.step("判断在首页"):
            driver.find_element_by_class_name('css-1geb7my').is_displayed()
        with allure.step("点击登出"):
            driver.find_element_by_class_name('css-1rnrzb1').click()





