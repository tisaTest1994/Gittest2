from Function.api_function import *
from Function.operate_sql import *


# Cabtial Pay相关cases
class TestCabitalPayApi:
    url = get_json()['cabital_pay'][get_json()['env']]['url']
    headers = {
        "Content-Type": "application/json"
    }

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_cabital_pay_001')
    @allure.description('创建订单')
    def test_cabital_pay_001(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                "purchase_amount": "100.23",
                "payment_currency": "USDT",
                "payment_amount": "",
                "network": "ETH",
                "valid_time": 0,
                "fee_paid_by": "Merchant",
                "payment_method": "OnChain",
                "success_url": "https://callback.cabital.com/success",
                "failed_url": "https://callback.cabital.com/failed",
                "processing_url": "https://callback.cabital.com/processing",
                "customer": {
                    "id": "04bcddc9-f112-4cd0-92c4-01553ca8c898",
                    "type": "Individual",
                    "name": "CASON STEIN",
                    "email": "lee@cabital.com",
                    "phone": {
                        "country_code": "+1",
                        "number": "123456789"
                    }
                },
                "purchase_order": {
                    "order_id": "565edff3-7a8f-4df5-8595-a56105d60894",
                    "items": [
                        {
                            "name": "ipad",
                            "quantity": 1,
                            "unit_price": "1000.08",
                            "url": "https://cabital.com"
                        }
                    ]
                },
                "metadata": "string"
            }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/v1/payments', key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data), headers=self.headers)
            print(self.headers)
            print(r.status_code)
            print(r.text)
