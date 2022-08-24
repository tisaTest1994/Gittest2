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

    @allure.title('test_cabital_pay_002')
    @allure.description('创建订单只留必传参数')
    def test_cabital_pay_002(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                "purchase_amount": "100.23",
                "success_url": "https://callback.cabital.com/success",
                "failed_url": "https://callback.cabital.com/failed",
                "processing_url": "https://callback.cabital.com/processing",
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
            assert r.json()['payment_id'] is not None, "创建订单只留必传参数错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_003')
    @allure.description('创建订单必传参数缺失')
    def test_cabital_pay_003(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "GBP",
                #"purchase_amount": "100.23",
                "success_url": "https://callback.cabital.com/success",
                "failed_url": "https://callback.cabital.com/failed",
                "processing_url": "https://callback.cabital.com/processing",
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
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['error_code'] == 100001, "创建订单必传参数缺失错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_004')
    @allure.description('使用同一reference_id重复创建订单')
    def test_cabital_pay_004(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": "NZxNU1GGBzOeKErL8HVSkDT8KZkTpj",
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['error_code'] == 100002, "使用同一reference_id重复创建订单错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_005')
    @allure.description('purchase_currency传入config不支持的币种')
    def test_cabital_pay_005(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "VND",
                "purchase_amount": "10000.23",
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['error_code'] == 100007, "purchase_currency传入config不支持的币种错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_006')
    @allure.description('purchase_amount使用超过最大值')
    def test_cabital_pay_006(self):
        with allure.step("确定币种"):
            for i in get_json(file='cabital_pay_config.json')['purchase_config']['purchase_currencies']:
                purchase_amount = i['limit']['max']
                if purchase_amount == '-1':
                    continue
                else:
                    purchase_amount = float(purchase_amount) + 10
                with allure.step("创建订单data"):
                    data = {
                        "reference_id": generate_string(30),
                        "purchase_currency": i['symbol'],
                        "purchase_amount": str(purchase_amount),
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
                        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['error_code'] == 100005, "purchase_amount使用超过最大值错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_007')
    @allure.description('purchase_amount使用小于最小值')
    def test_cabital_pay_007(self):
        with allure.step("确定币种"):
            for i in get_json(file='cabital_pay_config.json')['purchase_config']['purchase_currencies']:
                purchase_amount = i['limit']['min']
                if purchase_amount == '-1':
                    continue
                else:
                    purchase_amount = float(purchase_amount) - 0.01
                with allure.step("创建订单data"):
                    data = {
                        "reference_id": generate_string(30),
                        "purchase_currency": i['symbol'],
                        "purchase_amount": str(purchase_amount),
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
                        assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['error_code'] == 100004, "purchase_amount使用超过最大值错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_008')
    @allure.description('payment_currency传入config不支持的币种')
    def test_cabital_pay_008(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "EUR",
                "purchase_amount": "1000",
                "payment_currency": "BNB",
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['error_code'] == 100007, "payment_currency传入config不支持的币种错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_009')
    @allure.description('传入不支持的payment_method，目前只有OnChain')
    def test_cabital_pay_009(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "EUR",
                "purchase_amount": "1000",
                "payment_currency": "USDT",
                "payment_amount": "",
                "network": "ETH",
                "valid_time": 0,
                "fee_paid_by": "Merchant",
                "payment_method": "DJDJ",
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
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['error_code'] == 100001, "传入不支持的payment_method错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_010')
    @allure.description('指定了payment currency，指定了Network，接口返回参数中包含支付地址信息和自动补全payment amount 金额')
    def test_cabital_pay_010(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "EUR",
                "purchase_amount": "1000",
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
                assert r.json()['crypto_address'] != '', "指定了payment currency，指定了Network，接口返回参数中包含支付地址信息错误，返回值是{}".format(r.text)
                assert r.json()['payment_amount'] != '', "自动补全payment amount 金额错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_011')
    @allure.description('未指定payment currency，接口返回参数中无支付地址信息')
    def test_cabital_pay_011(self):
        with allure.step("创建订单data"):
            data = {
                "reference_id": generate_string(30),
                "purchase_currency": "EUR",
                "purchase_amount": "1000",
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
                assert r.json()['crypto_address'] == '', "指定了payment currency，指定了Network，接口返回参数中包含支付地址信息错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_012')
    @allure.description('交易详情payment_id不存在')
    def test_cabital_pay_012(self):
        payment_id = generate_string(20)
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/payments/{}'.format(payment_id), key='cabital pay', nonce=nonce)
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('GET', url='{}/api/v1/payments/{}'.format(self.url, payment_id), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_cabital_pay_013')
    @allure.description('检查查询订单的信息和创建订单相同')
    def test_cabital_pay_013(self):
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
        payment_id = r.json()['payment_id']
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/payments/{}'.format(payment_id), key='cabital pay', nonce=nonce)
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('GET', url='{}/api/v1/payments/{}'.format(self.url, payment_id), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['status'] == 'Pending', "创建订单只会pending错误，返回值是{}".format(r.text)

    @allure.title('test_cabital_pay_014')
    @allure.description('使用不属于本商户的payment_id查询订单')
    def test_cabital_pay_014(self):
        payment_id = '3d3676eb-a3f9-4bf8-8958-c222f692f716'
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/payments/{}'.format(payment_id), key='cabital pay', nonce=nonce)
            self.headers['ACCESS-KEY'] = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            self.headers['ACCESS-SIGN'] = sign
            self.headers['ACCESS-TIMESTAMP'] = str(unix_time)
            self.headers['ACCESS-NONCE'] = nonce
        with allure.step("创建订单"):
            r = session.request('GET', url='{}/api/v1/payments/{}'.format(self.url, payment_id), headers=self.headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 404, "http 状态码不对，目前状态码是{}".format(r.status_code)

