from Function.ui_function import *
import allure
from Function.api_common_function import *
from TestCase.TestApiCase.test_asset import *
import datetime


class TestAccountUi:

    def setup_method(self):
        with allure.step("打开 app"):
            start_app(package_name)
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    def teardown(self):
        with allure.step("关闭 app"):
            stop_app(package_name)

    @allure.title('test_account_001')
    @allure.description('使用已经注册账户登录，登录进入主页后退出')
    def test_account_001(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
            sleep(5)
            assert False, '123'
        with allure.step("登出"):
            UiFunction.logout()
            sleep(3)

    @allure.title('test_account_002')
    @allure.description('注册新账号')
    def test_account_002(self):
        with allure.step("判断升级提示"):
            if operate_element_app('welcomePage', 'Later', type='check', wait_time_max=10):
                operate_element_app('welcomePage', 'Later')
        with allure.step("先判断是否已经登录，判断升级提示"):
            if operate_element_app('portfolioPage', 'Portfolio', type='check'):
                return True
            else:
                with allure.step("开始注册流程"):
                    operate_element_app('signupPage', 'Sign Up')
                    sleep(3)
                # assert断言进入注册页面
                with allure.step("检查是否到达Sign Up 页面"):
                    assert operate_element_app('signupPage', 'Sign up with email', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Sign up with email')
                with allure.step("输入邮箱"):
                    text(generate_email())
                with allure.step("勾选协议"):
                    operate_element_app('signupPage', 'rule box')
                with allure.step("点击发送验证码"):
                    operate_element_app('signupPage', "Send Verification Code", type='click')
                with allure.step("检查是否到达输入邮箱验证码页面"):
                    assert operate_element_app('signupPage', 'Verify your email', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Verify your email')
                # with allure.step("Resend"):
                #     operate_element_app('signupPage', "Resend", type='click')
                with allure.step("输入邮箱验证码"):
                    text(get_json()['Web'][get_json()['env']]['code'])
                # assert断言Next按钮可点击
                with allure.step("判断是否可点击Next"):
                    assert operate_element_app('signupPage', "Next", type='check_enabled'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Next')
                with allure.step("点击Next"):
                    operate_element_app('signupPage', "Next", type='click')
                with allure.step("断言进入设置密码页面"):
                    assert operate_element_app('signupPage', 'Set login password', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Set login password')
                with allure.step("设置密码"):
                    operate_element_app('signupPage', 'password', type='input', input_string=get_json()['web'][get_json()['env']]['password'])
                # with allure.step("断言密码设置成功，高亮显示3个规则"):
                #     assert operate_element_app('signupPage', 'password rule box', type='check_selected'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'password rule box')
                    operate_element_app('signupPage', 'password', type='input', input_string=get_json()['Web'][get_json()['env']]['password'])

                with allure.step("点击Confirm Password"):
                    operate_element_app('signupPage', "Confirm Password", type='click')
                with allure.step("断言进入设置密码页面"):
                    assert operate_element_app('signupPage', 'Total Assert Value', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('signupPage', 'Total Assert Value')
            with allure.step("登出"):
                UiFunction.logout()
                sleep(3)

    @allure.title('test_account_003')
    @allure.description('portfolio 页面验证 total asset value')
    def test_account_003(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("通过API 获取Total Asset value"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            total_asset_value = r.json()['summary']['abs_amount']
            print(total_asset_value)
            total_asset_value_page = add_currency_symbol(total_asset_value, 'USD', True)
            print(total_asset_value_page)
            print(operate_element_app('portfolioPage', total_asset_value_page, 'check'))
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total_asset_value_page在页面的值是{}'.format(total_asset_value_page)

    @allure.title('test_account_004')
    @allure.description('portfolio 页面跳转进Asset Overview验证total asset value')
    def test_account_004(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("点击View"):
            operate_element_app('portfolioPage', 'View', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
        with allure.step("通过API 获取BTC的百分比"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
            print(r.json())
            total_asset_value = r.json()['summary']['abs_amount']
            print('total_asset_value：{}'.format(total_asset_value))
            total_asset_value_page = add_currency_symbol(total_asset_value, 'USD', True)
            print('total_asset_value_page：{}'.format(total_asset_value_page))
            print(operate_element_app('portfolioPage', total_asset_value_page, 'check'))
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total asset value在页面的值是{}'.format(total_asset_value_page)

    @allure.title('test_account_005')
    @allure.description('portfolio 页面跳转进Asset Overview验证5种币种的占比')
    def test_account_005(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("点击View"):
            operate_element_app('portfolioPage', 'View', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
        with allure.step("通过API 获取BTC的百分比"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            print(r.json())
            overview = r.json()['overview']
            for i in overview:
                code = i['code']
                percent = i['percent']
                print(code, percent)
                assert operate_element_app('portfolioPage', code, 'check') is True, 'code在页面的值是{}'.format(code)
                assert operate_element_app('portfolioPage', percent, 'check') is True, 'percent在页面的值是{}'.format(percent)

    @allure.title('test_account_006')
    @allure.description('portfolio 页面跳转进Asset Value初始值')
    def test_account_006(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("点击View"):
            operate_element_app('portfolioPage', 'View', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('portfolioPage', 'Asset Allocation')
        with allure.step("通过API 获取Asset Value初始值"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            total_asset_value = r.json()['history'][0]['total_value']
            total_asset_value_page = add_currency_symbol(total_asset_value, 'USD', True)
            print(operate_element_app('portfolioPage', total_asset_value_page, 'check'))
            assert operate_element_app('portfolioPage', total_asset_value_page, 'check') is True, 'total asset value在页面的值是{}'.format(total_asset_value_page)
        history = r.json()['history']
        print(history)
        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days=1)
        for i in history:
            date1 = i['date'].split()[0]
            if date1 == yesterday:
                total_value='$'+ i['total_value']
                print('date1的值是：{}'.format(date1))
                print('total_value的值是：{}'.format(total_value))
                assert operate_element_app('portfolioPage', date, 'check') is True, 'date在页面的值是{}'.format(date)
                assert operate_element_app('portfolioPage', total_value, 'check') is True, 'total_value在页面的值是{}'.format(total_value)
            else:
                pass

    @allure.title('test_account_007')
    @allure.description('portfolio 页面跳转进Asset Value初始值')
    def test_account_007(self):
        with allure.step("登录"):
            UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])
        with allure.step("点击View"):
            operate_element_app('portfolioPage', 'View', 'click')
        assert operate_element_app('portfolioPage', 'Asset Allocation', type='check'), '没有到达{}页面或者找不到{}页面元素'.format(
            'portfolioPage', 'Asset Allocation')
        with allure.step("通过API 获取Asset Value初始值"):
            headers['X-Currency'] = 'USD'
            r = session.request('GET', url='{}/assetstatapi/assetstat'.format(env_url), headers=headers)
            total_asset_value = r.json()['history'][0]['total_value']
            total_asset_value_page = add_currency_symbol(total_asset_value, 'USD', True)
            print(operate_element_app('portfolioPage', total_asset_value_page, 'check'))

                    











































