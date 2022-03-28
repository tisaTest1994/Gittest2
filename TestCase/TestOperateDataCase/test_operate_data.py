from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api core 相关 testcases")
class TestOperateDataApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_001')
    @allure.description('生成deposit return 测试数据')
    def test_001(self):
        data = {
            "subject": "TRANSACTION:GBP:80724c67-17eb-467b-9f50-b92c83564010",
            "timestamp": "2021-12-22T05:40:56.000Z",
            "account_id": 28038,
            "transactions": [
                {
                    "id": "1985386b-1487-4b56-b992-3eb64f6a3306",
                    "from": "Jamyues Leoie",
                    "iban": "GB33BCPY04054100003157",
                    "credit": True,
                    "currency": "GBP",
                    "bank_name": "",
                    "reference": "JFSQ27123",
                    "sort_code": "",
                    "timestamp": "2021-12-22T05:40:56.000Z",
                    "account_name": "Jamyues Leoie",
                    "bank_country": "",
                    "amount_actual": 0.13,
                    "account_number": "",
                    "notes_external": "",
                    "account_address": "",
                    "amount_instructed": 0.12
                }
            ]
        }
        r = session.request('POST', url='http://webhook.latibac.com/mh/bcb/events_callback', data=json.dumps(data), headers={'content-type': 'application/json'})
        print(r.text)