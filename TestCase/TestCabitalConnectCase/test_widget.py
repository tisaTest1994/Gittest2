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
                                           "VND": {"min": "250000",
                                                   "max": "5000000000"}}}, '不传入partner_id, 取得全部conversion limit错误，返回值是{}'.format(
                r.text)

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
                        assert r.json()['limits'][
                                   y] == config_conversion, '传入partner_id, 取得全部conversion limit错误，币种是{}, config 配置内的值是{}, 接口返回值是{}'.format(
                            y, config_conversion, r.json()['limits'][y])

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
                        "account_vid":
                            get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                'richard']['account_vid'],
                        "user_ext_ref":
                            get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                'richard']['user_ref_id']
                    }
                    with allure.step("获取2fa code"):
                        mfaVerificationCode = get_mfa_code('richard')
                        headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                    with allure.step("transfer 交易"):
                        r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json(
                            file='partner_info.json')[get_json()['env']][partner]['Partner_ID']), data=json.dumps(data),
                                            headers=headers)
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
                        wallet_balance_latest), 'transfer币种是{},transfer前金额是{},transfer金额是{}，transfer后金额是{}'.format(
                        i['symbol'],
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
                                nonce = generate_string(20) + str(time.time()).split('.')[0]
                                sign = ApiFunction.make_signature(unix_time=str(unix_time), method='PUT',
                                                                  url='/api/v1/accounts/{}/transfers/{}'.format(
                                                                      account_vid, transfer_id), connect_type=partner,
                                                                  nonce=nonce, body=json.dumps(data))
                                connect_headers['ACCESS-KEY'] = \
                                get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
                                connect_headers['ACCESS-SIGN'] = sign
                                connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
                                connect_headers['ACCESS-NONCE'] = nonce
                            r = session.request('PUT',
                                                url='{}/accounts/{}/transfers/{}'.format(connect_url, account_vid,
                                                                                         transfer_id),
                                                data=json.dumps(data), headers=connect_headers)
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
                'user_ext_ref':
                    get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                        'user_ref_id'],
                'email': get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                    'email'],
                'redirect_url': 'https://www.baidu.com',
                'feature': 'onboarding'
            }
            r1 = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("验签"):
                sign = ApiFunction.get_link_sign(url=r1.url, partner=partner)
                connect_headers['ACCESS-SECRET'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                    'Secret_Key']
                params['signature'] = sign
            r = session.request('GET', url='{}/partner/link'.format(connect_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.url)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)

    @allure.title('test_widget_005')
    @allure.description('B+T')
    def test_widget_005(self, partner):
        with allure.step("币种兑选择"):
            pairs = ApiFunction.get_buy_crypto_currency(partner=partner, type='all')
        with allure.step("T 支持币种"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['transfer_debit']['allow']:
                    with allure.step("t_fee"):
                        t_fee = i['fees']['transfer_debit_fee']['value']
                    for z in pairs:
                        for x in get_json()['checkOutAreaList2']:
                            with allure.step("创建数字货币购买交易信息，ccy 是buy"):
                                sleep(1)
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
                                                        data=json.dumps(data), headers=headers2)
                                    with allure.step("校验状态码"):
                                        assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                            r.status_code)
                                        token = r.json()['token']
                                        dic = json.loads(r.text)
                                        if "issuer" in dic.keys():
                                            issuer = dic["issuer"]
                                        else:
                                            issuer = ''
                                while 1 < 2:
                                    crypto_list = ApiFunction.get_buy_crypto_transfer_list(150, t_fee, pairs=z,
                                                                                           ccy='buy', country=x)
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
                                                "partner_name":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'partner_name'],
                                                "partner_id":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'Partner_ID'],
                                                "user_ext_ref":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'account_vid_list']['richard']['user_ref_id'],
                                                "account_vid":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'account_vid_list']['richard']['account_vid'],
                                                "receive": {
                                                    "code": i['symbol'],
                                                    "amount": crypto_list['buy_amount']
                                                },
                                                "fee": {
                                                    "code": i['symbol'],
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
                                    r = session.request('POST', url='{}/acquiring/buy'.format(env_url),
                                                        data=json.dumps(data),
                                                        headers=headers)
                                    logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                                    logger.info('状态码是{}'.format(str(r.status_code)))
                                    logger.info('返回值是{}'.format(str(r.text)))
                                    if 'Invalid Quote' not in r.text:
                                        break
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['status'] == 1, "币种兑{},地区{},ccy是buy,checkout支付错误，当前返回值是{}".format(z,
                                                                                                                      x,
                                                                                                                      r.text)
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
                                        assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                            r.status_code)
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
                                        amount = 40000
                                    elif 'KRW' in z:
                                        amount = 1500000
                                    elif 'VND' in z:
                                        amount = 915000
                                    elif 'CZK' in z:
                                        amount = 3000
                                    elif 'JPY' in z:
                                        amount = 55000
                                    elif 'TWD' in z:
                                        amount = 2000
                                    elif 'THB' in z:
                                        amount = 2000
                                    elif 'IDR' in z:
                                        amount = 2000000
                                    elif 'MXN' in z:
                                        amount = 20000
                                    else:
                                        amount = 550
                                while 1 < 2:
                                    crypto_list = ApiFunction.get_buy_crypto_transfer_list(amount, t_fee, pairs=z,
                                                                                           ccy='spend', country=x)
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
                                                "partner_name":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'partner_name'],
                                                "partner_id":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'Partner_ID'],
                                                "user_ext_ref":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'account_vid_list']['richard']['user_ref_id'],
                                                "account_vid":
                                                    get_json(file='partner_info.json')[get_json()['env']][partner][
                                                        'account_vid_list']['richard']['account_vid'],
                                                "receive": {
                                                    "code": i['symbol'],
                                                    "amount": crypto_list['buy_amount']
                                                },
                                                "fee": {
                                                    "code": i['symbol'],
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
                                    r = session.request('POST', url='{}/acquiring/buy'.format(env_url),
                                                        data=json.dumps(data), headers=headers)
                                    logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                                    logger.info('状态码是{}'.format(str(r.status_code)))
                                    logger.info('返回值是{}'.format(str(r.text)))
                                    sleep(2)
                                    if 'Invalid Quote' not in r.text:
                                        break
                                with allure.step("校验状态码"):
                                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                                with allure.step("校验返回值"):
                                    assert r.json()['status'] == 1, "币种兑{},地区{},ccy是spend,checkout支付错误，当前返回值是{}".format(
                                        z, x, r.text)

    @allure.title('test_widget_006')
    @allure.description('B+W')
    def test_widget_006(self, partner):
        with allure.step("币种兑选择"):
            pairs = ApiFunction.get_buy_crypto_currency(partner=partner, type='all')
        for z in pairs:
            for x in get_json()['checkOutAreaList2']:
                with allure.step("创建数字货币购买交易信息，ccy 是buy"):
                    sleep(1)
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
                                            data=json.dumps(data), headers=headers2)
                        with allure.step("校验状态码"):
                            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                r.status_code)
                            token = r.json()['token']
                            dic = json.loads(r.text)
                            if "issuer" in dic.keys():
                                issuer = dic["issuer"]
                            else:
                                issuer = ''
                    while 1 < 2:
                        crypto_list = ApiFunction.get_buy_crypto_transfer_list(150, '12', pairs=z,
                                                                               ccy='buy', country=x)
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
                                "destination_type": 3,
                                "withdraw_txn": {
                                    "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                                    "method": "ERC20",
                                    "receive": {
                                        "code": "USDT",
                                        "amount": crypto_list['buy_amount']
                                    },
                                    "fee": {
                                        "code": "USDT",
                                        "amount": "12"
                                    },
                                    "tx_hash": "1234"
                                },
                                "fee": {
                                    "code": (str(crypto_list['pairs']).split('-'))[1],
                                    "amount": crypto_list['transfer_fee']
                                }
                            }
                        }
                        logger.info('checkout传入参数是{}'.format(data))
                        r = session.request('POST', url='{}/acquiring/buy'.format(env_url),
                                            data=json.dumps(data),
                                            headers=headers)
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                        if 'Invalid Quote' not in r.text:
                            break
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, "币种兑{},地区{},ccy是buy,checkout支付错误，当前返回值是{}".format(z,
                                                                                                          x,
                                                                                                          r.text)
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
                            assert r.status_code == 201, "获取checkout token返回的http状态码不对，目前状态码是{}".format(
                                r.status_code)
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
                            amount = 40000
                        elif 'KRW' in z:
                            amount = 1500000
                        elif 'VND' in z:
                            amount = 715000
                        elif 'CZK' in z:
                            amount = 3000
                        elif 'JPY' in z:
                            amount = 55000
                        elif 'TWD' in z:
                            amount = 2000
                        elif 'THB' in z:
                            amount = 2000
                        elif 'IDR' in z:
                            amount = 80000000
                        elif 'EGP' in z:
                            amount = 2000
                        elif 'MXN' in z:
                            amount = 20000
                        else:
                            amount = 550
                    while 1 < 2:
                        crypto_list = ApiFunction.get_buy_crypto_transfer_list(amount, '12', pairs=z,
                                                                               ccy='spend', country=x)
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
                                "destination_type": 3,
                                "withdraw_txn": {
                                    "address": "0xA7185FBEE96B605709D9659894066dF21cc87f05",
                                    "method": "ERC20",
                                    "receive": {
                                        "code": "USDT",
                                        "amount": crypto_list['buy_amount']
                                    },
                                    "fee": {
                                        "code": "USDT",
                                        "amount": "12"
                                    },
                                    "tx_hash": "1234"
                                },
                                "fee": {
                                    "code": (str(crypto_list['pairs']).split('-'))[1],
                                    "amount": crypto_list['transfer_fee']
                                }
                            }
                        }
                        logger.info('checkout传入参数是{}'.format(data))
                        r = session.request('POST', url='{}/acquiring/buy'.format(env_url),
                                            data=json.dumps(data), headers=headers)
                        logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                        sleep(2)
                        if 'Invalid Quote' not in r.text:
                            break
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert r.json()['status'] == 1, "币种兑{},地区{},ccy是spend,checkout支付错误，当前返回值是{}".format(
                            z, x, r.text)

    @allure.title('test_widget_007')
    @allure.description('transfer debit 交易小于最小值')
    def test_widget_007(self, partner):
        with allure.step("划转"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['transfer_debit']['allow'] is True:
                    if i['config']['transfer_debit']['min'] != '-1':
                        data = {
                            "amount": str(Decimal(i['config']['transfer_debit']['min']) - Decimal(0.01)),
                            "code": i['symbol'],
                            "direction": "DEBIT",
                            "account_vid":
                                get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                    'richard']['account_vid'],
                            "user_ext_ref":
                                get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                    'richard']['user_ref_id']
                        }
                        with allure.step("获取2fa code"):
                            mfaVerificationCode = get_mfa_code('richard')
                            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                        with allure.step("transfer 交易"):
                            r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json(
                                file='partner_info.json')[get_json()['env']][partner]['Partner_ID']),
                                                data=json.dumps(data), headers=headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA003', "transfer 使用小于最小值的订单交易错误，返回值是{}".format(r.text)

    @allure.title('test_widget_008')
    @allure.description('transfer debit 交易大于最大值')
    def test_widget_008(self, partner):
        with allure.step("划转"):
            for i in get_json(file='partner_info.json')[get_json()['env']][partner]['config_info']['currencies']:
                if i['config']['transfer_debit']['allow'] is True:
                    if i['config']['transfer_debit']['max'] != '-1':
                        data = {
                            "amount": str(Decimal(i['config']['transfer_debit']['max']) + Decimal(0.01)),
                            "code": i['symbol'],
                            "direction": "DEBIT",
                            "account_vid":
                                get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                    'richard']['account_vid'],
                            "user_ext_ref":
                                get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list'][
                                    'richard']['user_ref_id']
                        }
                        with allure.step("获取2fa code"):
                            mfaVerificationCode = get_mfa_code('richard')
                            headers['X-Mfa-Otp'] = str(mfaVerificationCode)
                        with allure.step("transfer 交易"):
                            r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url, get_json(
                                file='partner_info.json')[get_json()['env']][partner]['Partner_ID']),
                                                data=json.dumps(data), headers=headers)
                        with allure.step("状态码和返回值"):
                            logger.info('状态码是{}'.format(str(r.status_code)))
                            logger.info('返回值是{}'.format(str(r.text)))
                        with allure.step("校验状态码"):
                            assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
                        with allure.step("校验返回值"):
                            assert r.json()['code'] == 'PA004', "transfer 使用大于最大值的订单交易错误，返回值是{}".format(r.text)

    @allure.title('test_widget_009')
    @allure.description('transfer debit 使用不支持的币种')
    def test_widget_009(self, partner):
        with allure.step("划转"):
            data = {
                "amount": '50',
                "code": 'CHF',
                "direction": "DEBIT",
                "account_vid":
                    get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                        'account_vid'],
                "user_ext_ref":
                    get_json(file='partner_info.json')[get_json()['env']][partner]['account_vid_list']['richard'][
                        'user_ref_id']
            }
            with allure.step("获取2fa code"):
                mfaVerificationCode = get_mfa_code('richard')
                headers['X-Mfa-Otp'] = str(mfaVerificationCode)
            with allure.step("transfer 交易"):
                r = session.request('POST', url='{}/connect/{}/transfer'.format(env_url,
                                                                                get_json(file='partner_info.json')[
                                                                                    get_json()['env']][partner][
                                                                                    'Partner_ID']),
                                    data=json.dumps(data), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 400, "http 状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert r.json()['code'] == 'PA019', "transfer 交易错误，返回值是{}".format(r.text)

