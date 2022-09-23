from Function.api_function import *
from Function.operate_sql import *


# Convert相关cases
class TestWidgetApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_widget_001')
    @allure.description('不传入partner_id, 取得全部conversion limit')
    def test_widget_001(self):
        with allure.step("不传入partner_id, 取得全部conversion limit"):
            params = {
                'partner_id': ''
            }
            r = session.request('GET', url='{}/connect/conversion/limits'.format(env_url), params=params,
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            assert r.json() == {"limits": {"BRL": {"min": "50", "max": "1000000"}, "BTC": {"min": "0.0002", "max": "5"},
                                           "CHF": {"min": "10", "max": "200000"}, "ETH": {"min": "0.002", "max": "100"},
                                           "EUR": {"min": "10", "max": "200000"}, "GBP": {"min": "10", "max": "200000"},
                                           "USDT": {"min": "10", "max": "200000"},
                                           "VND": {"min": "250000", "max": "5000000000"}}}, '不传入partner_id, 取得全部conversion limit错误，返回值是{}'.format(r.text)

    @allure.title('test_widget_002')
    @allure.description('传入partner_id, 取得全部conversion limit')
    def test_widget_002(self, partner):
        with allure.step("传入partner_id, 取得全部conversion limit"):
            params = {
                'partner_id': get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
            }
            r = session.request('GET', url='{}/connect/conversion/limits'.format(env_url), params=params,
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("验证数据是否和config一致"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                for y in r.json()['limits']:
                    if i['symbol'] == y:
                        config_conversion = i['config']['conversion']
                        del config_conversion['allow']
                        assert r.json()['limits'][y] == config_conversion, '传入partner_id, 取得全部conversion limit错误，币种是{}, config 配置内的值是{}, 接口返回值是{}'.format(y, config_conversion, r.json()['limits'][y])

    @allure.title('test_widget_003')
    @allure.description('transfer debit 交易')
    def test_widget_003(self, partner):
        with allure.step("划转"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                'account_vid']
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['transfer_debit']['allow'] is True:
                    with allure.step("获得transfer前金额"):
                        wallet_balance_old = ApiFunction.get_crypto_number(type=i['symbol'])
                    data = {
                        "amount": giveAmount(i['symbol']),
                        "code": i['symbol'],
                        "direction": "DEBIT",
                        "account_vid": get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid'],
                        "user_ext_ref": get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['user_ref_id']
                    }
                    with allure.step("获取2fa code"):
                        mfaVerificationCode = get_mfa_code('richard')
                        headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                    with allure.step("transfer 交易"):
                        r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']), data=json.dumps(data), headers=headers)
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
                        wallet_balance_latest = ApiFunction.get_crypto_number(type=i['symbol'])
                    assert Decimal(wallet_balance_old) - Decimal(data['amount']) == Decimal(
                        wallet_balance_latest), 'transfer币种是{},transfer前金额是{},transfer金额是{}，transfer后金额是{}'.format(i['symbol'],
                                                                                                                   wallet_balance_old,
                                                                                                                   data[
                                                                                                                       'amount'],
                                                                                                                   wallet_balance_latest)
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
                                sign = ApiFunction.make_signature(unix_time=str(unix_time), method='PUT', url='/api/v1/accounts/{}/transfers/{}'.format(account_vid, transfer_id), connect_type=partner, nonce=nonce, body=json.dumps(data))
                                connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            r = session.request('PUT', url='{}/accounts/{}/transfers/{}'.format(connect_url, account_vid, transfer_id), data=json.dumps(data), headers=connect_headers)
                            with allure.step("校验状态码"):
                                assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                            with allure.step("校验返回值"):
                                assert r.json() == {}, "确认划转交易错误，返回值是{}".format(r.text)

    @allure.title('test_widget_004')
    @allure.description('link onboarding')
    def test_widget_004(self, partner):
        with allure.step("获得用户信息"):
            params = {
                'partner_key': get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID'],
                'user_ext_ref': get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['user_ref_id'],
                'email': get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['email'],
                'redirect_url': 'https://www.baidu.com',
                'feature': 'onboarding'
            }
            r1 = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("验签"):
                sign = ApiFunction.get_link_sign(url=r1.url, partner=partner)
                connect_headers['ACCESS-SECRET'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Secret_Key']
                params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验url返回值"):
                print(r.text)
                #assert expect_url in r.url, "获取跳转地址,期望url是{}，返回值是{}".format(expect_url, r.url)