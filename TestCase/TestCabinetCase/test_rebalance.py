from Function.api_function import *
from Function.operate_sql import *


# operate相关cases
class TestRebalanceApi:

    # 初始化class
    def setup_method(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')

    @allure.title('test_rebalance_001 创建单边匹配的rebalance order')
    def test_rebalance_001(self):
        with allure.step("测试数据"):
            data = {
                "orders":
                    [
                        {
                            "value_date": "2021-12-17",
                            "order_type_enum": 2,
                            "counterparty_txn_id": "1233f1226",
                            "money_house_id": "MoneyHouseTypeBinanceDGTLT",
                            "currency": "BNB",
                            "principal": "110",
                            "fee_detail": {
                                "amount": "0",
                                "cost_type": 0
                            },
                            "operator": "alan",
                            "txn_hash": "txhash1224f1115",
                            "money_house_account_id": "98ca2442-5801-11ec-ae48-fec3d14991d2",
                            "order_id": ""
                        },
                        {
                            "order_id": "59e8407c-5e31-43cf-b560-5d8d67709c5d"
                        }
                    ]
            }
        with allure.step("调用接口"):
            r = session.request('POST', url='{}/operatorapi/orders/rebalance/create'.format(operateUrl), data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'accessToken' in r.text, "管理员账户登录错误，返回值是{}".format(r.text)


