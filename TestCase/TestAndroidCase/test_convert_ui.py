from Function.ui_function import *
from Function.api_function import *
import allure


class TestConvertUi:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app(package_name)
        # 登录 app
        UiFunction.login(account=email['email'], password=email['password'])

    # 每个cases结束后
    def teardown(self):
        # 关闭 app
        stop_app(package_name)

    @allure.testcase('test_convert_ui_001 换汇页面显示sell币种的可用余额')
    def test_convert_ui_001(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
            pair = '{}-{}'.format(list(pairs.keys())[0], pairs[list(pairs.keys())[0]][0])
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type=pair.split('-')[0], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证页面显示sell币种可用的Balance"):
            check("{} {} {}".format(get_json(file='multiple_languages.json')['CB036'], number, pair.split('-')[0]))

    @allure.testcase('test_convert_ui_002 换汇页面点击MAX')
    def test_convert_ui_002(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
            pair = '{}-{}'.format(list(pairs.keys())[0], pairs[list(pairs.keys())[0]][0])
        with allure.step("换汇页面点击MAX"):
            click("CB177")
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type=pair.split('-')[0], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证换汇页面点击MAX"):
            check('{}.*'.format(number), type='textMatches')

    @allure.testcase('test_convert_ui_003 换汇页面点击汇率转换按钮')
    def test_convert_ui_003(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
            pair = '{}-{}'.format(list(pairs.keys())[0], pairs[list(pairs.keys())[0]][0])
        with allure.step("点击转换sell-buy按钮"):
            click("android.widget.ImageView")
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type=pair.split('-')[1], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证页面显示sell币种可用的Balance"):
            check("{} {} {}".format(get_json(file='multiple_languages.json')['CB036'], number, pair.split('-')[1]))

    @allure.testcase('test_convert_ui_004 换汇页面点击汇率查询转换按钮')
    def test_convert_ui_004(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
        with allure.step("获得汇率"):
            r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, '{}-{}'.format(pairs[list(pairs.keys())[0]][0], list(pairs.keys())[0])), headers=headers)
            quote = r.json()['quote']
            quote_display = crypto_len(number=quote, type=list(pairs.keys())[0])
        with allure.step("检查汇率转换显示的汇率"):
            logger.info('汇率是1{}{}{}'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]))
            #check('1{}\{}\{}.*'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]), type='nameMatches')
        with allure.step("点击汇率转换按钮"):
            touch(Template(r'./../../Resource/Photos/cfx_change_pairs.png'))
            sleep(5)

    @allure.testcase('test_convert_ui_005 换汇页面切换sell币种')
    def test_convert_ui_005(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
            pair = '{}-{}'.format(list(pairs.keys())[0], pairs[list(pairs.keys())[0]][1])
        with allure.step("点击转换sell按钮"):
            click(pair.split('-')[0])
            check('CB212')
        with allure.step("Api获得币种可用Balance"):
            number = AccountFunction.get_crypto_number(type=pair.split('-')[1], balance_type='BALANCE_TYPE_AVAILABLE',
                                                       wallet_type='BALANCE')
            number = add_comma_number(number)
        with allure.step("选择其他货币并且检查余额"):
            check('{}.*'.format('ET'), type='textMatches')
            check('{} {}'.format(number, pair.split('-')[1]))


