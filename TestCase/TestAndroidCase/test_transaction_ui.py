from Function.ui_function import *
from Function.api_function import *
import allure


class TestTransactionUi:

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

    @allure.testcase('test_transaction_ui_001 查询所有交易信息')
    def test_transaction_ui_001(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')

    @allure.testcase('test_transaction_ui_002 查询BTC交易信息')
    def test_transaction_ui_002(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择币种"):
            click('CB403')
            click('BTC')
        with allure.step("接口获取BTC交易列表"):
            transaction_info = UiFunction.choose_transaction(crypto_type=['BTC'])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('android.widget.ScrollView').child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'], poco('android.widget.ScrollView').child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('android.widget.ScrollView').child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_003 查询ETH交易信息')
    def test_transaction_ui_003(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择币种"):
            click('CB403')
            click('ETH')
        with allure.step("接口获取ETH交易列表"):
            transaction_info = UiFunction.choose_transaction(crypto_type=['ETH'])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('android.widget.ScrollView').child().child().child()[
                0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],
                                                         poco('android.widget.ScrollView').child().child().child()[
                                                             0].attr('name'))
        with allure.step("点击transaction"):
            poco('android.widget.ScrollView').child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_004 查询USDT交易信息')
    def test_transaction_ui_004(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择币种"):
            click('CB403')
            click('USDT')
        with allure.step("接口获取USDT交易列表"):
            transaction_info = UiFunction.choose_transaction(crypto_type=['USDT'])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('android.widget.ScrollView').child().child().child()[
                0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],
                                                         poco('android.widget.ScrollView').child().child().child()[
                                                             0].attr('name'))
        with allure.step("点击transaction"):
            poco('android.widget.ScrollView').child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_005 查询Deposit交易信息')
    def test_transaction_ui_005(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB079')
        with allure.step("接口获取Deposit交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[1])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_006 查询Withdraw交易信息')
    def test_transaction_ui_006(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB307')
        with allure.step("接口获取Withdraw交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[6])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_007 查询Convert交易信息')
    def test_transaction_ui_007(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB062')
        with allure.step("接口获取Convert交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[2])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_008 查询Subscribe Flexible交易信息')
    def test_transaction_ui_008(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB259')
        with allure.step("接口获取Subscribe Flexible交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[3], product_type=[2])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_009 查询Subscribe Fixed交易信息')
    def test_transaction_ui_009(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB258')
        with allure.step("接口获取Subscribe Flexible交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[3], product_type=[1])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_010 查询Interest交易信息')
    def test_transaction_ui_010(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB162')
        with allure.step("接口获取Interest交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[4])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_011 查询Maturity交易信息')
    def test_transaction_ui_011(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB176')
        with allure.step("接口获取Maturity交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[5], product_type=[1])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_012 查询Redeem交易信息')
    def test_transaction_ui_012(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB229')
        with allure.step("接口获取Redeem交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[5], product_type=[2])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])

    @allure.testcase('test_transaction_ui_013 查询Reward交易信息')
    def test_transaction_ui_013(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB401')
        with allure.step("接口获取Reward交易列表"):
            transaction_info = UiFunction.choose_transaction(type=[7])
        with allure.step("检车交易transaction"):
            assert transaction_info['transaction_text'] in poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'), '第一个项目是{}, 发现{}'.format(transaction_info['transaction_text'],poco('Date').parent().child()[4].child().child().child().child()[0].attr('name'))
        with allure.step("点击transaction"):
            poco('Date').parent().child()[4].child().child().child().child()[0].click()
        with allure.step("检查页面transaction_id"):
            check(transaction_info['transaction_id'])