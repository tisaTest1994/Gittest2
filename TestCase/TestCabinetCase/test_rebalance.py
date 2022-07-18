import allure

from Function.api_function import *
from Function.operate_sql import *


# operate相关cases
class TestRebalanceApi:

    # 初始化class
    def setup_method(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')

    @allure.title('test_rebalance_001')
    @allure.description('查询rebalance order')
    def test_rebalance_001(self):
        with allure.step("查询rebalance order"):
            data = {
                "pagination_request": {
                    "page_no": 1,
                    "page_size": 10
                },
                "sort_request": {
                    "field": "id",
                    "order": "desc"
                },
                "orderId": "",
                "status": 0,
                "order_type": 0,
                "value_date": 0,
                "money_house_id": "",
                "money_house_account_id": "",
                "matched": 0,
                "txn_hash": ""
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/search'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'pagination_response' in r.text, "查询order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_002')
    @allure.description('查询rebalance order detail')
    def test_rebalance_002(self):
        with allure.step("查询rebalance order detail"):
            orderId = "e93a34fd-c3ea-4d8a-9d30-85a01fa32686"
            r = session.request('GET', url='{}/operatorapi/orders/rebalance/{}'.format(operateUrl, orderId),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order' in r.text, "查询order detail错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_003')
    @allure.description('创建双边net fee rebalance order')
    def test_rebalance_003(self):
        with allure.step("创建双边net fee rebalance order"):
            txn_hash = generate_string(16)
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-12",
                            "order_type_enum": 1,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeLedger1DGTLT",
                            "currency": "CHESS",
                            "principal": "45",
                            "fee_detail": {
                                "amount": "5",
                                "cost_type": 1,
                                "currency": "CHESS"
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "dfe0bdd9-9abe-11ec-ae7e-0a3898443cb8",
                            "order_id": ""
                        },
                        {
                            "value_date": "2021-12-23",
                            "order_type_enum": 2,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeLedger2DGTLT",
                            "currency": "CHESS",
                            "principal": "50",
                            "fee_detail": {
                                "cost_type": 0,
                                "amount": "0"
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "dfe0c274-9abe-11ec-ae7e-0a3898443cb8",
                            "order_id": ""
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建双边net fee rebalance order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_004')
    @allure.description('创建双边separate fee rebalance order')
    def test_rebalance_004(self):
        with allure.step("创建双边separate fee rebalance order"):
            txn_hash = generate_string(16)
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 1,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeBinanceDGTLT",
                            "currency": "ETH",
                            "principal": "2.2",
                            "fee_detail": {
                                "amount": "0",
                                "cost_type": 0
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "3a3b81da-f04e-11eb-9e63-ba224deb3be4",
                            "order_id": ""
                        },
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 2,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeFireBlocksDGTLT",
                            "currency": "ETH",
                            "principal": "2.2",
                            "fee_detail": {
                                "cost_type": 2,
                                "amount": "0.0003",
                                "money_house_account_id": "3a3b75b8-f04e-11eb-9e63-ba224deb3be4",
                                "cost_txn_id": generate_string(16),
                                "currency": "ETH",
                                "value_date": "2021-12-21"
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "3a3b75b8-f04e-11eb-9e63-ba224deb3be4",
                            "order_id": ""
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建双边separate fee rebalance order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_005')
    @allure.description('创建单边pay-in order')
    def test_rebalance_005(self):
        with allure.step("创建单边pay-in order"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 1,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeTransactiveDGTLT",
                            "currency": "EUR",
                            "principal": "33",
                            "fee_detail": {
                                "amount": "",
                                "cost_type": 0,
                                "currency": ""
                            },
                            "operator": "system",
                            "txn_hash": generate_string(16),
                            "money_house_account_id": "df5f83a1-0973-11ec-b1e1-82683a56eb1d",
                            "order_id": ""
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-in order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_006')
    @allure.description('创建单边pay-out order')
    def test_rebalance_006(self):
        with allure.step("创建单边pay-out order"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 2,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeFTXDGTLT",
                            "currency": "EUR",
                            "principal": "33",
                            "fee_detail": {
                                "cost_type": 2,
                                "amount": "3",
                                "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                                "cost_txn_id": generate_string(16),
                                "currency": "EUR",
                                "value_date": "2021-12-21"
                            },
                            "operator": "system",
                            "txn_hash": '25C2lc79qWUFymE7',
                            "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                            "order_id": ""
                        },
                        {
                            "order_id": "07e1e465-f7c9-46d4-8c93-cb200d54bd6f"
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-out order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_007')
    @allure.description('创建单边pay-in order后再创建pay-out order匹配')
    def test_rebalance_007(self):
        txn_hash = generate_string(16)
        with allure.step("创建单边pay-in order后再创建pay-out order匹配"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 1,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeTransactiveDGTLT",
                            "currency": "EUR",
                            "principal": "22",
                            "fee_detail": {
                                "amount": "",
                                "cost_type": 0,
                                "currency": ""
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "df5f83a1-0973-11ec-b1e1-82683a56eb1d",
                            "order_id": ""
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
            order_id = r.json()['order_ids'][0]
            logger.info(order_id)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-in order错误，返回值是{}".format(r.text)
        with allure.step("创建pay-out order与其匹配"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 2,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeFTXDGTLT",
                            "currency": "EUR",
                            "principal": "22",
                            "fee_detail": {
                                "cost_type": 2,
                                "amount": "3",
                                "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                                "cost_txn_id": generate_string(16),
                                "currency": "EUR",
                                "value_date": "2021-12-21"
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                            "order_id": ""
                        },
                        {
                            "order_id": order_id
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-out order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_008')
    @allure.description('创建单边pay-out order后再创建pay-in order匹配')
    def test_rebalance_008(self):
        txn_hash = generate_string(16)
        with allure.step("创建单边pay-out order后再创建pay-in order匹配"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 2,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeTransactiveDGTLT",
                            "currency": "EUR",
                            "principal": "33",
                            "fee_detail": {
                                "cost_type": 2,
                                "amount": "3",
                                "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                                "cost_txn_id": generate_string(16),
                                "currency": "EUR",
                                "value_date": "2021-12-21"
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "df5f83a1-0973-11ec-b1e1-82683a56eb1d",
                            "order_id": ""
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
            order_id = r.json()['order_ids'][0]
            logger.info(order_id)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-in order错误，返回值是{}".format(r.text)
        with allure.step("创建pay-out order与其匹配"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-30",
                            "order_type_enum": 1,
                            "counterparty_txn_id": generate_string(16),
                            "money_house_id": "MoneyHouseTypeFTXDGTLT",
                            "currency": "EUR",
                            "principal": "33",
                            "fee_detail": {
                                "amount": "",
                                "cost_type": 0,
                                "currency": ""
                            },
                            "operator": "system",
                            "txn_hash": txn_hash,
                            "money_house_account_id": "e3fd552b-0faf-11ec-b6ea-a655f054239a",
                            "order_id": ""
                        },
                        {
                            "order_id": order_id
                        }
                    ]
            }
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_ids' in r.text, "创建单边pay-out order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_009')
    @allure.description('查询fx order')
    def test_rebalance_009(self):
        with allure.step("查询fx order"):
            data = {
                "pagination_request": {
                    "page_no": 1,
                    "page_size": 10
                },
                "sort_request": {
                    "field": "id",
                    "order": "desc"
                },
                "order_id": "af2e4d99-20e7-4c06-b587-352b0f42986c"
            }
        with allure.step("调用接口"):
            r = session.request('POST', url='{}/operatorapi/cfx/order/internal/search'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'orders' in r.text, "查询order错误，返回值是{}".format(r.text)

    @allure.title('test_rebalance_010')
    @allure.description('创建fx order')
    def test_rebalance_010(self):
        with allure.step("创建fx order"):
            data = {
                "fx_buy": {
                    "currency": "GBP",
                    "amount": "2593.02",
                    "money_house_account_id": "9e4115c1-2bf3-11ec-880c-227d37e22e6a",
                    "tx_id": generate_string(16),
                    "value_date": "2021-12-22"
                },
                "fx_sell": {
                    "tx_id": generate_string(16),
                    "money_house_account_id": "3a3b80e8-f04e-11eb-9e63-ba224deb3be4",
                    "amount": "0.05390359",
                    "currency": "BTC",
                    "value_date": "2021-12-22"
                },
                "fee": {
                    "fee_type": 2,
                    "tx_id": generate_string(16),
                    "amount": "2.25",
                    "currency": "GBP",
                    "value_date": "2021-12-22",
                    "money_house_account_id": "9e4115c1-2bf3-11ec-880c-227d37e22e6a"
                },
                "counterparty_enum": 98,
                "created_by": "system",
                "updated_by": "system"
            }
        with allure.step("调用接口"):
            r = session.request('POST', url='{}/operatorapi/cfx/order/internal/create'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'order_id' in r.text, "创建order错误，返回值是{}".format(r.text)
