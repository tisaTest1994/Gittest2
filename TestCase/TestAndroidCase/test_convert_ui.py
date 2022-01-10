from Function.ui_function import *
from Function.api_function import *
import allure


class TestConvertUi:

    # 每个cases前执行
    def setup(self):
        # 打开 app
        start_app(package_name)
        # 登录 app
        UiFunction.login(account=get_json()['email']['email'], password=get_json()['email']['password'])

    # 每个cases结束后
    def teardown(self):
        # 关闭 app
        stop_app(package_name)

    @allure.title('test_convert_ui_001 换汇页面显示sell币种的可用余额')
    def test_convert_ui_001(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
            pair = '{}-{}'.format(list(pairs.keys())[0], pairs[list(pairs.keys())[0]][0])
        with allure.step("Api获得币种可用Balance"):
            number = ApiFunction.get_crypto_number(type=pair.split('-')[0], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证页面显示sell币种可用的Balance"):
            check("{} {} {}".format(get_json(file='multiple_languages.json')['CB036'], number, pair.split('-')[0]))

    @allure.title('test_convert_ui_002 换汇页面点击MAX')
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
            number = ApiFunction.get_crypto_number(type=pair.split('-')[0], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证换汇页面点击MAX"):
            check('{}.*'.format(number), type='textMatches')

    @allure.title('test_convert_ui_003 换汇页面点击汇率转换按钮')
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
            number = ApiFunction.get_crypto_number(type=pair.split('-')[1], balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE')
        with allure.step("验证页面显示sell币种可用的Balance"):
                check("{} {} {}".format(get_json(file='multiple_languages.json')['CB036'], number, pair.split('-')[1]))

    @allure.title('test_convert_ui_004 换汇页面点击汇率查询转换按钮')
    def test_convert_ui_004(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
        with allure.step("获得汇率"):
            r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, '{}-{}'.format(pairs[list(pairs.keys())[0]][0], list(pairs.keys())[0])), headers=headers)
            quote_display = crypto_len(number=r.json()['quote'], type=list(pairs.keys())[0])
        with allure.step("检查汇率转换显示的汇率"):
            logger.info('汇率是1{}{}{}'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]))
            assert add_comma_number(quote_display) in poco(get_ui_text('CB240')).sibling()[6].attr('name'), '汇率对错误，后端返回的汇率对是{}, 前端显示的是{}'.format(add_comma_number(quote_display), poco('Sell').sibling()[6].attr('name'))
        with allure.step("点击汇率转换按钮"):
            touch(Template('./../../Resource/Photos/cfx_change_pairs.png'))
            sleep(5)
        with allure.step("重新获得汇率并取倒数汇率"):
            r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, '{}-{}'.format(pairs[list(pairs.keys())[0]][0], list(pairs.keys())[0])), headers=headers)
            quote_display = crypto_len(number=Decimal(1) / Decimal(r.json()['quote']), type=pairs[list(pairs.keys())[0]][0])
        with allure.step("检查汇率转换显示的汇率"):
            logger.info('汇率是1{}{}{}'.format(list(pairs.keys())[0], quote_display, pairs[list(pairs.keys())[0]][0]))
            assert add_comma_number(quote_display) in poco(get_ui_text('CB240')).sibling()[6].attr('name'), '汇率对错误，后端返回的汇率对是{}, 前端显示的是{}'.format(add_comma_number(quote_display), poco('Sell').sibling()[6].attr('name'))

    @allure.title('test_convert_ui_005 换汇页面切换sell币种')
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
            number = ApiFunction.get_crypto_number(type=pair.split('-')[1], balance_type='BALANCE_TYPE_AVAILABLE',
                                                       wallet_type='BALANCE')
            number = add_comma_number(number)
        with allure.step("检查页面上币种可用Balance和api返回一致"):
            assert str(number) in poco('Continue').sibling().child().child()[0].attr('name'), 'api返回是{}, ui显示是{}'.format(str(number), poco('Continue').sibling().child().child()[0].attr('name'))
        with allure.step("选择其他货币并且点击确认"):
            poco(get_ui_text('CB059')).sibling().child().child().click()
            click('CB059')

    @allure.title('test_convert_ui_006 换汇并且检查金额')
    def test_convert_ui_006(self):
        with allure.step("进入换汇页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB062')
        with allure.step("输入需要sell的数量并确认"):
            poco('android.widget.EditText').click()
            text('0.003')
            keyevent("KEYCODE_ENTER")
            wait_time = 0
            while wait_time < 10:
                wait_time = wait_time + 1
                sleep(1)
                if poco(get_ui_text('CB062'))[1].attr('enabled'):
                    poco(get_ui_text('CB062'))[1].click()
                    wait_time = 11
        with allure.step("确认进入订单详情页面"):
            check('CB061')
        with allure.step("获得换汇汇率对"):
            r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
            pairs = r.json()['codes']
        with allure.step("获得汇率"):
            r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, '{}-{}'.format(pairs[list(pairs.keys())[0]][0], list(pairs.keys())[0])), headers=headers)
            quote_display = crypto_len(number=r.json()['quote'], type=list(pairs.keys())[0])
            logger.info('1{}={}{}'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]))
            check('1{}={}{}'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]))
        with allure.step("点击确认cfx交易"):
            wait_time = 0
            while wait_time < 10:
                wait_time = wait_time + 1
                sleep(1)
                if poco(get_ui_text('CB062')).attr('enabled'):
                    click('CB062')
                    wait_time = 11
        with allure.step("等待transaction详情页面"):
            check('{} {}'.format(get_ui_text('CB060').split(' ')[0], get_ui_text('CB262')))
        with allure.step("检查transaction详情页面交易金额和汇率"):
            check('1 {} = {} {}'.format(pairs[list(pairs.keys())[0]][0], quote_display, list(pairs.keys())[0]))
            check('0.003 {}'.format(list(pairs.keys())[0]))
        with allure.step("点击回到钱包"):
            click('CB431')
        with allure.step("检查回到钱包"):
            check('CB307')



