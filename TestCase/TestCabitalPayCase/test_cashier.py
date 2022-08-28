from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api account 相关 testcases")
class TestCashierApi:
    url = get_json()['cabital_pay'][get_json()['env']]['url']
    headers = {
        "Content-Type": "application/json"
    }

    # 初始化class
    def setup_method(self):
        pass

    @allure.title('test_cashier_001')
    @allure.description('获取商户logo和name')
    def test_cashier_001(self):
        with allure.step("创建好的订单编号"):
            payment_id = "0ad7d01a-09b9-4845-8d91-5f1df6a9010f"
            with allure.step("获取商户logo和name"):
                r = session.request('GET', url='{}/api/v1/cashier/config/{}'.format(self.url, payment_id),
                                    headers=self.headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['merchant']['logo'] == 'qaLogo', "获取商户logo和name错误，返回值是{}".format(r.text)

    @allure.title('test_cashier_002')
    @allure.description('获取交易详情')
    def test_cashier_002(self):
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments', key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
            with allure.step("获取交易详情"):
                r = session.request('GET', url='{}/api/v1/cashier/payment/{}'.format(self.url, payment_id),
                                    headers=self.headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['status'] == 'Pending', "获取交易详情错误，返回值是{}".format(r.text)

    @allure.title('test_cashier_003')
    @allure.description('使用不存在的payment_id获取交易详情')
    def test_cashier_003(self):
        with allure.step("创建好的订单编号"):
            payment_id = "05e76a4c-7c8c-4101-b517-f072e2ce13b3"
            with allure.step("获取交易详情"):
                r = session.request('GET', url='{}/api/v1/cashier/payment/{}'.format(self.url, payment_id),
                                    headers=self.headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cashier_004')
    @allure.description('已经有收款地址的payment_id再分配收款地址')
    def test_cashier_004(self):
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments',
                                                key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data),
                                headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
            with allure.step("已经有收款地址的payment_id再分配收款地址"):
                data = {
                    "payment_id": payment_id,
                    "code": "USDT",
                    "chain": "TRX"
                }
                r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                    headers=self.headers, data=json.dumps(data))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 500, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cashier_005')
    @allure.description('无收款地址的payment_id再分配收款地址')
    def test_cashier_005(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                "purchase_amount": "100.23",
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments',
                                                key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data),
                                headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
            with allure.step("无收款地址的payment_id再分配收款地址"):
                data = {
                    "payment_id": payment_id,
                    "code": "USDT",
                    "chain": "TRX"
                }
                r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                    headers=self.headers, data=json.dumps(data))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['address'] is not None, "无收款地址的payment_id再分配收款地址错误，返回值是{}".format(r.text)

    @allure.title('test_cashier_006')
    @allure.description('使用不存在的payment_id再分配收款地址')
    def test_cashier_006(self):
        payment_id = '123131231231231'
        with allure.step("已经有收款地址的payment_id再分配收款地址"):
            data = {
                "payment_id": payment_id,
                "code": "USDT",
                "chain": "TRX"
            }
            r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                headers=self.headers, data=json.dumps(data))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cashier_007')
    @allure.description('无收款地址的payment_id再分配收款地址使用范围之外的币种')
    def test_cashier_007(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                "purchase_amount": "100.23",
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments',
                                                key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data),
                                headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
            with allure.step("无收款地址的payment_id再分配收款地址使用范围之外的币种"):
                data = {
                    "payment_id": payment_id,
                    "code": "BNB",
                    "chain": "TRX"
                }
                r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                    headers=self.headers, data=json.dumps(data))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 500, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cashier_008')
    @allure.description('无收款地址的payment_id再分配收款地址使用范围之外的链')
    def test_cashier_008(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                "purchase_amount": "100.23",
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments',
                                                key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data),
                                headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
            with allure.step("无收款地址的payment_id再分配收款地址使用范围之外的链"):
                data = {
                    "payment_id": payment_id,
                    "code": "USDT",
                    "chain": "TRX1"
                }
                r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                    headers=self.headers, data=json.dumps(data))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['code'] == "301001", "无收款地址的payment_id再分配收款地址使用范围之外的链错误，返回值是{}".format(r.text)

    @allure.title('test_cashier_009')
    @allure.description('使用过期的payment_id再分配收款地址')
    def test_cashier_009(self):
        payment_id = "0ad7d01a-09b9-4845-8d91-5f1df6a9010f"
        with allure.step("已经有收款地址的payment_id再分配收款地址"):
            data = {
                "payment_id": payment_id,
                "code": "USDT",
                "chain": "TRX"
            }
            r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                headers=self.headers, data=json.dumps(data))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 500, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cashier_010')
    @allure.description('查询订单缺少chain')
    def test_cashier_010(self):
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments', key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
        with allure.step("查询订单缺少chain"):
            data = {
                "payment_id": payment_id,
                "code": "USDT",
            }
            r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                headers=self.headers, data=json.dumps(data))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == "301001", "查询订单缺少chain错误，返回值是{}".format(r.text)

    @allure.title('test_cashier_011')
    @allure.description('查询订单缺少code')
    def test_cashier_011(self):
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
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST', url='/api/v1/payments', key='cabital pay', nonce=nonce, body=json.dumps(data))
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('POST', url='{}/api/v1/payments'.format(self.url), data=json.dumps(data), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)
        with allure.step("创建好的订单编号"):
            payment_id = r.json()['payment_id']
        with allure.step("查询订单缺少code"):
            data = {
                "payment_id": payment_id,
                "chain": "TRX"
            }
            r = session.request('POST', url='{}/api/v1/cashier/payment/address/allocate'.format(self.url),
                                headers=self.headers, data=json.dumps(data))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == "301000", "查询订单缺少code错误，返回值是{}".format(r.text)



