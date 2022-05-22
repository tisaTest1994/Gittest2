from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api transaction 相关 testcases")
class TestTransactionApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transaction_001')
    @allure.description('查询全部交易记录')
    def test_transaction_001(self):
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 100
            },
            "user_txn_sub_types": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "statuses": [1, 2, 3, 4],
            "codes": []
        }
        with allure.step("查询特定条件的交易"):
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "查询全部交易记录错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_002')
    @allure.description('查询某些条件的交易记录')
    def test_transaction_002(self):
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 100
            },
            "user_txn_sub_types": [8, 9, 10, 11],
            "statuses": [1, 2, 3, 4],
            "codes": []
        }
        with allure.step("查询特定条件的交易"):
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "查询某些条件的交易记录错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_003')
    @allure.description('查询指定Debit详情')
    def test_transaction_003(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account='5CDucWnrB@189.com')
        transaction_id = 'cfe616da-4f1d-4e54-b826-50bc010b1b6a'
        params = {
            'txn_sub_type': 1
        }
        r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['transaction']['transaction_id'] == transaction_id, "查询指定Debit详情错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_004')
    @allure.description('web查询全部交易记录')
    def test_transaction_004(self):
        data = {
            "pagination_request": {
                "page_no": 1,
                "page_size": 100
            },
            "user_txn_sub_types": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
            "statuses": [1, 2, 3, 4],
            "codes": []
        }
        with allure.step("查询特定条件的交易"):
            r = session.request('POST', url='{}/txn/query/web'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "web查询全部交易记录错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_005')
    @allure.description('web查询很后面页面交易数据为空')
    def test_transaction_005(self):
        data = {
            "pagination_request": {
                "page_no": 9113,
                "page_size": 100
            }
        }
        with allure.step("web查询很后面页面交易数据为空"):
            r = session.request('POST', url='{}/txn/query/web'.format(env_url), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['transactions'] == [], "web查询全部交易记录错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_006')
    @allure.description('根据id编号查询单笔交易')
    def test_transaction_006(self):
        with allure.step("获得交易transaction_id"):
            transaction_id = ApiFunction.get_payout_transaction_id()
            logger.info('transaction_id 是{}'.format(transaction_id))
        with allure.step("查询单笔交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            params = {
                "txn_sub_type": 6
            }
            r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'product_id' in r.text, "根据id编号查询单笔交易错误，返回值是{}".format(r.text)

    @allure.title('test_transaction_007')
    @allure.description('查询特定条件的交易')
    def test_transaction_007(self):
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 100
            },
            "user_txn_sub_types": [1, 2, 3, 4, 5, 6],
            "statuses": [1, 2, 3, 4],
            "codes": ["ETH"]
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

