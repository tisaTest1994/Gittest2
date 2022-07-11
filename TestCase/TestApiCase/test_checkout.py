from Function.api_function import *
from Function.operate_sql import *
from Function.operate_excel import *


@allure.feature("Check out 相关 testcases")
class TestCheckoutApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_check_out_001')
    @allure.description('打开数字货币购买画面接口')
    def test_check_out_001(self):
        with allure.step("打开数字货币购买画面"):
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("获取接口返回的所有币种并放入list中"):
            payment_currencies = r.json()['payment_currencies']
        with allure.step("读取product limit中35个币种buy的最大最小值和接口的返回值进行对比"):
            for i in range(0, len(OperateExcel.get_product_limit())):
                # 表里有一个VND deposit（VND的deposit和buy都在acquiring里面）
                if OperateExcel.get_product_limit()[i]['transaction_type'] == 'Buy':
                    logger.info('已验证完成{}个币种的最大最小值,当前检查的币种为{}'.format(i+1, OperateExcel.get_product_limit()[i]['code']))
                    for j in range(0, len(payment_currencies)):
                        if OperateExcel.get_product_limit()[i]['code'] == payment_currencies[j]['code']:
                            assert Decimal(OperateExcel.get_product_limit()[i]['min']) == Decimal(payment_currencies[j]['min']), '币种{}的最小值错误，与product limit表中的值不同。接口返回值为{}'.format(OperateExcel.get_product_limit()[i]['min'], payment_currencies[j]['min'])
                            assert Decimal(OperateExcel.get_product_limit()[i]['max']) == Decimal(payment_currencies[j]['max']), '币种{}的最大值错误，与product limit表中的值不同。接口返回值为{}'.format(OperateExcel.get_product_limit()[i]['min'], payment_currencies[j]['max'])
                            payment_currencies.remove(payment_currencies[j])
                            break
                        else:
                            with allure.step("检查是否prodcut limit中的币种在接口中都已配置"):
                                if j == len(payment_currencies)-1:
                                    assert False, '接口返回的币种不全，与excel中的不同，缺少的币种为{}'.format(OperateExcel.get_product_limit()[i]['code'])
                                else:
                                    j += 1

    # @allure.title('test_check_out_002')
    # @allure.description('buy交易所有币种精度检查')
    # def test_check_out_002(self):

    # 没写完
    # @allure.title('test_check_out_003')
    # @allure.description('同payment with的卡，显示同上一笔成功的buy的货币对(CAD-USDT)')
    # def test_check_out_003(self):
    #     with allure.step("打开数字货币购买画面"):
    #         r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r.status_code)))
    #         logger.info('返回值是{}'.format(str(r.text)))
    #     with allure.step("获取接口返回的所有币种并放入list中"):
    #         payment_currencies = r.json()['payment_currencies']
    #     with allure.step("检查buy currencies及精度配置"):
    #         assert r.json()['buy_currencies']['code'] == 'USDT', 'buy currencies币种错误，接口返回是{}'.format(
    #             r.json()['buy_currencies']['code'])
    #         assert r.json()['buy_currencies']['precision'] == 6, 'buy currencies币种错误，接口返回是{}'.format(
    #             r.json()['buy_currencies']['code'])

    @allure.title('test_check_out_004获取报价')
    @allure.description('获取报价')
    def test_check_out_004(self):
        with allure.step("获取所有报价对"):
            payment_currency_list = []
            pair_list = []
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
            for i in r.json()['payment_currencies']:
                payment_currency_list.append(i['code'])
            for j in payment_currency_list:
                pair_list.append(j + "-USDT")
            for pair in pair_list:
                r2 = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, pair), headers=headers)
                logger.info('当前币种对为{}，接口返回汇率为{}'.format(pair, r2.json()['quote']))
                with allure.step("校验状态码"):
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))

    @allure.title('test_check_out_005获取数字货币购买人信息')
    @allure.description('获取数字货币购买人信息')
    def test_check_out_005(self):
        with allure.step("获取报价"):
            r = session.request('GET', url='{}/acquiring/buy/payer'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['card_holder_name'] == "yilei Wan" and r.json()['billing_address'] != {}, "获取数字货币购买人信息错误，返回值是{}".format(r.json()['card_holder_name'])

    @allure.title('test_check_out_006获取购买数字货币费用-with card')
    @allure.description('获取购买数字货币费用-with card')
    def test_check_out_006(self):
        data = {
            "code": "USD",
            "amount": "100",
            "card": {
                "scheme": "Visa",
                "issuer_country": "GB"
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee']['amount'] == "3.75", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])
            assert r.json()['receivable_amount'] == str(float(data['amount']) - float(r.json()['fee']['amount'])), '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])

    @allure.title('test_check_out_007获取购买数字货币费用，使用不支持的scheme')
    @allure.description('获取购买数字货币费用，使用不支持的scheme')
    def test_check_out_007(self):
        data = {
            "code": "USD",
            "amount": "100",
            "card": {
                "scheme": "UnionPay",
                "issuer_country": "GB"
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['code'] == '101019', '获取购买数字货币费用，使用不支持的scheme错误，接口返回值是{}'.format(r.json()['message'])

    @allure.title('test_check_out_008获取购买数字货币费用-no card')
    @allure.description('获取购买数字货币费用-no card')
    def test_check_out_008(self):
        data = {
            "code": "USD",
            "amount": "100",
            "card": {
                "scheme": "",
                "issuer_country": ""
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee']['amount'] == "3.75", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])
            assert r.json()['receivable_amount'] == str(float(data['amount']) - float(r.json()['fee']['amount'])), '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])

    @allure.title('test_check_out_009获取购买数字货币费用规则-with card')
    @allure.description('获取购买数字货币费用规则-with card')
    def test_check_out_009(self):
        data = {
            "code": "USD",
            "card": {
                "scheme": "Visa",
                "issuer_country": "GB"
            }
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee_rule']['type'] == '1', '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])
            assert r.json()['fee_rule']['percentage_charge_rule']['percentage'] == '3.75', '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['percentage_charge_rule']['percentage'])
            assert r.json()['fee_rule']['formula'] == 'CEILING(x*0.04,2)', '购买数字货币公式错误，接口返回值为{}'.format(r.json()['fee_rule']['percentage_charge_rule']['percentage'])

    @allure.title('test_check_out_010获取购买数字货币费用规则-no card')
    @allure.description('获取购买数字货币费用规则-no card')
    def test_check_out_010(self):
        data = {
            "code": "USD"
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee_rule']['type'] == 1, '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])
            assert r.json()['fee_rule']['percentage_charge_rule'][
                       'percentage'] == '1.85', '购买数字货币手续费错误，接口返回值为{}'.format(
                r.json()['fee_rule']['percentage_charge_rule']['percentage'])
            assert r.json()['fee_rule']['formula'] == 'CEILING(x*0.02,2)', '购买数字货币公式错误，接口返回值为{}'.format(
                r.json()['fee_rule']['percentage_charge_rule']['percentage'])

    @allure.title('test_check_out_011获取购买数字货币费用规则-no card,使用不支持的币种')
    @allure.description('获取购买数字货币费用规则-no card,使用不支持的币种')
    def test_check_out_011(self):
        data = {
            "code": "CNY"
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['code'] == "101019", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])

    @allure.title('test_check_out_012创建数字货币购买交易-payment with card')
    @allure.description('创建数字货币购买交易-payment with card')
    def test_check_out_012(self):
        with allure.step("get token"):
            data = {
                "type": "card",
                "number": "4242424242424242",
                "expiry_month": 6,
                "expiry_year": 2025,
                "name": "Bruce Wayne",
                "cvv": "956",
                "billing_address": {
                    "address_line1": "Checkout.com",
                    "address_line2": "90 Tottenham Court Road",
                    "city": "London",
                    "state": "London",
                    "zip": "W1T 4TJ",
                    "country": "GB"
                }
            }
            headers2 = {
                "Authorization": "Bearer pk_sbox_cqecp4mj36curomekpmzd42cjeg",
                "Content-Type": "application/json"
            }
            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data), headers=headers2)
        with allure.step("校验状态码"):
            assert r.status_code == 201, "http状态码不对，目前状态码是{}".format(r.status_code)
            token = r.json()['token']
            print(token)
        with allure.step("spend 100USD,根据报价，算出buy的金额"):
            spend_amount = '100'
            r3 = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, 'USDT-USD'), headers=headers)
            buy_amount = str(float(spend_amount)*float(r3.json()['quote']['amount']))
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": "USDT",
                    "amount": buy_amount
                },
                "spend": {
                    "code": "USD",
                    "amount": spend_amount
                },
                "quote": {
                    "id": r3.json()['quote']['id'],
                    "amount": r3.json()['quote']['amount'],
                },
                "major_code": "USDT",
                "card": {
                    "type": 1,
                    "token": token,
                    "expiry_month": "4",
                    "expiry_year": "2044",
                    "scheme": "Visa",
                    "last": "4242",
                    "bin": "424242",
                    "card_type": "Credit",
                    "issuer": "JPMORGAN CHASE BANK NA",
                    "issuer_country": "US"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with card"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验返回值"):
            assert r2.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r2.json())
            logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息"):
            with open('checkout.html', 'w') as file:
                file.write(r2.json()['redirect']['url'])

    @allure.title('test_check_out_013创建数字货币购买交易-payment with token')
    @allure.description('创建数字货币购买交易-payment with token')
    def test_check_out_013(self):
        with allure.step("spend 100USD,根据报价，算出buy的金额"):
            spend_amount = '100'
            r3 = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, 'USDT-USD'), headers=headers)
            buy_amount = str(float(spend_amount)*float(r3.json()['quote']['amount']))
        with allure.step("创建数字货币购买交易信息"):
            data = {
                "buy": {
                    "code": "USDT",
                    "amount": buy_amount
                },
                "spend": {
                    "code": "USD",
                    "amount": spend_amount
                },
                "quote": {
                    "id": r3.json()['quote']['id'],
                    "amount": r3.json()['quote']['amount'],
                },
                "major_code": "USDT",
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
                    "issuer_country": "US"
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with token"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验返回值"):
            assert r2.json() != {}, '创建数字货币购买交易-payment with token，接口返回值为{}'.format(r2.json())
            logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息"):
            checkout_html = 'checkout.html'
            f = open(checkout_html, 'w')
            f.write(r2.json()['redirect']['url'])
            f.close()

    # @allure.title('test_check_out_014')
    # @allure.description('创建数字货币购买交易-payment with card不绑卡，检查绑卡状态')
    # def test_check_out_014(self):
    #     with allure.step("get token"):
    #         data = {
    #             "type": "card",
    #             "number": "4242424242424666",
    #             "expiry_month": 6,
    #             "expiry_year": 2025,
    #             "name": "Ting DP319",
    #             "cvv": "956",
    #             "billing_address": {
    #                 "address_line1": "Checkout.com",
    #                 "address_line2": "90 Tottenham Court Road",
    #                 "city": "London",
    #                 "state": "London",
    #                 "zip": "W1T 4TJ",
    #                 "country": "GB"
    #             }
    #         }
    #         headers2 = {
    #             "Authorization": "Bearer pk_sbox_cqecp4mj36curomekpmzd42cjeg",
    #             "Content-Type": "application/json"
    #         }
    #         r = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data), headers=headers2)
    #     with allure.step("校验状态码"):
    #         assert r.status_code == 201, "http状态码不对，目前状态码是{}".format(r.status_code)
    #         token = r.json()['token']
    #         print(token)
    #     with allure.step("spend 100USD,根据报价，算出buy的金额"):
    #         spend_amount = '100'
    #         r3 = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, 'USDT-USD'), headers= ApiFunction.add_headers(account = 'yanting.huang+319@cabital.com'))
    #         buy_amount = str(float(spend_amount)*float(r3.json()['quote']['amount']))
    #     with allure.step("创建数字货币购买交易信息"):
    #         data = {
    #             "buy": {
    #                 "code": "USDT",
    #                 "amount": buy_amount
    #             },
    #             "spend": {
    #                 "code": "USD",
    #                 "amount": spend_amount
    #             },
    #             "quote": {
    #                 "id": r3.json()['quote']['id'],
    #                 "amount": r3.json()['quote']['amount'],
    #             },
    #             "major_code": "USDT",
    #             "card": {
    #                 "type": 1,
    #                 "token": token,
    #                 "expiry_month": "4",
    #                 "expiry_year": "2044",
    #                 "scheme": "Visa",
    #                 "last": "4242",
    #                 "bin": "424242",
    #                 "card_type": "Credit",
    #                 "issuer": "JPMORGAN CHASE BANK NA",
    #                 "issuer_country": "US"
    #             },
    #             "bind_card": False,
    #             "card_holder_name": "DP Ting319",
    #             "billing_address": {
    #                 "country_code": "DE",
    #                 "state": "",
    #                 "city": "3",
    #                 "post_code": "3",
    #                 "street_line_1": "3",
    #                 "street_line_2": ""
    #             },
    #             "nonce": generate_string(30)
    #         }
    #     with allure.step("创建数字货币购买交易-payment with card"):
    #         r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
    #     with allure.step("校验状态码"):
    #         assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
    #     with allure.step("状态码和返回值"):
    #         logger.info('状态码是{}'.format(str(r2.status_code)))
    #         logger.info('返回值是{}'.format(str(r2.text)))
    #     with allure.step("校验返回值"):
    #         assert r2.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r2.json())
    #         logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
    #     with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息"):
    #         with open('checkout.html', 'w') as file:
    #             file.write(r2.json()['redirect']['url'])


    @allure.title('test_check_out_051')
    @allure.description('查询用户使用过的所有卡')
    def test_check_out_051(self):
        with allure.step("查询用户使用过的所有卡"):
            params = {
                'binding': 'false'
            }
            r = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_check_out_052')
    @allure.description('删除用户是用过的卡')
    def test_check_out_052(self):
        with allure.step("删除用户是用过的卡"):
            params = {
                'token_id': 'false'
            }
            r = session.request('DELETE', url='{}/acquiring/cards/{}'.format(env_url, params['token_id']), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)






