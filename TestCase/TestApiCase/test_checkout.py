import allure

from Function.api_function import *
from Function.operate_sql import *
from Function.operate_excel import *
import webbrowser
import copy


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
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("获取接口返回的所有币种并放入list中"):
            payment_currencies = r.json()['payment_currencies']
        with allure.step("读取product limit中35个币种buy的最大最小值和接口的返回值进行对比"):
            for i in range(0, len(OperateExcel.get_product_limit())):
                # 表里有一个VND deposit（VND的deposit和buy都在acquiring里面）
                if OperateExcel.get_product_limit()[i]['transaction_type'] == 'Buy':
                    logger.info(
                        '已验证完成{}个币种的最大最小值,当前检查的币种为{}'.format(i + 1, OperateExcel.get_product_limit()[i]['code']))
                    for j in range(0, len(payment_currencies)):
                        if OperateExcel.get_product_limit()[i]['code'] == payment_currencies[j]['code']:
                            assert Decimal(OperateExcel.get_product_limit()[i]['min']) == Decimal(
                                payment_currencies[j]['min']), '币种{}的最小值错误，与product limit表中的值不同。接口返回值为{}'.format(
                                OperateExcel.get_product_limit()[i]['min'], payment_currencies[j]['min'])
                            assert Decimal(OperateExcel.get_product_limit()[i]['max']) == Decimal(
                                payment_currencies[j]['max']), '币种{}的最大值错误，与product limit表中的值不同。接口返回值为{}'.format(
                                OperateExcel.get_product_limit()[i]['min'], payment_currencies[j]['max'])
                            payment_currencies.remove(payment_currencies[j])
                            break
                        else:
                            with allure.step("检查是否prodcut limit中的币种在接口中都已配置"):
                                if j == len(payment_currencies) - 1:
                                    assert False, '接口返回的币种不全，与excel中的不同，缺少的币种为{}'.format(
                                        OperateExcel.get_product_limit()[i]['code'])
                                else:
                                    j += 1

    @allure.title('test_check_out_002')
    @allure.description('buy交易所有币种精度检查')
    def test_check_out_002(self):
        with allure.step("打开数字货币购买画面"):
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("读取Checkout currency中35个币种精度和接口的返回值进行对比"):
            path = os.path.split(os.path.realpath(__file__))[0] + '/../../Resource/Checkout currency.xlsx'
            row = OperateExcel.get_excel_sheet_all_row_number('Currency', path=path)
            precision_list = []
            for i in range(1, row):
                line = OperateExcel.get_excel_sheet_row('Currency', i, path=path)
                if 'empty' not in str(line[2]):
                    precision_list.append(
                        {str(line[0]).split(':')[1].replace("'", ""): int(float(str(line[2]).split(':')[1]))})
            for y in precision_list:
                for z in r.json()['payment_currencies']:
                    if list(y.keys())[0] == z['code']:
                        assert y[str(list(y.keys())[0])] == z['precision'], '{}币种精度检查错误'.format(z['code'])

    @allure.title('test_check_out_003')
    @allure.description('无成功的buy的交易，检查默认币种对及排序')
    def test_check_out_003(self):
        with allure.step("打开数字货币购买画面"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account='yanting.huang+4@cabital.com')
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
        with allure.step("把返回的币种放入列表中"):
            payment_currencies = r.json()['payment_currencies']
            buy_crypto_currency = []
            for i in range(0, len(payment_currencies)):
                buy_crypto_currency.append(payment_currencies[i]['code'])
        with allure.step("检查默认币种是否是EUR"):
            assert buy_crypto_currency[0] == 'EUR', '无成功的buy的交易，默认币种错误，接口返回为{}'.format(buy_crypto_currency[0])
        with allure.step("除去EUR，其他币种按a-z排序"):
            buy_crypto_currency.remove(buy_crypto_currency[0])
            buy_crypto_currency_original = copy.copy(buy_crypto_currency)
            buy_crypto_currency.sort()
            assert buy_crypto_currency == buy_crypto_currency_original, '币种默认排序错误，接口返回为{}'.format(buy_crypto_currency)

    @allure.title('test_check_out_004')
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

    @allure.title('test_check_out_005')
    @allure.description('获取数字货币购买人信息')
    def test_check_out_005(self):
        with allure.step("获取报价"):
            r = session.request('GET', url='{}/acquiring/buy/payer'.format(env_url), headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['card_holder_name'] == "yilei Wan" and r.json()[
                'billing_address'] != {}, "获取数字货币购买人信息错误，返回值是{}".format(r.json()['card_holder_name'])

    @allure.title('test_check_out_006')
    @allure.description('获取购买数字货币费用-with card(None EEA)')
    def test_check_out_006(self):
        data = {
            "code": "GBP",
            "amount": "100",
            "card": {
                "scheme": "Visa",
                "issuer_country": "BGN"
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee']['amount'] == "3.8", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])

    @allure.title('test_check_out_007')
    @allure.description('获取购买数字货币费用-with card(EEA)')
    def test_check_out_007(self):
        data = {
            "code": "HRK",
            "amount": "100",
            "card": {
                "scheme": "Visa",
                "issuer_country": "HR"
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee']['amount'] == "1.9", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])

    @allure.title('test_check_out_008')
    @allure.description('获取购买数字货币费用，使用不支持的scheme')
    def test_check_out_008(self):
        data = {
            "code": "USD",
            "amount": "100",
            "card": {
                "scheme": "UnionPay",
                "issuer_country": "GB"
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['code'] == '101020', '获取购买数字货币费用，使用不支持的scheme错误，接口返回值是{}'.format(r.json()['message'])

    @allure.title('test_check_out_009')
    @allure.description('获取购买数字货币费用-no card')
    def test_check_out_009(self):
        data = {
            "code": "USD",
            "amount": "100",
            "card": {
                "scheme": "",
                "issuer_country": ""
            }
        }
        with allure.step("获取购买数字货币费用"):
            r = session.request('POST', url='{}/acquiring/buy/fee'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee']['amount'] == "1.9", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee']['amount'])

    @allure.title('test_check_out_010')
    @allure.description('获取购买数字货币费用规则-with card')
    def test_check_out_010(self):
        data = {
            "code": "USD",
            "card": {
                "scheme": "Visa",
                "issuer_country": "US"
            }
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee_rule']['type'] == 1, '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])
            assert r.json()['fee_rule']['percentage_charge_rule']['percentage'] == '3.8', '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['percentage_charge_rule']['percentage'])
            assert r.json()['fee_rule']['formula'] == 'CEILING(x*0.038,2)', '购买数字货币公式错误，接口返回值为{}'.format(r.json()['fee_rule']['percentage_charge_rule']['percentage'])

    @allure.title('test_check_out_011')
    @allure.description('获取购买数字货币费用规则-no card')
    def test_check_out_011(self):
        data = {
            "code": "USD"
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['fee_rule']['type'] == 1, '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])
            assert r.json()['fee_rule']['percentage_charge_rule'][
                       'percentage'] == '1.9', '购买数字货币手续费错误，接口返回值为{}'.format(
                r.json()['fee_rule']['percentage_charge_rule']['percentage'])
            assert r.json()['fee_rule']['formula'] == 'CEILING(x*0.019,2)', '购买数字货币公式错误，接口返回值为{}'.format(
                r.json()['fee_rule']['percentage_charge_rule']['percentage'])

    @allure.title('test_check_out_012')
    @allure.description('获取购买数字货币费用规则-no card,使用不支持的币种')
    def test_check_out_012(self):
        data = {
            "code": "CNY"
        }
        with allure.step("获取购买数字货币费用规则"):
            r = session.request('POST', url='{}/acquiring/buy/fee/rule'.format(env_url), data=json.dumps(data),
                                headers=headers)
        with allure.step("校验状态码"):
            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验返回值"):
            assert r.json()['code'] == "101025", '购买数字货币手续费错误，接口返回值为{}'.format(r.json()['fee_rule']['type'])

    @allure.title('test_check_out_013')
    @allure.description('创建数字货币购买交易-payment with card')
    def test_check_out_013(self):
        with allure.step("get token"):
            data = {
                "type": "card",
                "number": "4242424242424242",
                "expiry_month": 6,
                "expiry_year": 2025,
                "name": "Bruce Wayne",
                "cvv": "100",
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
            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data),
                                headers=headers2)
        with allure.step("校验状态码"):
            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(r.status_code)
            token = r.json()['token']
            dic = json.loads(r.text)
            if "issuer" in dic.keys():
                issuer = dic["issuer"]
            else:
                issuer = ''
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(100, pairs='USDT-USD', ccy='buy', country='HK')
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
                    "type": 1,
                    "token": token,
                    "expiry_month": str(r.json()['expiry_month']),
                    "expiry_year": str(r.json()['expiry_year']),
                    "scheme": str(r.json()['scheme']),
                    "last": str(r.json()['last4']),
                    "bin": str(r.json()['bin']),
                    "card_type": str(r.json()['card_type']),
                    "issuer": issuer,
                    "issuer_country": str(r.json()['issuer_country'])
                },
                "bind_card": True,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30),
            }
        with allure.step("创建数字货币购买交易-payment with card"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验返回值"):
            assert r2.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r2.json())
            logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息,不需要了暂时先不删"):
            with open('checkout.html', 'w') as file:
                file.write(r2.json()['redirect']['url'])
        # with allure.step("打开3ds"):
        #     webbrowser.open(r2.json()['redirect']['url'])
        #     sleep(15)

    @allure.title('test_check_out_014')
    @allure.description('创建数字货币购买交易-payment with token')
    def test_check_out_014(self):
        with allure.step("获取交易数据"):
            crypto_list = ApiFunction.get_buy_crypto_list(200, pairs='USDT-BRL', ccy='buy', country='HK')
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
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30),
                "check_amount": False
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
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息,不需要了暂时先不删"):
            with open('checkout.html', 'w') as file:
                file.write(r2.json()['redirect']['url'])
        # with allure.step("打开3ds"):
        #     webbrowser.open(r2.json()['redirect']['url'])
        #     sleep(15)

    @allure.title('test_check_out_015')
    @allure.description('创建数字货币购买交易-payment with token，金额小于最小值或大于最大值')
    def test_check_out_015(self):
        with allure.step('从接口获得所有buy crypto的spend币种'):
            for i in ApiFunction.get_buy_crypto_currency(partner='woo', type='all'):
                with allure.step('获取法币{}最小和最大提现金额'.format(i.split('-')[1])):
                    amount_list_limit = ApiFunction.get_buy_crypto_limit(currency=i.split('-')[1])
                    amount_list = []
                with allure.step('根据币种精度计算法币{}小于最小和大于最大提现金额'.format(i.split('-')[1])):
                    r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
                    for z in r.json()['payment_currencies']:
                        if z['code'] == i.split('-')[1]:
                            if z['precision'] == 0:
                                amount_change = 1
                            elif z['precision'] == 2:
                                amount_change = 0.01
                            min_less = Decimal(str(amount_list_limit[0])) - Decimal(str(amount_change))
                            max_more = Decimal(str(amount_list_limit[1])) + Decimal(str(amount_change))
                    amount_list.append(str(min_less))
                    amount_list.append(str(max_more))
                with allure.step("创建数字货币购买交易币种对:{}".format(i)):
                    for amount in amount_list:
                        crypto_list = ApiFunction.get_buy_crypto_list(amount, pairs=i, ccy='spend', country='TH')
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
                                "street_line_1": "Shanghai",
                                "street_line_2": "Shab"
                            },
                            "nonce": generate_string(30)
                        }
                        with allure.step("创建数字货币购买交易{}-payment with token，金额小于最小值或大于最大值".format(i)):
                            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data),
                                                 headers=headers)
                        with allure.step("校验状态码"):
                            assert r2.status_code == 400, "http 状态码不对，目前状态码是{}".format(r2.status_code)
                        with allure.step("校验返回值"):
                            if amount == amount_list[0]:
                                print('当前交易币种对为{}'.format(i))
                                assert r2.json()['code'] == '101007', "创建数字货币购买交易{}-payment with token-(提现金额小于最小金额)返回值错误，当前返回值是{}".format(i, r2.text)
                            else:
                                assert r2.json()['code'] == '101006', "创建数字货币购买交易{}-payment with token-(提现金额大于最大金额)返回值错误，当前返回值是{}".format(r2.text)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r2.status_code)))
                            logger.info('返回值是{}'.format(str(r2.text)))

    @allure.title('test_check_out_016')
    @pytest.mark.skip(reason='要打开浏览器验证3ds，测试机上不能完成，仅可本地验证')
    @allure.description('创建数字货币购买交易-payment with card不绑卡，检查绑卡状态')
    def test_check_out_016(self):
        with allure.step("get token"):
            data = {
                "type": "card",
                "number": "4543474002249996",
                "expiry_month": 6,
                "expiry_year": 2045,
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
            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data),
                                headers=headers2)
        with allure.step("校验状态码"):
            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(r.status_code)
            token = r.json()['token']
        with allure.step("算出交易金额"):
            crypto_list = ApiFunction.get_buy_crypto_list(16, pairs='USDT-USD', ccy='buy', country='HK')
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
                    "type": 1,
                    "token": token,
                    "expiry_month": str(r.json()['expiry_month']),
                    "expiry_year": str(r.json()['expiry_year']),
                    "scheme": str(r.json()['scheme']),
                    "last": str(r.json()['last4']),
                    "bin": str(r.json()['bin']),
                    "card_type": str(r.json()['card_type']),
                    "issuer": str(r.json()['issuer']),
                    "issuer_country": str(r.json()['issuer_country'])
                },
                "bind_card": False,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30)
            }
        with allure.step("创建数字货币购买交易-payment with card"):

            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验返回值"):
            assert r2.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r2.json())
            logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息,不需要了暂时先不删"):
            with open('checkout.html', 'w') as file:
                file.write(r2.json()['redirect']['url'])
        with allure.step("打开3ds"):
            webbrowser.open(r2.json()['redirect']['url'])
            sleep(20)
        with allure.step("检易完成后，检查绑卡状态"):
            params = {
                'binding': 'false'
            }
            r4 = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
            for i in r4.json()['cards']:
                if i['token'] == 'src_jfqatucdnnbexp2whhgrybdns4':
                    assert i['is_deleted'] is True, '创建数字货币购买交易-payment with card不绑卡，绑卡状态错误，接口返回为{}'.format(
                        i['is_deleted'])

    @allure.title('test_check_out_017')
    @pytest.mark.skip(reason='要打开浏览器验证3ds，测试机上不能完成，仅可本地验证')
    @allure.description('创建数字货币购买交易-payment with card完成交易后，同payment with的卡，显示同上一笔成功的buy的货币对')
    def test_check_out_017(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yanting.huang+309@cabital.com')
        with allure.step("get token"):
            data = {
                "type": "card",
                "number": "4543474002249996",
                "expiry_month": 6,
                "expiry_year": 2045,
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
            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data),
                                headers=headers2)
        with allure.step("校验状态码"):
            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(r.status_code)
            token = r.json()['token']
        with allure.step("随机币种，获取交易数据"):
            buy_pair = ApiFunction.get_buy_crypto_currency(type='random')[0]
            spend_code = buy_pair.split('-')[1]
            spend_amount_limit = ApiFunction.get_buy_crypto_limit(currency=spend_code)
            spend_amount = random.randint(int(spend_amount_limit[0])+int(10), int(spend_amount_limit[0])+int(100))
            crypto_list = ApiFunction.get_buy_crypto_list(spend_amount, pairs=buy_pair, ccy='spend', country='HK')
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
                    "type": 1,
                    "token": token,
                    "expiry_month": str(r.json()['expiry_month']),
                    "expiry_year": str(r.json()['expiry_year']),
                    "scheme": str(r.json()['scheme']),
                    "last": str(r.json()['last4']),
                    "bin": str(r.json()['bin']),
                    "card_type": str(r.json()['card_type']),
                    "issuer": str(r.json()['issuer']),
                    "issuer_country": str(r.json()['issuer_country'])
                },
                "bind_card": False,
                "card_holder_name": "yilei Wan",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30),
                "check_amount": False
            }
        with allure.step("创建数字货币购买交易-payment with card"):
            r2 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            logger.info('返回值是{}'.format(str(r2.text)))
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r2.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r2.status_code)))
            logger.info('返回值是{}'.format(str(r2.text)))
        with allure.step("校验返回值"):
            assert r2.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r2.json())
            logger.info('transaction id是{}'.format(str(r2.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息,不需要了暂时先不删"):
            with open('checkout.html', 'w') as file:
                file.write(r2.json()['redirect']['url'])
        with allure.step("打开3ds"):
            webbrowser.open(r2.json()['redirect']['url'])
            sleep(30)
        with allure.step("交易完成后完成后，检查默认币种显是否正确"):
            r3 = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
            assert r3.json()["payment_currencies"][0]['code'] == spend_code
        with allure.step("交易完成后完成后，检查获取的货币对汇率是否正确"):
            r3 = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
            assert buy_pair + ':BuyTxn' in r3.json()["quote"]['id']

    @allure.title('test_check_out_018')
    @pytest.mark.skip(reason='要打开浏览器验证3ds，测试机上不能完成，仅可本地验证')
    @allure.description('创建数字货币购买交易-payment with card完成交易后，同payment with的卡，显示同上一笔成功的buy的货币对')
    def test_check_out_018(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yanting.huang+16@cabital.com',
                                                                             password='Zcdsw123')
        with allure.step("查询用户使用过的所有卡"):
            params = {
                'binding': 'false'
            }
            r = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
            token_id = r.json()['cards'][0]['id']
        with allure.step("删除用户是用过的卡"):
            params = {
                'token_id': token_id
            }
            r2 = session.request('DELETE', url='{}/acquiring/cards/{}'.format(env_url, params['token_id']),
                                 headers=headers, params=params)
        with allure.step("校验状态码"):
            assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("查询删除卡的状态"):
            params = {
                'binding': 'false'
            }
            r3 = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
            for i in r3.json()['cards']:
                if i['id'] == token_id:
                    assert i['is_deleted'] is True, '删除绑定的卡，预期参数错误，接口返回{}'.format(i['is_deleted'])
        with allure.step("再次进行交易时选择之前删除的卡进行交易（勾选绑卡）"):
            data = {
                "type": "card",
                "number": "5436031030606378",
                "expiry_month": 6,
                "expiry_year": 2025,
                "name": "Bruce Wayne",
                "cvv": "257",
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
            r4 = session.request('POST', url='https://api.sandbox.checkout.com/tokens', data=json.dumps(data),
                                 headers=headers2)
        with allure.step("校验状态码"):
            assert r4.status_code == 201, "http状态码不对，目前状态码是{}".format(r.status_code)
            token = r4.json()['token']
        with allure.step("根据报价，算出buy的金额"):
            crypto_list = ApiFunction.get_buy_crypto_list(10, pairs='USDT-BRL', ccy='buy', country='HK')
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
                    "type": 1,
                    "token": token,
                    "expiry_month": str(r.json()['expiry_month']),
                    "expiry_year": str(r.json()['expiry_year']),
                    "scheme": str(r.json()['scheme']),
                    "last": str(r.json()['last4']),
                    "bin": str(r.json()['bin']),
                    "card_type": str(r.json()['card_type']),
                    "issuer": str(r.json()['issuer']),
                    "issuer_country": str(r.json()['issuer_country'])
                },
                "bind_card": True,
                "card_holder_name": "Ting DP319",
                "billing_address": {
                    "country_code": "CN",
                    "state": "",
                    "city": "shanghai",
                    "post_code": "210000",
                    "street_line_1": "Shanghai",
                    "street_line_2": "Shab"
                },
                "nonce": generate_string(30),
                "check_amount": False
            }
        with allure.step("创建数字货币购买交易-payment with card"):
            r6 = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
        with allure.step("校验状态码"):
            logger.info('返回值是{}'.format(str(r6.text)))
            assert r6.status_code == 200, "http 状态码不对，目前状态码是{}".format(r6.status_code)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r6.status_code)))
            logger.info('返回值是{}'.format(str(r6.text)))
        with allure.step("校验返回值"):
            assert r6.json() != {}, '创建数字货币购买交易-payment with card，接口返回值为{}'.format(r6.json())
            logger.info('transaction id是{}'.format(str(r6.json()['txn_id'])))
        with allure.step("返回的redirect需要报存在html文件里打开操作一下,需要5分钟之内拿到payme给我们返回信息,不需要了暂时先不删"):
            with open('checkout.html', 'w') as file:
                file.write(r6.json()['redirect']['url'])
        with allure.step("打开3ds"):
            webbrowser.open(r6.json()['redirect']['url'])
            sleep(20)
        with allure.step("查询删除卡重新完成buy交易(勾选绑卡)的状态"):
            params = {
                'binding': 'false'
            }
            r3 = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
            for i in r3.json()['cards']:
                if i['id'] == token_id:
                    assert i['is_deleted'] is False, '删除绑定的卡，预期参数错误，接口返回{}'.format(i['is_deleted'])

    @allure.title('test_check_out_019')
    @allure.description('查询用户使用过的所有卡')
    def test_check_out_019(self):
        with allure.step("查询用户使用过的所有卡"):
            params = {
                'binding': 'false'
            }
            r = session.request('GET', url='{}/acquiring/cards'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_check_out_020')
    @allure.description('删除用户是用过的卡')
    def test_check_out_020(self):
        with allure.step("删除用户是用过的卡"):
            params = {
                'token_id': 'false'
            }
            r = session.request('DELETE', url='{}/acquiring/cards/{}'.format(env_url, params['token_id']),
                                headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_check_out_021')
    @allure.description('单B EE用户')
    def test_check_out_021(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='yanting.huang+16@cabital.com')
        with allure.step("币种兑选择"):
            pairs = ApiFunction.get_buy_crypto_currency(partner='woo', type='all')
        for z in pairs:
            for x in get_json()['checkOutAreaList2']:
                with allure.step("创建数字货币购买交易信息，ccy 是buy"):
                    while 1 < 2:
                        with allure.step("get token"):
                            data = {
                                "type": "card",
                                "number": "4242424242424242",
                                "expiry_month": 6,
                                "expiry_year": 2025,
                                "name": "Bruce Wayne",
                                "cvv": "100",
                                "billing_address": {
                                    "address_line1": "Checkout.com",
                                    "address_line2": "90 Tottenham Court Road",
                                    "city": "London",
                                    "state": "London",
                                    "zip": "W1T 4TJ",
                                    "country": x
                                }
                            }
                            headers2 = {
                                "Authorization": "Bearer pk_sbox_cqecp4mj36curomekpmzd42cjeg",
                                "Content-Type": "application/json"
                            }
                            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens',
                                                data=json.dumps(data), headers=headers2)
                            with allure.step("校验状态码"):
                                assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                    r.status_code)
                                token = r.json()['token']
                                dic = json.loads(r.text)
                                if "issuer" in dic.keys():
                                    issuer = dic["issuer"]
                                else:
                                    issuer = ''
                        crypto_list = ApiFunction.get_buy_crypto_list(150, pairs=z, ccy='buy', country=x)
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
                                "type": 1,
                                "token": token,
                                "expiry_month": '6',
                                "expiry_year": str(r.json()['expiry_year']),
                                "scheme": str(r.json()['scheme']),
                                "last": str(r.json()['last4']),
                                "bin": str(r.json()['bin']),
                                "card_type": str(r.json()['card_type']),
                                "issuer": issuer,
                                "issuer_country": x
                            },
                            "bind_card": True,
                            "card_holder_name": "Ting DP319",
                            "billing_address": {
                                "country_code": "CN",
                                "state": "",
                                "city": "shanghai",
                                "post_code": "210000",
                                "street_line_1": "Shanghai",
                                "street_line_2": "Shab"
                            },
                            "nonce": generate_string(30),
                            "check_amount": True
                        }
                        logger.info('checkout传入参数是{}'.format(data))
                        r = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data),
                                            headers=headers)
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                        if 'Invalid Quote' not in r.text:
                            break
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, "币种兑{},地区{},ccy是buy,checkout支付错误，当前返回值是{}".format(z, x, r.text)
                with allure.step("创建数字货币购买交易信息，ccy 是spend"):
                    with allure.step("解决最大/最小值"):
                        if 'CLF' in z:
                            amount = 100
                        elif 'CLP' in z:
                            amount = 1900
                        elif 'COP' in z:
                            amount = 4900
                        elif 'LKR' in z:
                            amount = 400
                        elif 'KRW' in z:
                            amount = 1500
                        elif 'VND' in z:
                            amount = 31500
                        elif 'IDR' in z:
                            amount = 300000
                        else:
                            amount = 150
                    while 1 < 2:
                        with allure.step("get token"):
                            data = {
                                "type": "card",
                                "number": "4242424242424242",
                                "expiry_month": 6,
                                "expiry_year": 2025,
                                "name": "Bruce Wayne",
                                "cvv": "100",
                                "billing_address": {
                                    "address_line1": "Checkout.com",
                                    "address_line2": "90 Tottenham Court Road",
                                    "city": "London",
                                    "state": "London",
                                    "zip": "W1T 4TJ",
                                    "country": x
                                }
                            }
                            headers2 = {
                                "Authorization": "Bearer pk_sbox_cqecp4mj36curomekpmzd42cjeg",
                                "Content-Type": "application/json"
                            }
                            r = session.request('POST', url='https://api.sandbox.checkout.com/tokens',
                                                data=json.dumps(data),
                                                headers=headers2)
                            with allure.step("校验状态码"):
                                assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                    r.status_code)
                                token = r.json()['token']
                        crypto_list = ApiFunction.get_buy_crypto_list(amount, pairs=z, ccy='spend', country=x)
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
                                "type": 1,
                                "token": token,
                                "expiry_month": '6',
                                "expiry_year": str(r.json()['expiry_year']),
                                "scheme": str(r.json()['scheme']),
                                "last": str(r.json()['last4']),
                                "bin": str(r.json()['bin']),
                                "card_type": str(r.json()['card_type']),
                                "issuer": issuer,
                                "issuer_country": x
                            },
                            "bind_card": True,
                            "card_holder_name": "Ting DP319",
                            "billing_address": {
                                "country_code": "CN",
                                "state": "",
                                "city": "shanghai",
                                "post_code": "210000",
                                "street_line_1": "Shanghai",
                                "street_line_2": "Shab"
                            },
                            "nonce": generate_string(30),
                            "check_amount": True
                        }
                        logger.info('checkout传入参数是{}'.format(data))
                        r = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data),
                                            headers=headers)
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                        if 'Invalid Quote' not in r.text:
                            break
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, "币种兑{},地区{},ccy是spend,checkout支付错误，当前返回值是{}".format(z, x, r.text)


