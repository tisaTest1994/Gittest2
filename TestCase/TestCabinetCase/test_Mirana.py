from Function.api_function import *
from Function.operate_sql import *


# operate相关cases
class TestOperateApi:

    # 初始化class
    def setup_method(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')

    @allure.title('test_2B_001')
    @allure.description('提现USDC成功')
    def test_2B_001(self):
        with allure.step("提现USDC成功"):
            data = {
                "currency": "USDC",
                "amount": "13.141592",
                "destination": "0xF9C184974f2eAfE6d43A8A5f1c2799ee7517D5C5"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/withdraw'.format(operateUrl,
                                                                                        get_json()['2B'][
                                                                                            'mirana_account']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)

    @allure.title('test_2B_002')
    @allure.description('申购活期产品成功')
    def test_2B_002(self):
        with allure.step("申购活期产品成功"):
            data = {
                "amount": "10"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/subscribe/{}'.format(operateUrl,
                                                                                            get_json()['2B'][
                                                                                                'mirana_account'],
                                                                                            get_json()['2B'][
                                                                                                'flexible_product']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)

    @allure.title('test_2B_003')
    @allure.description('申购定期产品成功')
    def test_2B_003(self):
        with allure.step("申购定期产品成功"):
            data = {
                "amount": "10"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/subscribe/{}'.format(operateUrl,
                                                                                            get_json()['2B'][
                                                                                                'mirana_account'],
                                                                                            get_json()['2B'][
                                                                                                'fixed_product']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)

    @allure.title('test_2B_004')
    @allure.description('赎回活期产品成功')
    def test_2B_004(self):
        with allure.step("赎回活期产品成功"):
            data = {
                "amount": "10"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/reedem/{}'.format(operateUrl,
                                                                                         get_json()['2B'][
                                                                                             'mirana_account'],
                                                                                         get_json()['2B'][
                                                                                             'flexible_product']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)

    @allure.title('test_2B_005')
    @allure.description('申购定期产品后打开auto renew')
    def test_2B_005(self):
        with allure.step("申购定期产品成功"):
            data = {
                "amount": "1"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/subscribe/{}'.format(operateUrl,
                                                                                            get_json()['2B'][
                                                                                                'mirana_account'],
                                                                                            get_json()['2B'][
                                                                                                'fixed_product']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)
        with allure.step("定期产品打开auto renew"):
            transaction_id = r.json()['transaction_id']
            data = {
                "auto_renew": True
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/renew/{}'.format(operateUrl,
                                                                                        get_json()['2B'][
                                                                                            'mirana_account'],
                                                                                        transaction_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['update_result'] == True, "查询update_result错误，返回值是{}".format(r.text)

    @allure.title('test_2B_006')
    @allure.description('申购定期后产品关闭auto renew')
    def test_2B_006(self):
        with allure.step("申购定期产品成功"):
            data = {
                "amount": "1.12"
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/subscribe/{}'.format(operateUrl,
                                                                                            get_json()['2B'][
                                                                                                'mirana_account'],
                                                                                            get_json()['2B'][
                                                                                                'fixed_product']),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert 'transaction_id' in r.text, "查询transaction_id错误，返回值是{}".format(r.text)
        with allure.step("定期产品打开auto renew"):
            transaction_id = r.json()['transaction_id']
            data = {
                "auto_renew": False
            }
            r = session.request('POST', url='{}/operatorapi/account/{}/renew/{}'.format(operateUrl,
                                                                                        get_json()['2B'][
                                                                                            'mirana_account'],
                                                                                        transaction_id),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['update_result'] == True, "查询update_result错误，返回值是{}".format(r.text)
