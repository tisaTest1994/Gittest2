from Function.ui_common_function import *


class UiFunction:

    @staticmethod
    def login(account, password):
        with allure.step("判断升级提示"):
            if operate_element_app('welcomePage', 'Later', type='check', wait_time_max=10):
                operate_element_app('welcomePage', 'Later')
        with allure.step("先判断是否已经登录，判断升级提示"):
            if operate_element_app('portfolioPage', 'Portfolio', type='check'):
                return True
            else:
                with allure.step("开始登录流程"):
                    operate_element_app('welcomePage', 'Log In')
        with allure.step("检查是否到达log in 页面"):
            assert operate_element_app('loginPage', 'Welcome Back', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('loginPage', 'Welcome Back')
        with allure.step("输入账户密码"):
            # poco(text="Account").click()
            # text(account)
            # text(password)
            # sleep(1)
            poco("android.widget.EditText").click()
            sleep(1)
            if operate_element_app('loginPage', 'android.widget.ImageView', 'check') is True:
                poco(text="Password").click()
                text(password)
                sleep(1)
            else:
                text(account)
                text(password)
                sleep(1)
        with allure.step("判断升级提示"):
            if operate_element_app('welcomePage', 'Later', type='check'):
                operate_element_app('welcomePage', 'Later')
        with allure.step("判断登录到首页"):
            assert operate_element_app('portfolioPage', 'Portfolio', type='check'), '没有到达{}页面或者找不到{}页面元素'.format(
                'portfolioPage', 'Portfolio')

    @staticmethod
    def logout():
        with allure.step("判断登录到首页"):
            assert operate_element_app('portfolioPage', 'Portfolio', type='check'), '没有到达{}页面或者找不到{}页面元素'.format(
                'portfolioPage', 'Portfolio')
        with allure.step("点击 Account 页面"):
            operate_element_app('accountPage', 'Account')
        with allure.step("点击 log out 元素"):
            operate_element_app('accountPage', 'log out')
        with allure.step("检查log out 弹框文案"):
            assert operate_element_app('accountPage', 'Are you sure to log out?', type='check'), '没有到达{}页面或者找不到{}页面元素'.format('accountPage', 'Are you sure to log out?')
        with allure.step("点击log out"):
            operate_element_app('accountPage', 'log out', type='1')[1].click()
            sleep(2)
        with allure.step("判断升级提示"):
            if operate_element_app('welcomePage', 'Later', type='check', wait_time_max=10):
                operate_element_app('welcomePage', 'Later')
        with allure.step("检查已经退出"):
            assert operate_element_app('welcomePage', 'Log In', type='check'), '没有到达{}页面或者找不到{}页面元素'.format(
                'welcomePage', 'Log In')

    @staticmethod
    def choose_transaction(crypto_type=['BTC', 'ETH', 'USDT'], num=0, type=[1, 2, 3, 4, 5, 6, 7], product_sub_type=[1, 2]):
        if 3 in type or 5 in type:
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 10
                },
                "user_txn_sub_types": type,
                "codes": crypto_type,
                "product_sub_types": product_sub_type
            }
        else:
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 10
                },
                "user_txn_sub_types": type,
                "codes": crypto_type,
            }
        r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
        transaction_info = r.json()['transactions'][num]
        logger.info('transaction信息是{}'.format(transaction_info))
        if transaction_info['user_txn_sub_type'] == 1:
            transaction_text = 'Deposit\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
        elif transaction_info['user_txn_sub_type'] == 2:
            transaction_text = 'Convert\n' + add_comma_number(str(json.loads(transaction_info['details'])['buy_currency']['amount']))
        elif transaction_info['user_txn_sub_type'] == 3:
            if transaction_info['product_sub_type'] == 1:
                transaction_text = 'Subscribe Fixed\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
            elif transaction_info['product_sub_type'] == 2:
                transaction_text = 'Subscribe Flexible\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
            else:
                transaction_text = 'Subscribe'
        elif transaction_info['user_txn_sub_type'] == 4:
            transaction_text = 'Interest\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
        elif transaction_info['user_txn_sub_type'] == 5:
            if transaction_info['product_sub_type'] == 1:
                transaction_text = 'Maturity\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
            elif transaction_info['product_sub_type'] == 2:
                transaction_text = 'Redeem\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
            else:
                transaction_text = 'Maturity'
        elif transaction_info['user_txn_sub_type'] == 6:
            transaction_text = 'Withdraw\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
        elif transaction_info['user_txn_sub_type'] == 7:
            transaction_text = 'Reward\n' + add_comma_number(str(json.loads(transaction_info['details'])['currency']['amount']))
        sleep(1)
        return {'transaction_id': transaction_info['transaction_id'], 'transaction_text': transaction_text}

    @staticmethod
    def choose_display_currency(type='USD'):
        # 点击 Account
        click('CB008')
        # 点击 My Preference
        click('CB179')
        # 获得当前哦那个户数据
        r = requests.request('GET', url='{}/account/info'.format(env_url), headers=headers)
        display_currency = r.json()['user']['userPreferenceSettings']['currency']
        if type != display_currency:
            # 点击Display Currency
            click(get_ui_text('CB090') + '\n' + display_currency)
            click(type)
            #回退页面
        keyevent('KEYCODE_BACK')
        # 下拉刷新
        click('CB214')
        slide('down')
        sleep(2)
