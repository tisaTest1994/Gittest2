from Function.api_function import *
from Function.operate_sql import *


@allure.feature("Payin cpf 相关 testcases")
class TestPayinCpfApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_payin_cpf_001')
    @allure.description('cpf注册状态检查')
    def test_payin_cpf_001(self):
        cpf_info = [('yanting.huang+192@cabital.com', 0),
                    ('yanting.huang+159@cabital.com', 1),
                    ('yanting.huang+162@cabital.com', 2),
                    ('yanting.huang+175@cabital.com', 3),
                    ('yanting.huang+161@cabital.com', 5)]
        for i in cpf_info:
            cpf_account = i[0]
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=cpf_account)
            with allure.step("BRL法币充值账户信息"):
                r = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'BRL', 'PIX'),
                                    headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['bank_accounts'][0][
                               'account_name'] == '3RZ SERVICOS DIGITAIS LTDA', "BRL法币充值账户信息错误，返回值是{}".format(r.text)
                with allure.step("校验cpf注册状态"):
                    assert r.json()['bank_accounts'][0]['register_status'] == i[1], '返回cpf状态错误，当前账号cpf状态应为{},实际接口返回状态为{}'.format(i[1], r.json()['bank_accounts'][0]['register_status'])

    @allure.title('test_payin_cpf_002')
    @allure.description('webhook模拟brl充值（cpf status=5）')
    @pytest.mark.skip(reason='transaction id必须唯一，不唯一就会报错')
    def test_payin_cpf_002(self):
        cpf_info = [('yanting.huang+161@cabital.com', 5)]
        for i in cpf_info:
            cpf_account = i[0]
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=cpf_account)
            with allure.step("请求数据"):
                data = {
                    "accountId": "47b5cd55-aa17-4d2c-8b1c-40d637fd100b",
                    "amount": {
                        "amount": 2000,
                        "currency": "BRL"
                    },
                    "amountNet": {
                        "amount": 1151,
                        "currency": "BRL"
                    },
                    "transactionDescription": {
                        "description": "test by yanting",
                        "name": "Yan Ting161",
                        "taxId": "123.322.238-98",
                        "taxIdCountry": 76
                    },
                    "date": "2022-06-04",
                    "dateDetailed": "0001-01-01T00:00:00+00:00",
                    "type": "Credit",
                    "transactionId": "c21cf84a-0ff5-4973-a010-00c6ee07004",
                    "counterpart": {
                        "name": "Yan Ting161",
                        "taxId": "123.322.238-98",
                        "bankAccount": "2342-4",
                        "bankBranch": "2342",
                        "taxIdCountry": 76
                    },
                    "blockchain": "None"
                }
            r = session.request('POST', url='https://webhook.latibac.com/mh/transfero/credit_transaction_status_changed',
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_payin_cpf_003')
    @allure.description('webhook模拟brl充值（cpf status=3），充值成功后状态变为5')
    @pytest.mark.skip(reason='cpf状态从3变为5只能测试一次')
    # 每次执行修改email，account id，和transaction id即可
    def test_payin_cpf_003(self):
        cpf_info = [('yanting.huang+188@cabital.com', 3)]
        for i in cpf_info:
            cpf_account = i[0]
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=cpf_account)
            with allure.step("请求数据"):
                data = {
                    "accountId": "761d5269-ec25-45c0-ba38-1e0ae8ce808d",
                    "amount": {
                        "amount": 2000,
                        "currency": "BRL"
                    },
                    "amountNet": {
                        "amount": 1188,
                        "currency": "BRL"
                    },
                    "transactionDescription": {
                        "description": "test by yanting",
                        "name": "Ting DP188",
                        "taxId": "322.081.156-60",
                        "taxIdCountry": 76
                    },
                    "date": "2022-06-04",
                    "dateDetailed": "0001-01-01T00:00:00+00:00",
                    "type": "Credit",
                    "transactionId": "c35cf87a-0fd7-4983-a331-02c6ee88004",
                    "counterpart": {
                        "name": "Ting DP188",
                        "taxId": "322.081.156-60",
                        "bankAccount": "2342-4",
                        "bankBranch": "2342",
                        "taxIdCountry": 76
                    },
                    "blockchain": "None"
                }
            r = session.request('POST', url='https://webhook.latibac.com/mh/transfero/credit_transaction_status_changed',
                                data=json.dumps(data),
                                headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("检查cpf状态是否从3变为5"):
                sleep(10)
                r2 = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'BRL', 'PIX'),headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验cpf注册状态"):
                    assert r2.json()['bank_accounts'][0]['register_status'] == 5, '状态错误，完成充值后状态未从3变成5'

    @allure.title('test_payin_cpf_004')
    @allure.description('获取用户cpf信息')
    def test_payin_cpf_004(self):
        cpf_info = [('yanting.huang+192@cabital.com', 0),
                    ('yanting.huang+159@cabital.com', 1),
                    ('yanting.huang+162@cabital.com', 2),
                    ('yanting.huang+175@cabital.com', 3),
                    ('yanting.huang+161@cabital.com', 5)]
        for i in cpf_info:
            cpf_account = i[0]
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=cpf_account)
            with allure.step("获取用户补充信息"):
                r = session.request('GET', url='{}/kyc/user/info/additional'.format(env_url), headers=headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                logger.info(r.json())
            with allure.step("检查cpf状态"):
                sleep(1)
                r2 = session.request('GET', url='{}/pay/deposit/fiat/{}/{}'.format(env_url, 'BRL', 'PIX'), headers=headers)
                with allure.step("校验状态码"):
                    assert r2.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验cpf注册状态"):
                    logger.info(r2.json()['bank_accounts'][0]['register_status'])
