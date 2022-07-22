from Function.api_function import *
from Function.operate_sql import *
from Function.operate_excel import *
import webbrowser


@allure.feature("Check out 相关 testcases")
class TestCheckoutApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_check_out_abnormal_001')
    @allure.description('创建数字货币购买交易-payment with token，cvv长度错误')
    def test_check_out_abnormal_001(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "12"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101039', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_002')
    @allure.description('创建数字货币购买交易-payment with token，cvv为空')
    def test_check_out_abnormal_002(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": ""
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101038', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_003')
    @allure.description('创建数字货币购买交易-payment with token，cvv含非数字和字母的字符')
    def test_check_out_abnormal_003(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "10！"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101039', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_004')
    @allure.description('创建数字货币购买交易-payment with token，address_line1为空')
    def test_check_out_abnormal_004(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101047', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_005')
    @allure.description('创建数字货币购买交易-payment with token，address_line1地址长度限制(1-200),使用长度201')
    def test_check_out_abnormal_005(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "112345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101048', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_006')
    @allure.description('创建数字货币购买交易-payment with token，address_line2非必填，检查是否可以为空')
    def test_check_out_abnormal_006(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": ""
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['txn_id'] != {}, 'address_line_2为空进行buy crtpto交易， 交易失败，接口返回值为{}'.format(r2.json())

    @allure.title('test_check_out_abnormal_007')
    @allure.description('创建数字货币购买交易-payment with token，address_line2地址长度限制(1-200),使用长度201')
    def test_check_out_abnormal_007(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": "112345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101049', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_008')
    @allure.description('创建数字货币购买交易-payment with token，city为空')
    def test_check_out_abnormal_008(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": "345",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101043', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_009')
    @allure.description('创建数字货币购买交易-payment with token，city长度大于最大50')
    def test_check_out_abnormal_009(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai1234567890123456789012345678901234567890123467890",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": "345",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101044', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_010')
    @allure.description('创建数字货币购买交易-payment with token，state非必填，检查state为空能否创建buy crypto交易')
    def test_check_out_abnormal_010(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": "345",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['txn_id'] != {}, 'state为空进行buy crtpto交易， 交易失败，接口返回值为{}'.format(r2.json())

    @allure.title('test_check_out_abnormal_011')
    @allure.description('创建数字货币购买交易-payment with token，state长度大于最大50')
    def test_check_out_abnormal_011(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "sichuan1234567890123456789012345678901234567890123467890",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "123",
                    "street_line_2": "345",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101042', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_012')
    @allure.description('创建数字货币购买交易-payment with token，post code长度错误')
    def test_check_out_abnormal_012(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "21000012345678901234567890123456789012345678901234567890",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101046', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_013')
    @allure.description('创建数字货币购买交易-payment with token，post code为空(应不为空)')
    def test_check_out_abnormal_013(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101045', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_014')
    @allure.description('创建数字货币购买交易-payment with token，post code含非数字和字母的字符')
    def test_check_out_abnormal_014(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "!@#",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101046', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_015')
    @allure.description('创建数字货币购买交易-payment with token，country为空(应不为空)')
    def test_check_out_abnormal_015(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha",
                    "zip": "234"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101040', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_016')
    @allure.description('创建数字货币购买交易-payment with token，country长度错误')
    def test_check_out_abnormal_016(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "BMW",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101041', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])

    @allure.title('test_check_out_abnormal_017')
    @allure.description('创建数字货币购买交易-payment with token，非ISO country code')
    def test_check_out_abnormal_017(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-EUR', ccy='spend', country='HK')
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": (str(crypto_list['pairs']).split('-'))[0],
                    "amount": crypto_list['buy_amount']
                },
                "spend": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['spend_amount']
                },
                "quote": {
                    "id": crypto_list['quote_id'],
                    "amount": crypto_list['quote']
                },
                "major_code": crypto_list['major_code'],
                "fee": {
                    "code": (str(crypto_list['pairs']).split('-'))[1],
                    "amount": crypto_list['service_charge']
                },
                "total_amount": crypto_list['total_spend_amount'],
                "card": {
                    "type": 2,
                    "token": "src_eiuwrsam5b3u5gya5vjceotv3q",
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US",
                    "cvv": "100"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "AB",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "xichuanbeilu",
                    "street_line_2": "Sha",
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("校验返回值"):
            assert r2.json()['code'] == '101041', '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json()['code'])