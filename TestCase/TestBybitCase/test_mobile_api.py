from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api connect 相关 testcases")
class TestConnectApi:
    url = get_json()['connect'][get_json()['env']]['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_connect_001 transfer 交易')
    @allure.description('transfer 交易')
    def test_connect_001(self):
        with allure.step("划转"):
            for i in get_json()['crypto_list']:
                with allure.step("获得transfer前金额"):
                    wallet_balance_old = ApiFunction.get_crypto_number(type=i)
                if i == 'USDT':
                    amount = '50'
                else:
                    amount = '0.01'
                data = {
                    "amount": amount,
                    "code": i,
                    "direction": "DEBIT",
                    "account_vid": get_json()['email']['accountId'],
                    "user_ext_ref": get_json()['email']['user_ext_ref']
                }
                with allure.step("获取2fa code"):
                    mfaVerificationCode = get_mfa_code(get_json()['email']['secretKey_richard'])
                    headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                with allure.step("transfer 交易"):
                    r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json()['connect'][get_json()['env']]['bybit']['Headers']['ACCESS-KEY']), data=json.dumps(data), headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json()['txn_id'] is not None, "transfer 交易错误，返回值是{}".format(r.text)
                    assert r.json()['status'] == 1, "transfer 交易错误，返回值是{}".format(r.text)
                transfer_id = r.json()['txn_id']
                sleep(10)
                with allure.step("获得transfer后金额"):
                    wallet_balance_latest = ApiFunction.get_crypto_number(type=i)
                assert Decimal(wallet_balance_old) - Decimal(data['amount']) == Decimal(wallet_balance_latest), 'transfer币种是{},transfer前金额是{},transfer金额是{}，transfer后金额是{}'.format(i, wallet_balance_old, data['amount'], wallet_balance_latest)
                with allure.step("确认划转"):
                    if r.json()['status'] == 1:
                        external_id = generate_string(25)
                        data = {
                            "status": "SUCCESS",
                            "code": "good",
                            "message": "ok",
                            "handle_time": int(time.time()),
                            "external_id": external_id
                        }
                        with allure.step("验签"):
                            unix_time = int(time.time())
                            nonce = generate_string(30)
                            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT',
                                                                url='/api/v1/accounts/{}/transfers/{}'.format(
                                                                    get_json()['email']['accountId'],
                                                                    transfer_id), nonce=nonce, body=json.dumps(data))
                            connect_header['ACCESS-SIGN'] = sign
                            connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
                            connect_header['ACCESS-NONCE'] = nonce
                        r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(self.url, get_json()['email']['accountId'], transfer_id), data=json.dumps(data), headers=connect_header)
                        with allure.step("校验状态码"):
                            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)

    # @allure.title('test_connect_002 transfer 交易')
    # @allure.description('transfer 交易')
    # def test_connect_002(self):
    #     with allure.step("确认划转"):
    #         account_id = 'cd7e353b-6f4c-45db-bdd5-78bdc13a53c7'
    #         external_id = generate_string(25)
    #         transfer_id = '5e2c1c61-2b57-4732-9aed-f41fffc185be'
    #         data = {
    #             "status": "FAILED",
    #             "code": "bad",
    #             "message": "fail error",
    #             "handle_time": int(time.time()),
    #             "external_id": external_id
    #         }
    #         with allure.step("验签"):
    #             unix_time = int(time.time())
    #             nonce = generate_string(30)
    #             sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT',
    #                                                 url='/api/v1/accounts/{}/transfers/{}'.format(
    #                                                     account_id,
    #                                                     transfer_id), nonce=nonce, body=json.dumps(data))
    #             connect_header['ACCESS-SIGN'] = sign
    #             connect_header['ACCESS-TIMESTAMP'] = str(unix_time)
    #             connect_header['ACCESS-NONCE'] = nonce
    #         r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id), data=json.dumps(data), headers=connect_header)
    #         with allure.step("校验状态码"):
    #             assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
    #         with allure.step("校验返回值"):
    #             assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)


