from Function.web_function import *
from Function.api_function import *

global driver


class TestCassApi:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    @allure.testcase('test_cass_001 打开登录页面')
    def test_cass_001(self):
        with allure.step("launch web"):
            driver = webFunction.launch_web(self.web_url)
        with allure.step("确定选择最新的tab"):
            driver.switch_to_new_tab()
        with allure.step("确定打开登录页面"):
            assert driver.find_element_by_id('signinForm').is_displayed(), '未打开登录页面'
        with allure.step("输入账号"):
            driver.find_element_by_id('username').clear()
            driver.find_element_by_id("username").send_keys(get_json()['web'][get_json()['env']]['account'])
        with allure.step("输入密码"):
            driver.find_element_by_id('password').clear()
            driver.find_element_by_id("password").send_keys(get_json()['web'][get_json()['env']]['password'])
        with allure.step("判断sign in 可被点击并且点击"):
            assert driver.find_element_by_class_name('css-c43lv').is_enabled(), 'sign in 可被点击'
            driver.find_element_by_class_name('css-c43lv').click()
        sleep(2000)

