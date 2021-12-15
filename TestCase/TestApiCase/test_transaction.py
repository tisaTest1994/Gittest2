from Function.api_function import *
from Function.operate_sql import *


# core相关cases
class TestTransactionApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.testcase('test_transaction_001 查询钱包所有币种详细金额以及报价，以美元价格返回')
    def test_transaction_001(self):
        with allure.step("查询钱包所有币种详细金额以及报价，以美元价格返回"):
            r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'wallets' in r.text, "查询钱包所有币种详细金额以及报价，以美元价格返回错误，返回值是{}".format(r.text)

    @allure.testcase('test_transaction_002 查询全部交易记录')
    def test_transaction_002(self):
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 100
            },
            "user_txn_sub_types": [1, 2, 3, 4, 5, 6],
            "statuses": [1, 2, 3, 4],
            "codes": []
        }
        with allure.step("查询特定条件的交易"):
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "获取产品列表错误，返回值是{}".format(r.text)