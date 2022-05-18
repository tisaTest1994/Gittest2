from Function.api_function import *
from Function.operate_sql import *


@allure.feature("VND Acquiring相关的api")
class TestAcquiringApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_acquiring_001')
    @allure.description('打开收单画面接口')
    def test_acquiring_001(self):
        with allure.step("VND打开收单画面接口"):
            r = session.request('GET', url='{}/acquiring/prepare/{}'.format(env_url, 'VND'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['payment_controls'][0]['payment_method'] == {'type': 1, 'sub_type': 1},\
                    'vnd收单画面支付方式错误，接口返回值是{}'.format(r.json())
                assert r.json()['payment_controls'][0]['constraint'] == {'min': '20000', 'max': '1000000000'},\
                    'vnd收单画面限额错误,接口返回值是{}'.format(r.json())
                assert r.json()['payment_controls'][0]['fee_rule']['percentage_charge_rule']['percentage'] == '2',\
                    'VND acquiring 费率错误,接口返回值是{}'.format(r.json())

    @allure.title('test_acquiring_002')
    @allure.description('VND建收单交易')
    def test_acquiring_002(self):
        with allure.step("VND创建收单交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            with allure.step("VND法币acquiring信息"):
                data = {
                    "amount": "30000",
                    "payment_method": {
                        "type": 1,
                        "sub_type": 1
                    },
                    "txn_type": 1,
                    "card": {
                        "card_no": "9704001933454934",
                        "issue_date": "03/07",
                        "holder_name": "NGUYEN VAN A"
                    },
                    "Nonce": "JamesTest"
                }
            r = session.request('POST', url='{}/acquiring/{}'.format(env_url, 'VND'), data=json.dumps(data), headers=headers)
            r2 = session.request('GET', url='{}/acquiring/prepare/{}'.format(env_url, 'VND'), headers=headers)
            fee = float(r2.json()['payment_controls'][0]['fee_rule']['percentage_charge_rule']['percentage'])*0.01*(float(data['amount']))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info('txn_id:{}'.format(r.json()['txn_id']))
                assert r.json()['instructed_amount'] == data['amount'], 'acquiring扣除fee前的金额错误，接口返回值{}'.format(r.json['instructed_amount'])
                assert float(r.json()['actual_amount']) == float(data['amount']) - fee, 'acquiring实际金额错误，接口返回值{}'.format(r.json['actual_amount'])
                assert r.json()['fee']['amount'] == '600', 'fee错误，接口返回值{}'.format(r.json()['fee'])
                sleep(6)
            with allure.step("刷新获取收单交易"):
                r3 = session.request('GET', url='{}/acquiring/{}'.format(env_url, r.json()['txn_id']), headers=headers)
                print(r3.url)
            with allure.step("校验返回值"):
                assert r3.status_code == 200, "http 状态码不对，目前状`态码是{}".format(r.status_code)

    @allure.title('test_acquiring_003')
    @allure.description('计算收单费用-VND')
    def test_acquiring_003(self):
        with allure.step("计算收单费用-VND"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
            with allure.step("VND法币acquiring信息"):
                data = {
                    "code": "VND",
                    "amount": "20000",
                    "payment_method": {
                        "type": 1,
                        "sub_type": 1
                    }
                }
            r = session.request('POST', url='{}/acquiring/fee'.format(env_url), data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['fee'] == {'code': 'VND', 'amount': '400'}, '收单费用计算错误，接口返回值是{}'.format(r.json()['fee'])


    @allure.title('test_convert_007')
    @allure.description('使用错误金额换汇交易')
    def test_convert_007(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['email']['payout_email'])
        quote = ApiFunction.get_quote('USDT-VND')
        print(quote)
        # data = {
        #     "quote_id": quote['quote_id'],
        #     "quote": quote['quote'],
        #     "pair": 'USDT-VND',
        #     "buy_amount": str(float(quote['quote'])*10),
        #     "sell_amount": 10,
        #     "major_ccy": 'USDT'
        # }
        data = {
            "quote_id": "20210416225049:BTC-USDT:Customer",
            "quote": "61426.365",
            "pair": "BTC-USDT",
            "buy_amount": "0.001",
            "sell_amount": "61.426365",
            "major_ccy": "BTC"
        }
        r = session.request('POST', url='{}/txn/cfx'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('申请换汇参数{}'.format(data))
        assert 'amount calculation error' in r.text, '使用错误金额换汇交易错误,返回值是{}'.format(r.text)