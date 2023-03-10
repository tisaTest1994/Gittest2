from Function.web_common_function import *
from Function.api_function import *
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from airtest_selenium.proxy import WebChrome
from selenium import webdriver
from airtest.core.api import *
import allure
import platform


class webFunction:

    @staticmethod
    def launch_web(url):
        # os.path.abspath()获得绝对路径
        path = os.path.abspath(os.path.dirname(__file__))
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-gpu')
        # 指定浏览器的分辨率
        options.add_argument('--window-size=1920,1080')
        options.add_argument("--no-sandbox")
        # 不显示正在受自动化软件控制
        options.add_experimental_option("excludeSwitches", ['enable-automation'])
        options.add_experimental_option('useAutomationExtension', False)
        # 指定浏览器以无头模式运行
        # 无界面运行
        options.add_argument('--headless')
        if 'mac' in str(platform.platform()):
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_mac", chrome_options=options, desired_capabilities=DesiredCapabilities.CHROME)
        else:
            driver = WebChrome(executable_path=path + "/../Resource/chromedriver_linux", desired_capabilities=DesiredCapabilities.CHROME, chrome_options=options)
        driver.get(url)
        return driver

    @staticmethod
    def login_web(chrome_driver, account=get_json()['web'][get_json()['env']]['account'], password=get_json()['web'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert operate_element_web(chrome_driver, 'loginPage', 'signinForm', type='check'), '未打开登录页面'
        with allure.step("输入账号"):
            operate_element_web(chrome_driver, 'loginPage', 'username', type='delete')
            operate_element_web(chrome_driver, 'loginPage', 'username', type='input', input_string=account)
        with allure.step("输入密码"):
            operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', type='delete')
            operate_element_web(chrome_driver, 'loginPage', 'sign_password_input', type='input', input_string=password)
        with allure.step("点击log in"):
            operate_element_web(chrome_driver, 'loginPage', 'login_login')
            sleep(3)
        with allure.step("确定已经登录成功到首页"):
            assert operate_element_web(chrome_driver, 'assetPage', 'Cabital Logo', type='check'), '未成功登录'
            sleep(3)

    # 登出 Web
    @staticmethod
    def logout_web(chrome_driver):
        with allure.step("点击登出"):
            operate_element_web(chrome_driver, 'assetPage', 'header-btn-hi-nickname')
            operate_element_web(chrome_driver, 'assetPage', 'header-btn-user-signout')
            assert operate_element_web(chrome_driver, 'loginPage', 'login_forgotpw', "check"), "未退出账号"

    # 注册 web
    @staticmethod
    def signup_web(chrome_driver):
        test_account = generate_email()
        email_code = get_json()['web'][get_json()['env']]['code']
        password = get_json()['web'][get_json()['env']]['password']
        with allure.step("确定打开登录页面"):
            assert operate_element_web(chrome_driver, 'loginPage', 'signinForm', type='check'), '未打开登录页面'
        with allure.step("填写注册信息"):
            # 点击signup按钮，跳转至signup页面
            operate_element_web(chrome_driver, 'loginPage', "login_gotosignup")
            # 输入账号
            operate_element_web(chrome_driver, 'signupPage', "signup_form_password_email", "input", test_account)
            # 点击发送验证码
            operate_element_web(chrome_driver, 'signupPage', "signup_sendcode")
            # 输入验证码
            operate_element_web(chrome_driver, 'signupPage', "mailcode", "input", email_code)
            # 输入密码
            operate_element_web(chrome_driver, 'signupPage', "signup_form_password_input", "input", password)
            # 勾选复选框
            operate_element_web(chrome_driver, 'signupPage', "signup_termschk")
            # 点击注册按钮
            operate_element_web(chrome_driver, 'signupPage', "signup_registernow")
            time.sleep(2)
        with allure.step("确定注册成功"):
            assert operate_element_web(chrome_driver, "assetPage", "Cabital Logo", "check"), "注册失败"

    # 注册 web指定账号（因为要很多账号且能收到bybit邮件）
    @staticmethod
    def signup_web_specified(chrome_driver, test_account, email_code=get_json()['web'][get_json()['env']]['code'],
                             password=get_json()['web'][get_json()['env']]['password']):
        with allure.step("确定打开登录页面"):
            assert operate_element_web(chrome_driver, 'loginPage', 'signinForm', type='check'), '未打开登录页面'
        with allure.step("填写注册信息"):
            # 点击signup按钮，跳转至signup页面
            operate_element_web(chrome_driver, 'loginPage', "login_gotosignup")
            # 输入账号
            operate_element_web(chrome_driver, 'signupPage', "signup_form_password_email", "input", test_account)
            # 点击发送验证码
            operate_element_web(chrome_driver, 'signupPage', "signup_sendcode")
            # 输入验证码
            operate_element_web(chrome_driver, 'signupPage', "mailcode", "input", email_code)
            # 输入密码
            operate_element_web(chrome_driver, 'signupPage', "signup_form_password_input", "input", password)
            # 勾选复选框
            operate_element_web(chrome_driver, 'signupPage', "signup_termschk")
            # 点击注册按钮
            operate_element_web(chrome_driver, 'signupPage', "signup_registernow")
            time.sleep(2)
        with allure.step("确定注册成功"):
            assert operate_element_web(chrome_driver, "assetPage", "Cabital Logo", "check"), "注册失败"

    # web生成随机convert金额
    @staticmethod
    def web_cfx_random(pair, major_ccy):
        buy_type = pair.split('-')[0]
        sell_type = pair.split('-')[1]
        if major_ccy.lower() == buy_type.lower():
            with allure.step("major_ccy 是buy值"):
                if buy_type == 'BTC' or buy_type == 'ETH':
                    buy_amount = random.uniform(0.02, 0.39999999)
                elif buy_type == 'USDT':
                    buy_amount = random.uniform(10, 500.999999)
                else:
                    buy_amount = random.uniform(10, 500.99)
                quote = ApiFunction.get_quote(pair)
                buy_amount = crypto_len(number=str(buy_amount), type=buy_type)
                sell_amount = crypto_len(number=str(float(buy_amount) * float(quote['quote'])), type=sell_type)
        else:
            with allure.step("major_ccy 是sell值"):
                if sell_type == 'BTC' or sell_type == 'ETH':
                    sell_amount = random.uniform(0.02, 0.39999999)
                elif sell_type == 'USDT':
                    sell_amount = random.uniform(10, 500.999999)
                else:
                    sell_amount = random.uniform(10, 500.99)
                quote = ApiFunction.get_quote(pair)
                sell_amount = crypto_len(number=str(sell_amount), type=sell_type)
                buy_amount = crypto_len(number=str(float(sell_amount) / float(quote['quote'])), type=buy_type)
        data = {
            "quote_id": quote['quote_id'],
            "quote": quote['quote'],
            "pair": pair,
            "buy_amount": str(buy_amount),
            "sell_amount": str(sell_amount),
            "major_ccy": major_ccy
        }
        return {'data': data}

    # web convert币种切换
    @staticmethod
    def web_convert_select_currency(chrome_driver,buy_currency, sell_currency):
        crypto_list = get_json()['crypto_list']
        cash_list = get_json()['cash_list']
        fiat_sell_default = 'EUR'
        fiat_buy_default = 'USDT'
        if buy_currency in cash_list:
            # 如果buy的币种和sell的默认币EUR种相同，则先把sell的默认币种改成BTC
            operate_element_web(chrome_driver, 'convertPage', 'convert_sell_select')
            sleep(1)
            operate_element_web(chrome_driver, 'convertPage', '{}'.format("BTC"))
            assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_select',
                                       'get_text') == "BTC", "sell币种切换失败"
        with allure.step("切换buy的币种"):
            if buy_currency != fiat_buy_default:
                operate_element_web(chrome_driver, 'convertPage', 'convert_buy_select')
                sleep(1)
                operate_element_web(chrome_driver, 'convertPage', '{}'.format(buy_currency))
                assert operate_element_web(chrome_driver, 'convertPage', 'convert_buy_select',
                                           'get_text') == buy_currency, "buy币种{}切换失败".format(buy_currency)
        with allure.step("切换sell的币种"):
            if sell_currency != fiat_sell_default:
                operate_element_web(chrome_driver, 'convertPage', 'convert_sell_select')
                sleep(1)
                operate_element_web(chrome_driver, 'convertPage', '{}'.format(sell_currency))
                assert operate_element_web(chrome_driver, 'convertPage', 'convert_sell_select',
                                           'get_text') == sell_currency, "sell币种{}切换失败".format(buy_currency)
