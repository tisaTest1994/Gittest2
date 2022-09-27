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
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
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
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
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
                                connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            with allure.step("查询转账记录"):
                                r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url, external_id), headers=connect_headers)
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
                        assert Decimal(old_balance) - Decimal(data['amount']) == Decimal(new_balance), "用户balance变化错误，操作前的balance是{},操作金额是{},操作后的金额是{}".format(old_balance, str(giveAmount(i['symbol'])), new_balance)

    @allure.title('test_transfer_002')
    @allure.description('partner发起请求，把资金从cabital转移到partner账户并且关联C+T交易')
    def test_transfer_002(self, partner):
        with allure.step("获取用户的account_vid"):
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
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
                                connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
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
            account_vid = get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard']['account_vid']
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
                        connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
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
                                connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            with allure.step("查询转账记录"):
                                r = session.request('GET', url='{}/recon/transfers/{}'.format(connect_url, external_id), headers=connect_headers)
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
                                credit_fee = i['fees']['credit_fee']['value']
                            with allure.step("计算用户balance变化"):
                                assert Decimal(old_balance) + Decimal(data['amount']) - Decimal(credit_fee) == Decimal(
                                    new_balance), "用户balance变化错误，操作前的balance是{},操作金额是{},操作后的金额是{}".format(old_balance,
                                                                                                          str(giveAmount(
                                                                                                              i[
                                                                                                                  'symbol'])),
                                                                                                          new_balance)

    @allure.title('test_transfer_004')
    @allure.description('B+T')
    def test_transfer_004(self, partner):
        with allure.step("币种兑选择"):
            pairs = ApiFunction.get_buy_crypto_currency(type='all')
            pairs.remove('USDT-IDR')
        with allure.step("t_fee"):
            t_fee = '0.99'
        for z in pairs:
            for x in get_json()['checkOutAreaList2']:
                # with allure.step("创建数字货币购买交易信息，ccy 是buy"):
                #     with allure.step("get token"):
                #         data = {
                #             "type": "card",
                #             "number": "4242424242424242",
                #             "expiry_month": 6,
                #             "expiry_year": 2025,
                #             "name": "Bruce Wayne",
                #             "cvv": "100",
                #             "billing_address": {
                #                 "address_line1": "Checkout.com",
                #                 "address_line2": "90 Tottenham Court Road",
                #                 "city": "London",
                #                 "state": "London",
                #                 "zip": "W1T 4TJ",
                #                 "country": x
                #             }
                #         }
                #         headers2 = {
                #             "Authorization": "Bearer pk_sbox_cqecp4mj36curomekpmzd42cjeg",
                #             "Content-Type": "application/json"
                #         }
                #         r = session.request('POST', url='https://api.sandbox.checkout.com/tokens',
                #                             data=json.dumps(data),
                #                             headers=headers2)
                #         with allure.step("校验状态码"):
                #             assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(r.status_code)
                #             token = r.json()['token']
                #             dic = json.loads(r.text)
                #             if "issuer" in dic.keys():
                #                 issuer = dic["issuer"]
                #             else:
                #                 issuer = ''
                #     while 1 < 2:
                #         crypto_list = ApiFunction.get_buy_crypto_transfer_list(150, t_fee, pairs=z, ccy='buy', country=x)
                #         data = {
                #             "buy": {
                #                 "code": (str(crypto_list['pairs']).split('-'))[0],
                #                 "amount": crypto_list['buy_amount']
                #             },
                #             "spend": {
                #                 "code": (str(crypto_list['pairs']).split('-'))[1],
                #                 "amount": crypto_list['spend_amount']
                #             },
                #             "quote": {
                #                 "id": crypto_list['quote_id'],
                #                 "amount": crypto_list['quote']
                #             },
                #             "major_code": crypto_list['major_code'],
                #             "fee": {
                #                 "code": (str(crypto_list['pairs']).split('-'))[1],
                #                 "amount": crypto_list['service_charge']
                #             },
                #             "total_amount": crypto_list['total_spend_amount'],
                #             "card": {
                #                 "type": 1,
                #                 "token": token,
                #                 "expiry_month": '6',
                #                 "expiry_year": str(r.json()['expiry_year']),
                #                 "scheme": str(r.json()['scheme']),
                #                 "last": str(r.json()['last4']),
                #                 "bin": str(r.json()['bin']),
                #                 "card_type": str(r.json()['card_type']),
                #                 "issuer": issuer,
                #                 "issuer_country": x
                #             },
                #             "bind_card": True,
                #             "card_holder_name": "Ting DP319",
                #             "billing_address": {
                #                 "country_code": "CN",
                #                 "state": "",
                #                 "city": "shanghai",
                #                 "post_code": "210000",
                #                 "street_line_1": "Shanghai",
                #                 "street_line_2": "Shab"
                #             },
                #             "nonce": generate_string(30),
                #             "check_amount": True,
                #             "destination": {
                #                 "destination_type": 2,
                #                 "transfer_txn": {
                #                     "partner_name": "latibac",
                #                     "partner_id": "90edccf2-ebee-4b35-9f87-c90bfcd1c174",
                #                     "user_ext_ref": "996465012836982998",
                #                     "account_vid": "728ded80-1e19-4146-b8ff-a1a893590e33",
                #                     "receive": {
                #                         "code": "USDT",
                #                         "amount": crypto_list['buy_amount']
                #                     },
                #                     "fee": {
                #                         "code": "USDT",
                #                         "amount": str(t_fee)
                #                     }
                #                 },
                #                 "fee": {
                #                     "code": (str(crypto_list['pairs']).split('-'))[1],
                #                     "amount": crypto_list['transfer_fee']
                #                 }
                #             }
                #         }
                #         logger.info('checkout传入参数是{}'.format(data))
                #         r = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data),
                #                             headers=headers)
                #         logger.info('状态码是{}'.format(str(r.status_code)))
                #         logger.info('返回值是{}'.format(str(r.text)))
                #         if 'Invalid Quote' not in r.text:
                #             break
                #     with allure.step("校验状态码"):
                #         assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                #     with allure.step("校验返回值"):
                #         assert r.json()['status'] == 1, "币种兑{},地区{},ccy是buy,checkout支付错误，当前返回值是{}".format(z, x, r.text)
                with allure.step("创建数字货币购买交易信息，ccy 是spend"):
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
                            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(r.status_code)
                            token = r.json()['token']
                            dic = json.loads(r.text)
                            if "issuer" in dic.keys():
                                issuer = dic["issuer"]
                            else:
                                issuer = ''
                    with allure.step("解决最大/最小值"):
                        if 'CLF' in z:
                            amount = 1000
                        elif 'CLP' in z:
                            amount = 90000
                        elif 'COP' in z:
                            amount = 490000
                        elif 'LKR' in z:
                            amount = 4000
                        elif 'KRW' in z:
                            amount = 1500000
                        elif 'VND' in z:
                            amount = 315000
                        elif 'CZK' in z:
                            amount = 3000
                        elif 'JPY' in z:
                            amount = 55000
                        else:
                            amount = 550
                    while 1 < 2:
                        crypto_list = ApiFunction.get_buy_crypto_transfer_list(amount, t_fee, pairs=z, ccy='spend', country=x)
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
                            "check_amount": True,
                            "destination": {
                                "destination_type": 2,
                                "transfer_txn": {
                                    "partner_name": "latibac",
                                    "partner_id": "90edccf2-ebee-4b35-9f87-c90bfcd1c174",
                                    "user_ext_ref": "996465012836982998",
                                    "account_vid": "728ded80-1e19-4146-b8ff-a1a893590e33",
                                    "receive": {
                                        "code": "USDT",
                                        "amount": crypto_list['buy_amount']
                                    },
                                    "fee": {
                                        "code": "USDT",
                                        "amount": str(t_fee)
                                    }
                                },
                                "fee": {
                                    "code": (str(crypto_list['pairs']).split('-'))[1],
                                    "amount": crypto_list['transfer_fee']
                                }
                            }
                        }
                        logger.info('checkout传入参数是{}'.format(data))
                        r = session.request('POST', url='{}/acquiring/buy'.format(env_url), data=json.dumps(data), headers=headers)
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                        if 'Invalid Quote' not in r.text:
                            break
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, "币种兑{},地区{},ccy是spend,checkout支付错误，当前返回值是{}".format(z, x, r.text)