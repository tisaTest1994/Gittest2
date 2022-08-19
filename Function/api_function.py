from run import *
from Function.operate_sql import *
import webbrowser


class ApiFunction:

    # 获取用户token
    @staticmethod
    def get_account_token(account=get_json()['email']['email'], password=get_json()['email']['password'], type='cabital'):
        data = {
            "username": account,
            "password": password
        }
        if type == 'operate':
            r = session.request('POST', url='{}/operator/operator/login'.format(operateUrl), data=json.dumps(data), headers=headers)
        elif type == 'monitor':
            data['grant_type'] = 'password'
            data['client_id'] = get_json()['kyc'][get_json()['env']]['client_id']
            headers['Authorization'] = get_json()['kyc'][get_json()['env']]['Authorization']
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            r = session.request('POST', url='{}/auth/realms/{}/protocol/openid-connect/token'.format(get_json()['kyc'][get_json()['env']]['authServer'], get_json()['kyc'][get_json()['env']]['realm']), data=urlencode(data), headers=headers)
            return r.json()['access_token']
        else:
            headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
            headers['X-Browser-Key'] = 'yilei_test'
            r = session.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data), headers=headers)
        if r.text is None:
            return "login is error, return is {}".format(r.text)
        elif 'accessToken' not in r.text:
            return "login is error, return is {}".format(r.text)
        else:
            return r.json()['accessToken']

    # 加headers，只能默认账户,使用usd
    @staticmethod
    def add_headers(account=get_json()['email']['email'], password=get_json()['email']['password'], currency=get_json()['preference_currency']):
        headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
        headers['X-Browser-Key'] = 'yilei_api_test'
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account, password=password)
        headers['X-Currency'] = currency
        headers['Accept-Language'] = get_json()['language']

    # 获取user_id
    @staticmethod
    def get_user_id(account_id=None, email=None):
        data = {
            "accountId": account_id,
            "email": email
        }
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        r = session.request('POST', url='{}/operator/operator/users/search'.format(operateUrl), data=json.dumps(data),
                            headers=headers)
        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accounts' in r.text, "查找user_id错误，返回值是{}".format(r.text)
        return r.json()['accounts'][0]['userId']

    # 获取用户状态
    @staticmethod
    def get_account_status(account_id=None, user_id=None, email=None):
        data = {
            "accountId": account_id,
            "userId": user_id,
            "email": email
        }
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')
        r = session.request('POST', url='{}/operator/operator/users/search'.format(operateUrl), data=json.dumps(data),
                            headers=headers)
        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accounts' in r.text, "查找user_id错误，返回值是{}".format(r.text)
        return r.json()['accounts'][0]['status']
    
    # 注册
    @staticmethod
    def sign_up(account=generate_email(), password=get_json()['email']['password']):
        data = {
            "emailAddress": account,
            "password": password,
            "verificationCode": "666666"
        }
        r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "注册用户错误，返回值是{}".format(r.text)
        return r.json()['accessToken']

    # 提现ETH获取交易id
    @staticmethod
    def get_payout_transaction_id(amount='0.02', address='0x428DA40C585514022b2eB537950d5AB5C7365a07', code_type='ETH'):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
        mfaVerificationCode = get_mfa_code()
        headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
        if code_type == 'BTC':
            data = {
                "amount": amount,
                "code": code_type,
                "address": address,
                "partner_id": '800b482d-0a88-480a-aae7-741f77a572f4',
                'user_ext_ref': '988518746672869376'
            }
        else:
            data = {
                "amount": amount,
                "code": code_type,
                "address": address,
                "method": "ERC20",
                "partner_id": '800b482d-0a88-480a-aae7-741f77a572f4',
                'user_ext_ref': '988518746672869376'
            }
        r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                            headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json()['transaction_id'] is not None, "payout币种是{}，金额是{}错误，返回值是{}".format(data['code'], data['amount'], r.text)
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId):
        r1 = session.request('GET', url=' {}/earn/products/{}/next_yield'.format(env_url, productId), headers=headers)
        return r1.json()['next_yield']

    # 获取当前换汇报价
    @staticmethod
    def get_quote(pair):
        r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, pair), headers=headers)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r.json()['valid_until'])))
        logger.info('获得报价的服务器时间是{},换汇币种对是{},换汇价格是{}'.format(strTime, pair, r.json()))
        return r.json()

    # 获取钱包指定币种某个交易状态的数量
    @staticmethod
    def get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE', amount_type='amount'):
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        for i in r.json():
            if i['code'] == type and i['wallet_type'] == wallet_type:
                for y in i['balances']:
                    if y['type'] == balance_type:
                        balance_type_available_amount = y[amount_type]
        return balance_type_available_amount

    # 获取钱包指定币种某个交易状态的数量
    @staticmethod
    def get_crypto_frozen_number(type='BTC', balance_type='BALANCE_TYPE_FROZEN', wallet_type='BALANCE', amount_type='amount'):
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers)
        for i in r.json():
            if i['code'] == type and i['wallet_type'] == wallet_type:
                for y in i['balances']:
                    if y['type'] == balance_type:
                        balance_type_frozen_amount = y[amount_type]
        return balance_type_frozen_amount

    # 获取钱包指定币种全部数量
    @staticmethod
    def get_all_crypto_number():
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        crypto_list = get_json()['crypto_list']
        number_dict = {}
        for i in r.json()['wallets']:
            for y in crypto_list:
                if i['code'] == y:
                    number_dict[y] = i['amount']
        return number_dict

    # 获取当前某个币的当前资产价值，用USD结算
    @staticmethod
    def get_crypto_abs_amount(type='BTC'):
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        for i in r.json()['wallets']:
            if i['code'] == type:
                return i['abs_amount']

    # 获得今日损益
    @staticmethod
    def get_today_increase():
        crypto_list = get_json()['crypto_list']
        # 当前全部货币数量
        number_dict = ApiFunction.get_all_crypto_number()
        # 今天utc0点时间
        yesterday_time = datetime.now(tz=pytz.timezone('UTC')).strftime("%Y%m%d")
        today_increase = {}
        for i in crypto_list:
            # 目前货币数量
            number = number_dict[i]
            data = {
                "pagination_request": {
                    "cursor": "0",
                    "page_size": 99999
                },
                "user_txn_sub_types": [1, 2, 4, 6, 7],
                "statuses": [2],
                "codes": [i],
                "created_from": int(get_zero_utc_time())
            }
            r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers)
            for y in r.json()['transactions']:
                if y['user_txn_sub_type'] == 1:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['buy_currency']['code'] == i:
                    number = float(number) - float(json.loads(y['details'])['buy_currency']['amount'])
                elif y['user_txn_sub_type'] == 2 and json.loads(y['details'])['sell_currency']['code'] == i:
                    number = float(number) + float(json.loads(y['details'])['buy_currency']['amount'])
                elif y['user_txn_sub_type'] == 4:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 6:
                    number = float(number) + float(json.loads(y['details'])['currency']['amount'])
                elif y['user_txn_sub_type'] == 7:
                    number = float(number) - float(json.loads(y['details'])['currency']['amount'])
            # 获取昨天UTC23:59的汇率价格
            quote = sqlFunction.get_crypto_quote(type=i, day_time=yesterday_time)
            yesterday_amount = (Decimal(number) * Decimal(quote)).quantize(Decimal('0.00'), ROUND_FLOOR)
            # 获得当前价格
            now_amount = ApiFunction.get_crypto_abs_amount(type=i)
            today_increase[i] = (Decimal(yesterday_amount) - Decimal(now_amount)).quantize(Decimal('0.00'), ROUND_FLOOR)
        return str(today_increase)

    # 获得总持仓成本
    @staticmethod
    def get_cost(type='ETH'):
        # 获得交易记录
        data = {
            "pagination_request": {
                "cursor": "0",
                "page_size": 9999999
            },
            "user_txn_sub_types": [1, 2, 6],
            "statuses": [2],
            "codes": [type]
        }
        r = session.request('POST', url='{}/txn/query'.format(env_url), data=json.dumps(data), headers=headers,
                            timeout=10)
        for y in r.json()['transactions']:
            cost = 0
            if y['user_txn_sub_type'] == 1:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
            if y['user_txn_sub_type'] == 2:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
            if y['user_txn_sub_type'] == 6:
                order_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(y['updated_at']))
                amount = json.loads(y['details'])['currency']['amount']

    # 查询交易状态
    @staticmethod
    def get_transaction_status(transaction_id, type):
        params = {
            'txn_sub_type': type
        }
        r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
        return r.json()['transaction']['status']

    # 获取一天cfx数据
    @staticmethod
    def get_one_day_cfx_info(day_time=(datetime.now(tz=pytz.timezone('UTC')) + timedelta(days=-1)).strftime("%Y-%m-%d")):
        cfx_book = get_json()['cfx_book']
        time_list = get_zero_time(day_time=day_time)
        cfx_info = []
        for i in time_list:
            info = sqlFunction().get_cfx_detail(end_time=i)
            if info is not None and '()' not in str(info):
                cfx_info.append(info)
        cfx_list = []
        for y in cfx_info:
            for z in y:
                cfx_dict = {}
                if z['trading_direction'] == 1:
                    cfx_dict['buy_us'] = str(cfx_book[str(z['book_id'])]).split('-')[1]
                    cfx_dict['sell_us'] = str(cfx_book[str(z['book_id'])]).split('-')[0]
                    cfx_dict['buy_us_amount'] = z['pnl_amount']
                    cfx_dict['sell_us_amount'] = z['trading_amount']
                    cfx_dict['profit'] = z['gnl']
                    cfx_dict['order_time'] = z['aggregation_no']
                    profit = Decimal(z['trading_amount']) * Decimal(z['cost'])
                    if '.' in str(profit):
                        if str(cfx_book[str(z['book_id'])]).split('-')[1] == 'BTC' or \
                                str(cfx_book[str(z['book_id'])]).split('-')[1] == 'ETH':
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
                        elif str(cfx_book[str(z['book_id'])]).split('-')[1] == 'USDT':
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
                        else:
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:2])
                    profit = Decimal(profit) - Decimal(z['pnl_amount'])
                    assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
                elif z['trading_direction'] == 2:
                    cfx_dict['buy_us'] = str(cfx_book[str(z['book_id'])]).split('-')[0]
                    cfx_dict['sell_us'] = str(cfx_book[str(z['book_id'])]).split('-')[1]
                    cfx_dict['buy_us_amount'] = z['trading_amount']
                    cfx_dict['sell_us_amount'] = z['pnl_amount']
                    cfx_dict['profit'] = z['gnl']
                    cfx_dict['order_time'] = z['aggregation_no']
                    profit = Decimal(z['trading_amount']) * Decimal(z['cost'])
                    if '.' in str(profit):
                        if str(cfx_book[str(z['book_id'])]).split('-')[1] == 'BTC' or \
                                str(cfx_book[str(z['book_id'])]).split('-')[1] == 'ETH':
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:8])
                        elif str(cfx_book[str(z['book_id'])]).split('-')[1] == 'USDT':
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:6])
                        else:
                            profit = '{}.{}'.format(str(profit).split('.')[0], str(profit).split('.')[1][:2])
                    profit = Decimal(z['pnl_amount']) - Decimal(profit)
                    assert Decimal(profit) == Decimal(z['gnl']), '预计损益是{}，数据库返回是{}'.format(profit, z['gnl'])
                cfx_dict['cost'] = z['cost']
                cfx_list.append(cfx_dict)
        return cfx_list

    # 验签
    @staticmethod
    def make_access_sign(unix_time, method, url, body='', key='', nonce=''):
        if key == 'cabital pay':
            if nonce == '':
                if body == '':
                    data = '{}{}{}'.format(unix_time, method, url)
                else:
                    data = '{}{}{}{}'.format(unix_time, method, url, body)
            else:
                if body == '':
                    data = '{}{}{}{}'.format(unix_time, method, nonce, url)
                else:
                    data = '{}{}{}{}{}'.format(unix_time, method, nonce, url, body)
            key = get_json()['cabital_pay'][get_json()['env']]['secretKey']
            data = data.encode("utf-8")
            #sign = str(sign, 'utf-8')
        else:
            if nonce == '':
                if key == '':
                    key = get_json()['kyc'][get_json()['env']]['kycSecretKey']
                elif key == 'infinni games':
                    key = get_json()['infinni_games']['secretKey']
                if body == '':
                    data = '{}{}{}'.format(unix_time, method, url)
                else:
                    data = '{}{}{}{}'.format(unix_time, method, url, body)
            else:
                if key == '':
                    key = get_json()['connect'][get_json()['env']]['bybit']['secretKey']
                elif key == 'infinni games':
                    key = get_json()['infinni_games']['secretKey']
                if body == '':
                    data = '{}{}{}{}'.format(unix_time, method, nonce, url)
                else:
                    data = '{}{}{}{}{}'.format(unix_time, method, nonce, url, body)
            key = key.encode('utf-8')
            message = data.encode('utf-8')
            sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
            sign = str(sign, 'utf-8')
        return sign

    # 验签 sha256
    @staticmethod
    def infinni_games_access_sign(url):
        key = get_json()['infinni_games']['secretKey']
        key = key.encode('utf-8')
        message = url.encode('utf-8')
        sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
        sign = str(sign, 'utf-8')
        return sign

    # 获得webhook
    @staticmethod
    def get_webhook(type='kyc'):
        conn = http.client.HTTPSConnection('api.pipedream.com')
        webhook = get_json()[type][get_json()['env']]['webhook']
        conn.request("GET", '/v1/sources/{}/events'.format(webhook), '', {'Authorization': 'Bearer {}'.format(get_json()[type][get_json()['env']]['api_key'])})
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    # 删除webhook
    @staticmethod
    def delete_old_webhook(type='kyc'):
        conn = http.client.HTTPSConnection('api.pipedream.com')
        webhook = get_json()['kyc'][get_json()['env']]['webhook']
        conn.request("DELETE", '/v1/sources/{}/events'.format(webhook), '', {'Authorization': 'Bearer {}'.format(get_json()[type][compliance_service_type]['api_key'])})
        conn.getresponse()

    # 验证webhook需要的信息
    @staticmethod
    def check_webhook_info(path, caseSystemId, action='', suggestion='', decision=''):
        sleep_time = 0
        while sleep_time < 500:
            if 'operator' in path:
                return True
            else:
                webhook_info = ApiFunction.get_webhook()
                for y in json.loads(webhook_info)['data']:
                    if y['e']['path'] == path:
                        if 'case' in path and y['e']['body']['caseSystemId'] == caseSystemId:
                            webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'],
                                                                        method=y['e']['method'], url=y['e']['path'],
                                                                        body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                            logger.info(
                                '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, action:{}, suggestion:{}, decision:{}'.format(
                                    path, caseSystemId, action, suggestion, decision))
                            return True
                        elif 'case/reviewed' in path and y['e']['body']['caseSystemId'] == caseSystemId and \
                                y['e']['body']['suggestion'] == suggestion:
                            webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'],
                                                                        method=y['e']['method'], url=y['e']['path'],
                                                                        body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                            logger.info(
                                '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, action:{}, suggestion:{}, decision:{}'.format(
                                    path, caseSystemId, action, suggestion, decision))
                            return True
                        elif 'case/completed' in path and y['e']['body']['caseSystemId'] == caseSystemId and \
                                y['e']['body']['decision'] == decision:
                            webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'],
                                                                        method=y['e']['method'], url=y['e']['path'],
                                                                        body=y['e']['bodyRaw'])
                            assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                            logger.info(
                                '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, action:{}, suggestion:{}, decision:{}'.format(
                                    path, caseSystemId, action, suggestion, decision))
                            return True
            sleep(10)
            sleep_time = sleep_time + 10
        assert False, '未找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, action:{}, suggestion:{}, decision:{}'.format(
            path, caseSystemId, action, suggestion, decision)

    # 活期申购
    @staticmethod
    def subscribe():
        r = session.request('GET', url='{}/earn/products'.format(env_url), headers=headers)
        product_list = random.choice(r.json())
        code = product_list['code']
        product_id = product_list['product_id']
        if code == 'USDT':
            amount = '20'
        else:
            amount = "0.01327"
        data = {
            "tx_type": 1,
            "amount": amount,
            "code": code
        }
        r = session.request('POST', url='{}/earn/products/{}/transactions'.format(env_url, product_id), data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'tx_id' in r.text, "赎回错误，返回值是{}".format(r.text)
        return {'product_id': product_id, 'code': code, 'tx_id': r.json()['tx_id']}

    # 定期申购
    @staticmethod
    def subscribe_fix(auto_renew=False):
        r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        product_list = random.choice(random.choice(r.json())['products'])
        logger.info('项目信息是{}'.format(product_list))
        code = product_list['code']
        product_id = product_list['product_id']
        if code == 'USDT':
            amount = '1000'
            interest_amount = str(((Decimal(amount) * (Decimal(product_list['apy']) / 100) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(product_list['tenor']))
        else:
            amount = "1"
            interest_amount = str(((Decimal(amount) * (Decimal(product_list['apy']) / 100) / Decimal(365)).quantize(Decimal('0.00000000'), ROUND_FLOOR)) * Decimal(product_list['tenor']))
        data = {
            "subscribe_amount": {
                "code": code,
                "amount": amount
            },
            "maturity_interest": {
                "code": code,
                "amount": interest_amount
            },
            "auto_renew": auto_renew
        }
        logger.info('申购信息是{}'.format(data))
        r = session.request('POST', url='{}/earn/fix/products/{}/transactions'.format(env_url, product_id), data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'tx_id' in r.text, "赎回错误，返回值是{}".format(r.text)
        return {'product_id': product_id, 'code': code, 'tx_id': r.json()['tx_id']}

    # 收取验证码先发再收
    @staticmethod
    def get_verification_code(type, account):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
        data = {
            "email": account,
            "type": type
        }
        r = session.request('POST', url='{}/account/verify-code/email'.format(env_url), data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "收取验证码失败，返回值是{}".format(r.text)
        code = ApiFunction.get_email_code(type)
        return code

    # 收取邮箱验证码，只收取
    @staticmethod
    def get_email_code(type):
        sleep(5)
        sleep_time = 0
        while sleep_time < 10:
            email_info = get_email()
            if type == 'REGISTRY':
                if get_json(file='multiple_languages_email.json')['EM001'] in email_info['title']:
                    break
            elif type == 'FORGET_PASSWORD':
                if get_json(file='multiple_languages_email.json')['EM007'] in email_info['title']:
                    break
            elif type == 'ENABLE_MFA':
                if get_json(file='multiple_languages_email.json')['EM014'] in email_info['title']:
                    break
            elif type == 'DISABLE_MFA':
                if get_json(file='multiple_languages_email.json')['EM016'] in email_info['title']:
                    break
            elif type == 'MFA_EMAIL':
                if get_json(file='multiple_languages_email.json')['EM011'] in email_info['title']:
                    break
            sleep_time = sleep_time + 5
            sleep(10)
        code = str(email_info['body']).split('"code":')[1].split('"')[1]
        return code

    # 校验验证码
    @staticmethod
    def verify_verification_code(type, email, code):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=email)
        data = {
            "email": email,
            "type": type,
            "code": code
        }
        r = session.request('POST', url='{}/account/verify-code/email/verify'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('状态码是{}'.format(str(r.status_code)))
        logger.info('返回值是{}'.format(str(r.text)))
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "校验验证码失败，返回值是{}".format(r.text)

    # 换汇
    @staticmethod
    def cfx_hedging_pairs(pair):
        with allure.step("获取直盘或者拆盘汇率对"):
            sql = "select books from split_setting where pair = '{}';".format(pair)
            books = sqlFunction().connect_mysql('hedging', sql=sql, type=1)
            pair_list = {}
            books = json.loads(books['books'])
            for i in books['books']:
                pair_list[i['id']] = i['pair']
            if len(pair_list.keys()) == 1:
                logger.info('获得直盘币种对{}'.format(pair_list))
                return pair_list
            else:
                logger.info('获得拆盘币种对{}'.format(pair_list))
                return pair_list

    # 指定换汇币种对和major_ccy币种，随机生成换汇金额。
    @staticmethod
    def cfx_random_number(cfx_dict):
        with allure.step("major_ccy 是buy值"):
            if cfx_dict['buy'] == cfx_dict['major_ccy']:
                if cfx_dict['buy'] == 'BTC' or cfx_dict['buy'] == 'ETH':
                    buy_amount = random.uniform(0.02, 0.199)
                else:
                    buy_amount = random.uniform(25, 1000.11)
                buy_amount = crypto_len(number=buy_amount, type=cfx_dict['buy'])
                quote = ApiFunction.get_quote('{}-{}'.format(cfx_dict['buy'], cfx_dict['sell']))
                sell_amount = str(float(buy_amount) * float(quote['quote']))
                sell_amount = crypto_len(number=sell_amount, type=cfx_dict['sell'])
        with allure.step("major_ccy 是sell值"):
            if cfx_dict['sell'] == cfx_dict['major_ccy']:
                if cfx_dict['sell'] == 'BTC' or cfx_dict['sell'] == 'ETH':
                    sell_amount = random.uniform(0.02, 0.199)
                else:
                    sell_amount = random.uniform(25, 1000.11)
                sell_amount = crypto_len(number=sell_amount, type=cfx_dict['sell'])
                quote = ApiFunction.get_quote('{}-{}'.format(cfx_dict['buy'], cfx_dict['sell']))
                buy_amount = str(float(sell_amount) / float(quote['quote']))
                buy_amount = crypto_len(number=buy_amount, type=cfx_dict['buy'])
        return {"buy": cfx_dict['buy'], "sell": cfx_dict['sell'], "buy_amount": buy_amount, "sell_amount": sell_amount, "quote": quote, "major_ccy": cfx_dict['major_ccy']}

    # 获得全部币种的list
    @staticmethod
    def balance_list():
        crypto_list = get_json()['crypto_list']
        cash_list = get_json()['cash_list']
        return crypto_list + cash_list

    # 获得全部换汇币种对的list
    @staticmethod
    def get_cfx_list():
        cfx_list = []
        r = session.request('GET', url='{}/txn/cfx/codes'.format(env_url))
        balance_list = ApiFunction.balance_list()
        with allure.step("从metadata接口获取已开启的币种信息"):
            fiat_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
            fiat_list_metadata = fiat_metadata.json()['currencies']
            fiat_all_metadata = fiat_list_metadata.keys()
        with allure.step("如在metada中关闭，则去除"):
            for m in range(0, len(balance_list)):
                if balance_list[m] not in fiat_all_metadata:
                    balance_list.remove(balance_list[m])
        for i in balance_list:
            balance_list2 = r.json()['codes'][i]
            with allure.step("从metadata接口获取已开启的币种信息"):
                fiat_metadata = session.request('GET', url='{}/core/metadata'.format(env_url), headers=headers)
                fiat_list_metadata = fiat_metadata.json()['currencies']
                fiat_all_metadata = fiat_list_metadata.keys()
            with allure.step("如在metada中关闭，则去除"):
                for m in range(0, len(balance_list2)-1):
                    if balance_list2[m] not in fiat_all_metadata:
                        balance_list2.remove(balance_list2[m])
            for y in balance_list2:
                cfx_list.append('{}-{}'.format(i, y))
        for z in cfx_list:
            cfx_list.remove('{}-{}'.format(z.split('-')[1], z.split('-')[0]))
        return cfx_list

    # 换汇
    @staticmethod
    def cfx_random(pair, major_ccy, buy_amount=random.uniform(10, 500.999999), url=env_url, type='interior', headers=headers, account_id=''):
        cycle = 0
        while cycle < 5:
            buy_type = pair.split('-')[0]
            sell_type = pair.split('-')[1]
            if major_ccy.lower() == buy_type.lower():
                with allure.step("major_ccy 是buy值"):
                    if buy_type == 'BTC' or buy_type == 'ETH':
                        buy_amount = random.uniform(0.02, 0.39999999)
                    elif buy_type == 'USDT':
                        buy_amount = buy_amount
                    elif buy_type == 'VND':
                        buy_amount = random.randint(250000, 300000)
                    elif buy_type == 'BRL':
                        buy_amount = random.uniform(50, 100.00)
                    else:
                        buy_amount = random.uniform(20, 500.99)
                    quote = ApiFunction.get_quote(pair)
                    buy_amount = crypto_len(number=str(buy_amount), type=buy_type)
                    if sell_type == 'VND':
                        sell_amount_temporary = crypto_len(number=str(float(buy_amount) * float(quote['quote'])),
                                                           type=sell_type)
                        if '.' in str(sell_amount_temporary):
                            sell_amount = sell_amount_temporary.split('.')[0]
                    else:
                        sell_amount = crypto_len(number=str(float(buy_amount) * float(quote['quote'])), type=sell_type)
            else:
                with allure.step("major_ccy 是sell值"):
                    if sell_type == 'BTC' or sell_type == 'ETH':
                        sell_amount = random.uniform(0.02, 0.39999999)
                    elif sell_type == 'USDT':
                        sell_amount = random.uniform(10, 500.999999)
                    elif sell_type == 'VND':
                        sell_amount = random.randint(250000, 300000)
                    elif sell_type == 'BRL':
                        sell_amount = random.uniform(50, 100.99)
                    else:
                        sell_amount = random.uniform(20, 500.99)
                    quote = ApiFunction.get_quote(pair)
                    sell_amount = crypto_len(number=str(sell_amount), type=sell_type)
                    if buy_type == 'VND':
                        buy_amount_temporary = crypto_len(number=str(float(sell_amount) / float(quote['quote'])),
                                                          type=buy_type)
                        if '.' in str(buy_amount_temporary):
                            buy_amount = buy_amount_temporary.split('.')[0]
                    else:
                        buy_amount = crypto_len(number=str(float(sell_amount) / float(quote['quote'])), type=buy_type)
            data = {
                "quote_id": quote['quote_id'],
                "quote": quote['quote'],
                "pair": pair,
                "buy_amount": str(buy_amount),
                "sell_amount": str(sell_amount),
                "major_ccy": major_ccy,
                "partner_id": '800b482d-0a88-480a-aae7-741f77a572f4',
                'user_ext_ref': '988518746672869376'
            }
            logger.info('发送换汇参数是{}'.format(data))
            if type == 'interior':
                r = session.request('POST', url='{}/txn/cfx'.format(url), data=json.dumps(data), headers=headers)
            else:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(30)
                    sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='POST',
                                                        url='/api/v1/accounts/{}/conversions'.format(
                                                            account_id),
                                                        nonce=nonce,
                                                        body=json.dumps(data))
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                r = session.request('POST', url='{}/accounts/{}/conversions'.format(url, account_id), data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                return {'data': data, 'returnJson': r.json()}
            cycle = cycle + 1
        assert False, '换汇失败，接口返回{}'.format(r.text)

    # 根据config 获得支持币种，支持bybit，infinni games
    @staticmethod
    def get_connect_support(url, headers, key=''):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            if key == 'infinni games':
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games', nonce=nonce)
            else:
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(url), headers=headers)
            support_list = []
            for i in r.json()['currencies']:
                support_list.append(i['symbol'])
        return support_list

    # 根据config 获得支持cash币种，支持bybit，infinni games
    @staticmethod
    def get_connect_support_cash(url, headers, key=''):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            if key == 'infinni games':
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games', nonce=nonce)
            else:
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(url), headers=headers)
            support_list = []
            for i in r.json()['currencies']:
                if i['type'] == 1:
                    support_list.append(i['symbol'])
        return support_list

    # 根据config 获得cfx list，支持bybit，infinni games
    @staticmethod
    def get_connect_cfx_list(url, headers, key=''):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            if key == 'infinni games':
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games', nonce=nonce)
            else:
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(url), headers=headers)
            cfx_list = []
            for i in r.json()['pairs']:
                cfx_list.append(i['pair'])
        return cfx_list

    # 根据需求或得config参数
    @staticmethod
    def get_config_info(project='bybit', type='', symbol=''):
        headers = {}
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(30)
            if project == 'infinni games':
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', key='infinni games', nonce=nonce)
                url = get_json()['infinni_games']['url']
                headers['ACCESS-KEY'] = get_json()['infinni_games']['partner_id']
            elif project == 'bybit':
                sign = ApiFunction.make_access_sign(unix_time=str(unix_time), method='GET', url='/api/v1/config', nonce=nonce)
                url = get_json()['connect'][get_json()['env']]['url']
                headers = get_json()['connect'][get_json()['env']]['bybit']['Headers']
            headers['ACCESS-SIGN'] = sign
            headers['ACCESS-TIMESTAMP'] = str(unix_time)
            headers['ACCESS-NONCE'] = nonce
        with allure.step("获取合作方的配置"):
            r = session.request('GET', url='{}/config'.format(url), headers=headers)
            if type == 'pairs':
                cfx_list = []
                for i in r.json()['pairs']:
                    cfx_list.append(i['pair'])
                return cfx_list
            elif type == 'cash':
                cash_list = []
                for i in r.json()['currencies']:
                    if i['type'] == 1:
                        cash_list.append(i['symbol'])
                return cash_list
            elif type == 'crypto':
                crypto_list = []
                for i in r.json()['currencies']:
                    if i['type'] == 2:
                        crypto_list.append(i['symbol'])
                return crypto_list
            elif type == 'credit_limit':
                credit_list = []
                credit_limit = []
                for i in r.json()['currencies']:
                    if i['config']['credit']['allow']:
                        credit_dict = i['config']['credit']
                        del(credit_dict['allow'])
                        credit_dict['symbol'] = i['symbol']
                        credit_list.append(credit_dict)
                for j in credit_list:
                    if j['symbol'] == symbol:
                        credit_limit.append([j['min'], j['max']])
                return credit_limit

            elif type == 'debit_limit':
                debit_list = []
                debit_limit = []
                for i in r.json()['currencies']:
                    if i['config']['debit']['allow']:
                        debit_dict = i['config']['debit']
                        del(debit_dict['allow'])
                        debit_dict['symbol'] = i['symbol']
                        debit_list.append(debit_dict)
                for j in debit_list:
                    if j['symbol'] == symbol:
                        debit_limit.append([j['min'], j['max']])
                return debit_limit

            elif type == 'debit_fee':
                debit_fee = []
                debit_fee_value = []
                for i in r.json()['currencies']:
                    if i['fees']['debit_fee']['is_single']:
                        debit_dict = i['fees']['debit_fee']
                        del (debit_dict['is_single'])
                        debit_dict['symbol'] = i['symbol']
                        debit_fee.append(debit_dict)
                for j in debit_fee:
                    if j['symbol'] == symbol:
                        debit_fee_value.append([j['value'], j['original_value']])
                return debit_fee_value

            elif type == 'cfx_limit':
                cfx_list = []
                cfx_limit = []
                for i in r.json()['currencies']:
                    if i['config']['conversion']['allow']:
                        cfx_dict = i['config']['conversion']
                        del(cfx_dict['allow'])
                        cfx_dict['symbol'] = i['symbol']
                        cfx_list.append(cfx_dict)
                for j in cfx_list:
                    if j['symbol'] == symbol:
                        cfx_limit.append([j['min'], j['max']])
                return cfx_limit

            elif type == 'all':
                all_list = []
                for i in r.json()['currencies']:
                    all_list.append(i['symbol'])
                return all_list

    # 获取buy crypto所有支持的币种
    @staticmethod
    def get_buy_crypto_currency(type='all'):
        r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
        payment_currencies = r.json()['payment_currencies']
        buy_crypto_currency = []
        buy_crypto_currency_random = []
        for i in range(0, len(payment_currencies)):
            buy_crypto_currency.append('USDT-{}'.format(payment_currencies[i]['code']))
        if type == 'random':
            j = random.randint(0, len(buy_crypto_currency))
            buy_crypto_currency_random.append(buy_crypto_currency[j])
            return buy_crypto_currency_random
        else:
            return buy_crypto_currency

    # 获取buy crypto指定币种的最大最小值
    @staticmethod
    def get_buy_crypto_limit(currency='USDT'):
        r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
        payment_currencies = r.json()['payment_currencies']
        buy_crypto_limit = []
        for i in range(0, len(payment_currencies)):
            if payment_currencies[i]['code'] == currency:
                buy_crypto_limit.append(payment_currencies[i]['min'])
                buy_crypto_limit.append(payment_currencies[i]['max'])
                return buy_crypto_limit

    # 获取buy crypto指定币种的手续费，买入卖出数量。
    @staticmethod
    def get_buy_crypto_list(amount, pairs='USDT-EUR', ccy='spend', country='TH'):
        with allure.step("获取汇率"):
            r = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, pairs), headers=headers)
            quote = r.json()['quote']['amount']
            quote_id = r.json()['quote']['id']
        with allure.step("打开数字货币购买画面"):
            r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers)
            for i in r.json()['payment_currencies']:
                if i['code'] == str(pairs.split('-')[1]):
                    precision = i['precision']
        with allure.step("确认major_code"):
            if ccy == 'spend':
                major_code = pairs.split('-')[1]
            else:
                major_code = pairs.split('-')[0]
        with allure.step("判断方向"):
            if ccy == 'spend':
                with allure.step("判断地区"):
                    if country in get_json()['EAList']:
                        total_spend_amount = Decimal(amount)
                        service_charge = (total_spend_amount * Decimal(0.0185)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        spend_amount = (total_spend_amount * Decimal(1 - 0.0185)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        buy_amount = (spend_amount / Decimal(quote))
                    else:
                        total_spend_amount = Decimal(amount)
                        service_charge = (total_spend_amount * Decimal(0.0375)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        spend_amount = (total_spend_amount * Decimal(1 - 0.0375))

                        buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
            else:
                with allure.step("判断地区"):
                    if country in get_json()['EAList']:
                        buy_amount = Decimal(amount)
                        spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        total_spend_amount = (spend_amount / Decimal(1 - 0.0185)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        service_charge = (total_spend_amount * Decimal(0.0185)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        if total_spend_amount != Decimal(get_precision(service_charge, precision, True)) + spend_amount:
                            total_spend_amount = Decimal(get_precision(service_charge, precision, True)) + spend_amount
                    else:
                        buy_amount = Decimal(amount)
                        spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        total_spend_amount = (spend_amount / Decimal(1 - 0.0375)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        service_charge = (total_spend_amount * Decimal(0.0375)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        if total_spend_amount != Decimal(get_precision(service_charge, precision, True)) + spend_amount:
                            total_spend_amount = Decimal(get_precision(service_charge, precision, True)) + spend_amount
            return {'major_code': major_code, 'pairs': pairs, 'quote_id': quote_id, 'quote': quote, 'total_spend_amount': get_precision(total_spend_amount, precision), 'spend_amount': get_precision(spend_amount, precision), 'service_charge': get_precision(service_charge, precision, True), 'buy_amount': get_precision(buy_amount, 6)}



