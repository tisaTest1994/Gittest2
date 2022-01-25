import time

from Function.web_function import *
from Function.web_common_function import *


class TestWebLogin:
    # 获取测试网站url
    web_url = get_json()['web'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
        with allure.step("获取用户偏好设置"):
            r = session.request('GET', url='{}/preference/account/setting'.format(env_url), headers=headers)
            self.currency = r.json()['currency']
            headers['X-Currency'] = self.currency
        with allure.step("获得driver"):
            self.driver = webFunction.launch_web(self.web_url)

    def teardown_method(self):
        with allure.step("关闭driver"):
            self.driver.close()

    @allure.title('test_web_login_001 signup页面跳转')
    def test_login_001(self):
        # Sign up
        with allure.step("Sign Up注册页面跳转"):
            operate_element(self.driver, 'loginPage', "login_gotosignup")
            assert check_web(self.driver, 'signupPage', "signupForm"), '跳转Sign Up页面失败'

    @allure.title('test_web_login_001')
    @allure.description('signup邮箱规则校验')
    def test_signup_001(self):
        with allure.step("测试第一个字符为<>()[\]\\.,;:\s@\“字符的邮箱"):
            operate_element(self.driver, 'loginPage', "login_gotosignup")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "<>test@cabital.com")
            assert get_element_text(self.driver, "signupPage", "signup_form_password_email-helper-text") ==\
                   'Please enter a valid email address', "未显示邮箱格式错误或提示信息错误"
        with allure.step("如@后为[ ]内非4个一到三位数字且以.分割，如：test@[23.143.42.1234]"):
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "clear2")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "test@[23.143.42.1234]")
            assert get_element_text(self.driver, "signupPage", "signup_form_password_email-helper-text") == \
                   'Please enter a valid email address', "未显示邮箱格式错误或提示信息错误"
        with allure.step("如@后为大写字母，小写字母，“-”或数字，.后面不为2个或2个以上的大写字母或小写字母。如：test@qwe12.c 和test@DF-.a1"):
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "clear2")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "test@qwe12.c")
            assert get_element_text(self.driver, "signupPage", "signup_form_password_email-helper-text") == \
                   'Please enter a valid email address', "未显示邮箱格式错误或提示信息错误"
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "clear2")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "test@DF-.a1")
            assert get_element_text(self.driver, "signupPage", "signup_form_password_email-helper-text") == \
                   'Please enter a valid email address', "未显示邮箱格式错误或提示信息错误"
        with allure.step("邮箱含中文，如测试@163.com"):
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "clear2")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "测试@163.com")
            assert self.driver.find_element_by_xpath("//*[@id='signup_sendcode'][@tabindex='0']"), "send code显示状态错误"
        with allure.step("输入正确格式邮箱"):
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "clear2")
            operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "qwe@cabital.com")

            #assert self.driver.find_element_by_xpath("//*[@id='signup_sendcode'][@tabindex='0']"), "send code显示状态错误"

    @allure.title('test_web_signup_002')
    @allure.description('signup_send code')
    def test_signup_002(self):
        """注册账号用脚本跑账号不好管理，故不写注册部分脚本"""
        operate_element(self.driver, 'loginPage', "login_gotosignup")
        operate_element(self.driver, 'signupPage', "signup_form_password_email", "input", "qwe@cabital.com")
        with allure.step("点击send code,验证码输入框字符限制6位验证"):
            operate_element(self.driver, 'signupPage', "signup_sendcode", "click")
            operate_element(self.driver, 'signupPage', "mailcode", "input", "6666666")
            # 输入7个6，看value是否为6个6。
            assert self.driver.find_element_by_name("mailcode").get_attribute("value") == "666666", "验证码输入字符未限制"

    @allure.title('test_web_signup_003')
    @allure.description('密码显隐默认状态及设置密码')
    def test_signup_003(self):
        operate_element(self.driver, 'loginPage', "login_gotosignup")
        with allure.step("确定密码显隐默认状态"):
            # Password显隐默认不显示
            assert self.driver.find_element_by_xpath('//*[@id="signup_form_password_input"][@type= "password"]'),\
                "密码显隐默认状态错误"
        with allure.step("设置密码-正确密码格式"):
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "input", "Aaaa1234")
            assert self.driver.find_element_by_xpath('//*[@id="signupForm"]/div[4]/p'), "输入正确格式密码，提示信息未消失"
        with allure.step("错误密码格式1：密码设置位数少于8位"):
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "delete", cycle=8)
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "input", "Aaaa123")
            assert self.driver.find_element_by_xpath('//*[@id="signupForm"]/div[4]/p').text ==\
                   "Password must have at least 8 characters, 1 uppercase letter, 1 lowercase letter and 1 number.", "输入错误格式密码，提示信息未显示"
        with allure.step("错误密码格式2：含有非法字符"):
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "delete", cycle=8)
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "input", "你好中国!@#1")
            assert self.driver.find_element_by_xpath(
                '//*[@id="signupForm"]/div[4]/p').text == "Password must have at least 8 characters," \
                                                          " 1 uppercase letter, 1 lowercase letter and 1 number.",\
                "输入错误格式密码，提示信息未显示"
        with allure.step("错误密码格式3：没有大写或小写字母"):
            # 没有大写字母
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "delete", cycle=8)
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "input", "aaaa1234")
            assert self.driver.find_element_by_xpath(
                '//*[@id="signupForm"]/div[4]/p').text == "Password must have at least 8 characters," \
                                                          " 1 uppercase letter, 1 lowercase letter and 1 number.",\
                "输入错误格式密码，提示信息未显示"
            # 没有小写字母
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "delete", cycle=8)
            operate_element(self.driver, 'signupPage', "signup_form_password_input", "input", "AAAA1234")
            assert self.driver.find_element_by_xpath(
                '//*[@id="signupForm"]/div[4]/p').text == "Password must have at least 8 characters," \
                                                          " 1 uppercase letter, 1 lowercase letter and 1 number.",\
                "输入错误格式密码，提示信息未显示"
        with allure.step("密码显隐切换"):
            # 密码默认不显示，点击密码显隐按钮后密码显示
            operate_element(self.driver, 'signupPage', "MuiIconButton-edgeEnd", "click")
            assert self.driver.find_element_by_xpath('//*[@id="signup_form_password_input"][@type="text"]'),\
                "密码显隐默认状态错误"
            # 再次点击密码显隐按钮，密码隐藏
            operate_element(self.driver, 'signupPage', "MuiIconButton-edgeEnd", "click")
            assert self.driver.find_element_by_xpath('//*[@id="signup_form_password_input"][@type="password"]'),\
                "密码显隐默认状态错误"

    @allure.title('test_web_signup_004')
    @allure.description('协议条款复选框及条款信息检查')
    def test_signup_004(self):
        operate_element(self.driver, 'loginPage', "login_gotosignup")
        with allure.step("点击协议同意书前复选框"):
            # 复选框默认不勾选,点击复选框
            self.driver.find_element_by_id("signup_termschk").click()
            #operate_element(self.driver, 'signupPage', "signup_termschk", "click")
            assert "Mui-checked" in self.driver.find_element_by_xpath('//*[@id="signup_termschk"]/..').\
                get_attribute("class"), "复选框勾选失败"
        # with allure.step("点击Terms of Services并关闭页面"):
        #     operate_element(self.driver, 'signupPage', "service", "click")
        #     assert check_web(self.driver, "signupPage", "full-width-tab-0"), "Terms of Services页面未显示"
        #     #关闭窗口的close按钮缺一个id
        #     # operate_element(self.driver, 'signupPage', "", "click")
        #     # assert (check_web(self.driver, "signupPage", "full-width-tab-0") is False), "Terms of Services页面未显示"
        # with allure.step("点击Privacy Policy并关闭页面"):
        #     operate_element(self.driver, 'signupPage', "policy", "click")
        #     assert check_web(self.driver, "signupPage", "full-width-tab-0"), "Privacy Policy页面未显示"
