from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api bind bank card相关 testcases")
class TestBindBankCardApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_bind_bank_card_001')
    @allure.description('USD绑定银行卡-us bank account')
    @pytest.mark.skip(reason='手动操作')
    def test_bind_bank_card_001(self):
        # with allure.step("切换账号"):
        #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        with allure.step("us bank account"):
            data = {
                "code": "USD",
                "money_house_id": "MoneyHouseTypeCircleDGTLT",
                "account_name": "Wan yilei",
                "account_number": "1234223432344236",
                "aba_routing_number": "121000248",
                "bank_address": {
                    "country_code": "US"
                },
                "billing_address": {
                    "country_code": "US",
                    "state": "MA",
                    "city": "Boston",
                    "post_code": "01234",
                    "street_line_1": "100 Money Street"
                }
            }
        with allure.step("USD绑定银行卡"):
            r = session.request('POST', url='{}/pay/bank-account'.format(env_url), headers=headers,
                                data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_bind_bank_card_002')
    @allure.description('USD绑定银行卡-not us bank account iban supported')
    @pytest.mark.skip(reason='手动操作')
    def test_bind_bank_card_002(self):
        # with allure.step("切换账号"):
        #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        with allure.step("not us bank account iban supported"):
            data = {
                "code": "USD",
                "money_house_id": "MoneyHouseTypeCircleDGTLT",
                "account_name": "Wan yilei",
                "iban": "DE31100400480532013000",
                "bank_address": {
                    "city": "Berlin",
                    "country_code": "de"
                },
                "billing_address": {
                    "country_code": "de",
                    "city": "Berlin",
                    "post_code": "01234",
                    "street_line_1": "100 Money Street"
                }
            }
        with allure.step("USD绑定银行卡"):
            r = session.request('POST', url='{}/pay/bank-account'.format(env_url), headers=headers,
                                data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_bind_bank_card_003')
    @allure.description('USD绑定银行卡-not us bank account iban not supported')
    @pytest.mark.skip(reason='手动操作')
    def test_bind_bank_card_003(self):
        # with allure.step("切换账号"):
        #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        with allure.step("not us bank account iban supported"):
            data = {
                "code": "USD",
                "money_house_id": "MoneyHouseTypeCircleDGTLT",
                "account_name": "Wan yilei",
                "account_number": "621485001021478",
                "swift_code": "CMBCHKHH",
                "bank_name": "CHINA MERCHANTS BANK",
                "bank_address": {
                    "country_code": "HK",
                    "city": "Hongkong"
                },
                "billing_address": {
                    "country_code": "HK",
                    "city": "Hongkong",
                    "post_code": "01234",
                    "street_line_1": "100 Money Street"
                }
            }
        with allure.step("USD绑定银行卡"):
            r = session.request('POST', url='{}/pay/bank-account'.format(env_url), headers=headers,
                                data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_bind_bank_card_004')
    @allure.description('获取USD已经绑定银行卡列表')
    def test_bind_bank_card_004(self):
        # with allure.step("切换账号"):
        #     headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        params = {
            'payment_method': 'SWIFT',
            'money_house_id': 'MoneyHouseTypeCircleDGTLT',
            'code': 'USD'
        }
        with allure.step("获取已经绑定银行卡列表"):
            r = session.request('GET', url='{}/pay/bank-accounts'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['bound_bank_account_max_cnt'] == 3, "获取已经绑定银行卡列表失败，返回值是{}".format(r.text)

    @allure.title('test_bind_bank_card_005')
    @allure.description('获取USD某个银行卡具体信息')
    def test_bind_bank_card_005(self):
        bank_id = 'b949a136-d8ae-4f44-8acd-9e989eca2bd0'
        with allure.step("获取某个银行卡具体信息"):
            r = session.request('GET', url='{}/pay/bank-account/{}'.format(env_url, bank_id), headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['bound_bank_account']['id'] == bank_id, "获取某个银行卡具体信息失败，返回值是{}".format(r.text)

    @allure.title('test_bind_bank_card_006')
    @allure.description('获取USD某个银行国家列表')
    def test_bind_bank_card_006(self):
        params = {
            'payment_method': 'SWIFT',
            'money_house_id': 'MoneyHouseTypeCircleDGTLT',
            'code': 'USD'
        }
        with allure.step("获取某个银行国家列表"):
            r = session.request('GET', url='{}/pay/bank-account'.format(env_url), headers=headers, params=params)
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json()['countries'] is not None, "获取某个银行国家列表失败，返回值是{}".format(r.text)

    @allure.title('test_bind_bank_card_007')
    @allure.description('解绑USD银行卡')
    #@pytest.mark.skip(reason='手动操作')
    def test_bind_bank_card_007(self):
        bank_id = '5a54dccb-683b-4046-b245-46b240e9e28b'
        data = {
            'id': 'bank_id'
        }
        with allure.step("获取某个银行国家列表"):
            r = session.request('DELETE', url='{}/pay/bank-account/{}'.format(env_url, bank_id), headers=headers, data=json.dumps(data))
        with allure.step("状态码和返回值"):
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)

