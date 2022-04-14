from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api payout cash 相关 testcases")
class TestPayoutCashApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payout_cash_001')
    @allure.description('法币获取提现费率和提现限制')
    def test_payout_cash_001(self):
        with allure.step("获取法币列表"):
            for i in get_json()['cash_list']:
                with allure.step("获取提现费率和提现限制"):
                    data = {
                        "code": i,
                        "amount": "100"
                    }
                    r = session.request('POST', url='{}/pay/withdraw/fiat/verification'.format(env_url),
                                        data=json.dumps(data), headers=headers)
                    if i == 'GBP':
                        assert r.json()['fee']['amount'] == '2.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'EUR':
                        assert r.json()['fee']['amount'] == '2.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'BRL':
                        assert r.json()['fee']['amount'] == '3.6', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)
                    elif i == 'CHF':
                        assert r.json()['fee']['amount'] == '4.5', '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert r.json()['fee']['code'] == i, '获取提现费率和提现限制错误, 币种是{}'.format(i)
                        assert float(r.json()['receivable_amount']) == float(data['amount']) - float(
                            r.json()['fee']['amount']), '获取提现费率和提现限制错误, 币种是{}'.format(i)

    @allure.title('test_payout_cash_002')
    @allure.description('获得法币提现币种')
    def test_payout_cash_002(self):
        with allure.step("提现币种"):
            r = session.request('GET', url='{}/pay/withdraw/ccy/{}'.format(env_url, 'fiat'), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                cash_list = []
                for y in r.json()['fiat']:
                    if y['status'] == 1:
                        cash_list.append(y['name'])
                assert (set(cash_list) == set(get_json()['cash_list'])), '获得法币提现币种错误，接口返回币种是{}'.format(cash_list)

    @allure.title('test_payout_cash_003')
    @allure.description('开启法币提现画面')
    def test_payout_cash_003(self):
        with allure.step("获取法币列表"):
            for i in get_json()['cash_list']:
                with allure.step("开启法币提现画面"):
                    params = {
                        'code': i
                    }
                    r = session.request('GET', url='{}/pay/withdraw/fiat'.format(env_url), params=params,
                                        headers=headers)
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        if i == 'GBP':
                            assert r.json()['supported_payment_methods'] == 'Faster Payments', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {'min': '20', 'max': '40000', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'EUR':
                            assert r.json()['supported_payment_methods'] == 'SEPA', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods'][r.json()['supported_payment_methods']] == {'max': '50000', 'min': '25', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'CHF':
                            assert r.json()['supported_payment_methods'] == 'SIC or SWIFT', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods']['SIC'] == {'max': '50000', 'min': '25', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                        elif i == 'BRL':
                            assert r.json()['supported_payment_methods'] == 'PIX or Bank Transfer', '开启法币提现画面错误，币种是{},接口返回值是{}'.format(i, r.json())
                            assert r.json()['payment_methods']['Bank Transfer'] == {'min': '20', 'max': '300000', 'order': 1}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
                            assert r.json()['payment_methods']['PIX'] == {'min': '20', 'max': '300000', 'order': 0}, '开启法币提现画面错误，币种是{},接口返回值是{}'.format(
                                i, r.json())
