from Function.api_function import *
from Function.operate_sql import *


# 账户划转相关cases
class TestTransferApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_transfer_001')
    @allure.description('partner发起请求，把资金从cabital转移到partner账户')
    def test_transfer_001(self, partner):
        with allure.step("获取用户的account_vid"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                'account_vid']
        with allure.step("获得不同币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['debit']['allow']:
                    with allure.step("未操作前的balance"):
                        old_balance = ApiFunction.connect_get_balance(partner, account_vid, i['symbol'])['balances']
                    with allure.step("获得data"):
                        with allure.step("获得otp"):
                            mfaVerificationCode = get_mfa_code('richard')
                        external_id = generate_string(25)
                        data = {
                            'amount': giveAmount(i['symbol']),
                            'symbol': i['symbol'],
                            'otp': str(mfaVerificationCode),
                            'direction': 'DEBIT',
                            'external_id': external_id
                        }
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='POST',
                                                          url='/api/v1/accounts/{}/transfers'.format(account_vid),
                                                          connect_type=partner, nonce=nonce, body=json.dumps(data))
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("把数字货币从cabital转移到bybit账户"):
                        r = session.request('POST', url='{}/accounts/{}/transfers'.format(connect_url, account_vid),
                                            data=json.dumps(data), headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        if "PA043" not in r.text:
                            with allure.step("校验返回值"):
                                assert r.json()[
                                           'status'] == 'SUCCESS', "partner发起请求，把资金从cabital转移到partner账户失败，返回值是{}".format(
                                    r.text)
                        else:
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                            logger.info('由于每日限额超额，该笔transfer交易不成功，message是{}'.format(r.json()['message']))
                    if r.status_code != 400:
                        with allure.step("查询交易数据"):
                            sleep(2)
                            with allure.step("验签"):
                                unix_time = int(time.time())
                                nonce = generate_string(20) + str(time.time()).split('.')[0]
                                sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                                  url='/api/v1/recon/transfers/{}'.format(external_id),
                                                                  connect_type=partner, nonce=nonce)
                                connect_headers['ACCESS-KEY'] = \
                                get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            with allure.step("查询转账记录"):
                                r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url, external_id),
                                                    headers=connect_headers)
                            with allure.step("状态码和返回值"):
                                logger.info('状态码是{}'.format(str(r.status_code)))
                                logger.info('返回值是{}'.format(str(r.text)))
                            with allure.step("校验状态码"):
                                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                            with allure.step("校验返回值"):
                                assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)
                    with allure.step("操作后的balance"):
                        new_balance = ApiFunction.connect_get_balance(partner, account_vid, i['symbol'])['balances']
                    with allure.step("计算用户balance变化"):
                        assert Decimal(old_balance) - Decimal(data['amount']) == Decimal(
                            new_balance), "用户balance变化错误，操作前的balance是{},操作金额是{},操作后的金额是{}".format(old_balance,
                                                                                                  str(giveAmount(
                                                                                                      i['symbol'])),
                                                                                                  new_balance)

    @allure.title('test_transfer_002')
    @allure.description('partner发起请求，把资金从cabital转移到partner账户并且关联C+T交易')
    def test_transfer_002(self, partner):
        with allure.step("获取用户的account_vid"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                'account_vid']
        with allure.step("获取换汇支持币种对"):
            cfx_list = []
            for z in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['pairs']:
                cfx_list.append(z['pair'])
        with allure.step("获得不同币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['debit']['allow']:
                    for y in cfx_list:
                        if i['symbol'] in y:
                            transaction = ApiFunction.cfx_random(y, y.split('-')[0], account_id=account_vid,
                                                                 headers=connect_header, url=connect_url,
                                                                 partner=partner)
                            cfx_transaction_id = transaction['returnJson']['transaction_id']
                            with allure.step("获得data"):
                                with allure.step("获得otp"):
                                    mfaVerificationCode = get_mfa_code('richard')
                                external_id = generate_string(25)
                                data = {
                                    'amount': transaction['data']['buy_amount'],
                                    'symbol': i['symbol'],
                                    'otp': str(mfaVerificationCode),
                                    'direction': 'DEBIT',
                                    'external_id': external_id,
                                    'conversion_id': cfx_transaction_id
                                }
                            with allure.step("验签"):
                                unix_time = int(time.time())
                                nonce = generate_string(20) + str(time.time()).split('.')[0]
                                sign = ApiFunction.make_signature(unix_time=str(unix_time), method='POST',
                                                                  url='/api/v1/accounts/{}/transfers'.format(
                                                                      account_vid),
                                                                  connect_type=partner, nonce=nonce,
                                                                  body=json.dumps(data))
                                connect_headers['ACCESS-KEY'] = \
                                get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            with allure.step("把数字货币从cabital转移到partner账户"):
                                r = session.request('POST',
                                                    url='{}/accounts/{}/transfers'.format(connect_url, account_vid),
                                                    data=json.dumps(data), headers=connect_headers)
                            with allure.step("状态码和返回值"):
                                logger.info('状态码是{}'.format(str(r.status_code)))
                                logger.info('返回值是{}'.format(str(r.text)))
                                if "PA043" not in r.text:
                                    with allure.step("校验返回值"):
                                        assert r.json()[
                                                   'status'] == 'SUCCESS', "partner发起请求，把资金从cabital转移到partner账户失败，返回值是{}".format(
                                            r.text)
                                else:
                                    assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                                    logger.info('由于每日限额超额，该笔transfer交易不成功，message是{}'.format(r.json()['message']))
                            if r.status_code != 400:
                                with allure.step("查询交易数据"):
                                    sleep(2)
                                    with allure.step("验签"):
                                        unix_time = int(time.time())
                                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                                          url='/api/v1/recon/transfers/{}'.format(
                                                                              external_id),
                                                                          connect_type=partner, nonce=nonce)
                                        connect_headers['ACCESS-KEY'] = \
                                            get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                        connect_headers['ACCESS-SIGN'] = sign
                                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                        connect_headers['ACCESS-NONCE'] = nonce
                                    with allure.step("查询转账记录"):
                                        r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url,
                                                                                                      external_id),
                                                            headers=connect_headers)
                                    with allure.step("状态码和返回值"):
                                        logger.info('状态码是{}'.format(str(r.status_code)))
                                        logger.info('返回值是{}'.format(str(r.text)))
                                    with allure.step("校验状态码"):
                                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                                    with allure.step("校验返回值"):
                                        assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)

    @allure.title('test_transfer_003')
    @allure.description('partner发起请求，把资金从partner转移到cabital账户')
    def test_transfer_003(self, partner):
        with allure.step("获取用户的account_vid"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                'account_vid']
        with allure.step("获得不同币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['credit']['allow']:
                    with allure.step("未操作前的balance"):
                        old_balance = ApiFunction.connect_get_balance(partner, account_vid, i['symbol'])['balances']
                    with allure.step("获得data"):
                        with allure.step("获得otp"):
                            mfaVerificationCode = get_mfa_code('richard')
                        external_id = generate_string(25)
                        data = {
                            'amount': str(giveAmount(i['symbol'])),
                            'symbol': i['symbol'],
                            'otp': str(mfaVerificationCode),
                            'direction': 'CREDIT',
                            'external_id': external_id
                        }
                    with allure.step("验签"):
                        unix_time = int(time.time())
                        nonce = generate_string(20) + str(time.time()).split('.')[0]
                        sign = ApiFunction.make_signature(unix_time=str(unix_time), method='POST',
                                                          url='/api/v1/accounts/{}/transfers'.format(account_vid),
                                                          connect_type=partner, nonce=nonce, body=json.dumps(data))
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                            'Partner_ID']
                        connect_headers['ACCESS-SIGN'] = sign
                        connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                        connect_headers['ACCESS-NONCE'] = nonce
                    with allure.step("把数字货币从cabital转移到bybit账户"):
                        r = session.request('POST', url='{}/accounts/{}/transfers'.format(connect_url, account_vid),
                                            data=json.dumps(data), headers=connect_headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                        if "PA043" not in r.text:
                            with allure.step("校验返回值"):
                                assert r.json()[
                                           'status'] == 'SUCCESS', "partner发起请求，把资金从partner转移到cabital账户失败，返回值是{}".format(
                                    r.text)
                        else:
                            assert r.status_code == 400, "http状态码不对，目前状态码是{}".format(r.status_code)
                            logger.info('由于每日限额超额，该笔transfer交易不成功，message是{}'.format(r.json()['message']))
                    if r.status_code != 400:
                        with allure.step("查询交易数据"):
                            sleep(2)
                            with allure.step("验签"):
                                unix_time = int(time.time())
                                nonce = generate_string(20) + str(time.time()).split('.')[0]
                                sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                                                  url='/api/v1/recon/transfers/{}'.format(external_id),
                                                                  connect_type=partner, nonce=nonce)
                                connect_headers['ACCESS-KEY'] = \
                                get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            with allure.step("查询转账记录"):
                                r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url, external_id),
                                                    headers=connect_headers)
                            with allure.step("状态码和返回值"):
                                logger.info('状态码是{}'.format(str(r.status_code)))
                                logger.info('返回值是{}'.format(str(r.text)))
                            with allure.step("校验状态码"):
                                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                            with allure.step("校验返回值"):
                                assert r.json()['external_id'] == external_id, "查询转账记录错误，返回值是{}".format(r.text)
                            with allure.step("操作后的balance"):
                                new_balance = ApiFunction.connect_get_balance(partner, account_vid, i['symbol'])[
                                    'balances']
                            with allure.step("获取手续费"):
                                if i['fees']['credit_fee']['value'] == '':
                                    credit_fee = '0'
                                else:
                                    credit_fee = i['fees']['credit_fee']['value']
                            with allure.step("计算用户balance变化"):
                                assert Decimal(old_balance) + Decimal(data['amount']) - Decimal(credit_fee) == Decimal(
                                    new_balance), "用户balance变化错误，操作前的balance是{},操作金额是{},操作后的金额是{}".format(old_balance,
                                                                                                          str(giveAmount(
                                                                                                              i[
                                                                                                                  'symbol'])),
                                                                                                          new_balance)
