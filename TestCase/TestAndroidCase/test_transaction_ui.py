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
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 10
                },
                "user_txn_sub_types": [1, 2, 3, 4, 5, 6],
                "statuses": [1, 2, 3, 4],
                "codes": ["BTC"]
            }
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            print(r.json())

    @allure.testcase('test_transaction_ui_003 查询ETH交易信息')
    def test_transaction_ui_003(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择币种"):
            click('CB403')
            click('ETH')

    @allure.testcase('test_transaction_ui_004 查询USDT交易信息')
    def test_transaction_ui_004(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择币种"):
            click('CB403')
            click('USDT')

    @allure.testcase('test_transaction_ui_005 查询Deposit交易信息')
    def test_transaction_ui_005(self):
        with allure.step("进入transaction页面"):
            poco(get_json(file='multiple_languages.json')['CB214']).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型"):
            click('CB020')
            click('CB079')

    @allure.testcase('test_transaction_ui_006 查询Deposit交易信息以及详细信息')
    def test_transaction_ui_006(self):
        with allure.step("进入transaction页面"):
            poco(get_ui_text('CB214')).parent().child("android.view.View")[1].click()
            click('CB284')
        with allure.step("选择交易类型为Deposit"):
            click('CB020')
            click('CB079')
        with allure.step("点击某个交易"):
            print(poco(get_ui_text('CB079')).exists())
            sleep(20)