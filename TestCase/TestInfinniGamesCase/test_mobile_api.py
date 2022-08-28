import json

from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api connect 相关 testcases")
class TestMobileApi:
    url = get_json()['infinni_games']['url']

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()
            headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']

    @allure.title('test_mobile_001')
    @allure.description('获取合作方配置')
    def test_mobile_001(self):
        with allure.step("获取合作方配置"):
            partner_id = get_json()['infinni_games']['partner_id']
        with allure.step("获取data"):
            r = session.request('GET', url='{}/connect/{}/transfer/limit'.format(env_url, partner_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['configs'] is not None, "获取合作方配置错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_002')
    @allure.description('获取合作方划转交易配置- (传入部分参数)')
    def test_mobile_002(self):
        with allure.step("获取合作方配置"):
            partner_id = get_json()['infinni_games']['partner_id']
        with allure.step("获取data"):
            r = session.request('GET',
                                url='{}/connect/{}/transfer/limit?ccy_type=2&transfer_type=1&only_enabled_ccy=true'.format(
                                    env_url, partner_id), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['configs'] is not None, "获取合作方配置错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_003')
    @allure.description('合作方划转交易费用')
    def test_mobile_003(self):
        with allure.step("合作方划转交易费用"):
            data = {
                "amount": "50",
                "code": "USDT",
                "direction": "DEBIT"
            }
            r = session.request('POST', url='{}/connect/{}/transfer/fee'.format(env_url, get_json()['infinni_games'][
                'partner_id']), data=json.dumps(data), headers=headers)
            logger.info('r.json返回值是:{}'.format(r.json()))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                logger.info('返回值是{}'.format(str(r.text)))
                assert r.json()['fee']['amount'] == '0', "合作方划转交易费用错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_004')
    @allure.description('合作方划转交易预校验-(link关系存在)')
    def test_mobile_004(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account='external.qa@cabital.com', password='Zcdsw123')
        partner_id = get_json()['infinni_games']['partner_id']
        with allure.step("合作方划转交易 预校验"):
            data = {
                "amount": "50",
                "code": "USDT",
                "direction": "DEBIT",
                "account_vid": "125831ca-a068-46fe-b5a9-bfc610f915dc",
                "user_ext_ref": "988518746672869376"
            }
            r = session.request('POST', url='{}/connect/{}/transfer/confirm'.format(env_url, partner_id), data=json.dumps(data), headers=headers)
            logger.info('r.json返回值是：{}'.format(r.json()))
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "合作方划转交易 预校验错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_005')
    @allure.description('合作方划转交易预校验-(link关系不存在异常场景)')
    def test_mobile_005(self):
        with allure.step(" 没有link关系合作方划转交易 预校验"):
            data = {
                "amount": "50",
                "code": "USDT",
                "direction": "DEBIT",
                "account_vid": "d9f35f7c-ec94-425d-9f66-95585457bb7d",
                "user_ext_ref": "james.lee@cabital.com"
            }
            r = session.request('POST',
                                url='{}/connect/{}/transfer/confirm'.format(env_url, get_json()['infinni_games'][
                                    'partner_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == "PA013", "合作方划转交易 预校验错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_006')
    @allure.description('合作方划转交易-使用其他人绑定的account_idv')
    def test_mobile_006(self):
        with allure.step("合作方划转交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("法币提现"):
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        with allure.step("参数"):
            data = {
                "amount": "50",
                "code": "USDT",
                "direction": "DEBIT",
                "account_vid": "d9f35f7c-ec94-425d-9f66-95585457bb7d",
                "user_ext_ref": get_json()['infinni_games']['uid_B']
            }
            r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json()['infinni_games'][
                'partner_id']), data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA013', "合作方划转交易错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_007')
    @allure.description('合作方划转交易-cabital发起transfer debit交易成功，校验可用余额')
    def test_mobile_007(self):
        with allure.step("合作方划转交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        with allure.step("参数"):
            data = {
                "amount": "20",
                "code": "USDT",
                "direction": "DEBIT",
                "account_vid": get_json()['infinni_games']['account_vid_c'],
                "user_ext_ref": get_json()['infinni_games']['uid_C']
            }
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=data['code'])
            logger.info('transfer_amount_wallet_balance_old的值是{}'.format(transfer_amount_wallet_balance_old))
        r = session.request('POST',
                            url='{}/connect/{}/transfer'.format(env_url, get_json()['infinni_games']['partner_id']),
                            data=json.dumps(data), headers=headers)
        logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step('获得transfer后币种可用balance数量'):
            transfer_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=data['code'])
            logger.info('transfer_amount_wallet_balance_latest的值是{}'.format(transfer_amount_wallet_balance_latest))
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) - Decimal(data['amount']) == Decimal(
                transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)
        with allure.step("校验返回值"):
            assert r.json()['amount'] == data['amount'], "合作方划转交易错误，返回值是{}".format(r.text)
            transfer_id = r.json()['txn_id']
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
                                                            get_json()['infinni_games']['account_vid_c'], transfer_id),
                                                        key='infinni games', nonce=nonce, body=json.dumps(data))
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(self.url, get_json()['infinni_games']['account_vid_c'], transfer_id), data=json.dumps(data), headers=headers)
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)

    @allure.title('test_mobile_008')
    @allure.description('合作方划转交易-cabital发起transfer debit交易失败，校验用户账户可用资金解冻成功')
    def test_mobile_008(self):
        with allure.step("合作方划转交易"):
            headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
                account=get_json()['email']['payout_email'])
        with allure.step("获得otp"):
            mfaVerificationCode = get_mfa_code()
            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        with allure.step("参数"):
            data = {
                "amount": "20.01",
                "code": "USDT",
                "direction": "DEBIT",
                "account_vid": get_json()['infinni_games']['account_vid_c'],
                "user_ext_ref": get_json()['infinni_games']['uid_C']
            }
        with allure.step('获得transfer前币种可用balance数量'):
            transfer_amount_wallet_balance_old = ApiFunction.get_crypto_number(type=data['code'])
            logger.info('transfer_amount_wallet_balance_old的值是{}'.format(transfer_amount_wallet_balance_old))
        r = session.request('POST',
                            url='{}/connect/{}/transfer'.format(env_url, get_json()['infinni_games']['partner_id']),
                            data=json.dumps(data), headers=headers)
        logger.info('r.json()返回值是{}'.format(r.json()))
        with allure.step('获得transfer后币种可用balance数量'):
            transfer_amount_wallet_balance_latest = ApiFunction.get_crypto_number(type=data['code'])
            logger.info('transfer_amount_wallet_balance_latest的值是{}'.format(transfer_amount_wallet_balance_latest))
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验transfer前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) - Decimal(data['amount']) == Decimal(
                transfer_amount_wallet_balance_latest), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest)
        with allure.step("校验返回值"):
            assert r.json()['amount'] == data['amount'], "合作方划转交易错误，返回值是{}".format(r.text)
            transfer_id = r.json()['txn_id']
        with allure.step("确认划转"):
            if r.json()['status'] == 1:
                external_id = generate_string(25)
                data = {
                    "status": "FAILED",
                    "code": "bad",
                    "message": "fail error",
                    "handle_time": int(time.time()),
                    "external_id": external_id
                }
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT',
                                                url='/api/v1/accounts/{}/transfers/{}'.format(
                                                    get_json()['infinni_games']['account_vid_c'], transfer_id),
                                                key='infinni games', nonce=nonce, body=json.dumps(data))
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(self.url, get_json()['infinni_games'][
            'account_vid_c'], transfer_id), data=json.dumps(data), headers=headers)
        logger.info('webhook返回值是{}'.format(r.json()))
        sleep(3)
        with allure.step('获得webhook失败后币种可用balance数量'):
            transfer_amount_wallet_balance_latest2 = ApiFunction.get_crypto_number(type='USDT')
            logger.info('transfer_amount_wallet_balance_latest2的值是{}'.format(transfer_amount_wallet_balance_latest2))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)
        with allure.step("校验transfer失败前后的可用balance数量"):
            assert Decimal(transfer_amount_wallet_balance_old) == Decimal(
                transfer_amount_wallet_balance_latest2), "transfer前后可用balance数量不对，transfer前balance是{}，transfer后balance是{}".format(
                transfer_amount_wallet_balance_old, transfer_amount_wallet_balance_latest2)

    @allure.title('test_connect_001 transfer 交易')
    @allure.description('transfer 交易')
    def test_connect_002(self):
        with allure.step("确认划转"):
            account_id = '2f1f9c33-6e3a-40e0-b5e2-e38e2ebe4987'
            external_id = generate_string(25)
            transfer_id = '5304901b-9f4b-4536-91e0-ab3b345aa3bd'
            data = {
                "status": "FAILED",
                "code": "bad",
                "message": "fail error",
                "handle_time": int(time.time()),
                "external_id": external_id
            }
            with allure.step("验签"):
                unix_time = int(time.time())
                nonce = generate_string(30)
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='PUT',
                                                    url='/api/v1/accounts/{}/transfers/{}'.format(
                                                        account_id,
                                                        transfer_id), key='infinni games', nonce=nonce, body=json.dumps(data))
                connect_headers['ACCESS-SIGN'] = sign
                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                connect_headers['ACCESS-NONCE'] = nonce
            r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(self.url, account_id, transfer_id), data=json.dumps(data), headers=connect_headers)
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)

