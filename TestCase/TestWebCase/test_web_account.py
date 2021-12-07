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
            driver.find_element_by_id('sign_password_input').clear()
            driver.find_element_by_id("sign_password_input").send_keys(get_json()['web'][get_json()['env']]['password'])
        with allure.step("判断sign in 可被点击并且点击"):
            assert driver.find_element_by_id('login_login').is_enabled()
            driver.find_element_by_id('login_login').click()
        sleep(2000)

    def test_cass_002(self):
        with allure.step("launch web"):
            driver = webFunction.launch_web(self.web_url)
        with allure.step("确定选择最新的tab"):
            driver.switch_to_new_tab()
        with allure.step("确定打开登录页面"):
            assert driver.find_element_by_id('signinForm').is_displayed(), '未打开登录页面'
        with allure.step("点击Forget pwd"):
            driver.find_element_by_id('login_forgotpw').click()
        with allure.step("通过重置密码text校验"):
            assert driver.find_element_by_xpath('//*[@id="dialog_forgetpassword"]/h4').is_displayed(), '打开重置密码页面'
        with allure.step("清除Account"):
            driver.find_element_by_id('dialog_forgetpassword_email_input').clear()
        with allure.step("输入Account"):
            driver.find_element_by_id('dialog_forgetpassword_email_input').send_keys(get_json()['web'][get_json()['env']]['account'])
        with allure.step("输入验证码"):
            driver.find_element_by_xpath('//*[@name="mailcode"]').send_keys(get_json()['web'][get_json()['env']]['code'])
        with allure.step("输入密码"):
            driver.find_element_by_id('dialog_forgetpassword_email_input').send_keys(get_json()['web'][get_json()['env']]['newpassword'])
        with allure.step("判断Confirm 可被点击并且点击"):
            assert driver.find_element_by_id('dialog_forgetpassword_confirm').is_enabled()
            driver.find_element_by_id('dialog_forgetpassword_confirm').click()


