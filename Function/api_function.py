from run import *
from Function.operate_sql import *


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
            return "登录获得token错误，返回值是{}".format(r.text)
        elif 'accessToken' not in r.text:
            return "登录获得token错误，返回值是{}".format(r.text)
        else:
            return r.json()['accessToken']

    # 加headers，只能默认账户,使用usd
    @staticmethod
    def add_headers(currency='USD'):
        headers['User-Agent'] = 'iOS;1.0.0;1;14.4;14.4;iPhone;iPhone 12 Pro Max;'
        headers['X-Browser-Key'] = 'yilei_test'
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token()
        headers['X-Currency'] = currency

    # 注册
    @staticmethod
    def sign_up(account=get_json()['email']['email'], password=get_json()['email']['password']):
        data = {
            "emailAddress": account,
            "password": password,
            "verificationCode": "666666",
            "citizenCountryCode": random.choice(get_json()['citizenCountryCodeList'])
        }
        r = session.request('POST', url='{}/account/user/signUp'.format(env_url), data=json.dumps(data), headers=headers)
        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "注册用户错误，返回值是{}".format(r.text)

    # 提现ETH获取交易id
    @staticmethod
    def get_payout_transaction_id(amount='0.03', address='0x428DA40C585514022b2eB537950d5AB5C7365a07', code_type='ETH'):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=get_json()['email']['payout_email'])
        code = ApiFunction.get_verification_code(type='MFA_EMAIL', account=get_json()['email']['payout_email'])
        secretKey = get_json()['secretKey']
        totp = pyotp.TOTP(secretKey)
        mfaVerificationCode = totp.now()
        headers['X-Mfa-Otp'] = str(mfaVerificationCode)
        headers['X-Mfa-Email'] = '{}###{}'.format(get_json()['email']['payout_email'], code)
        logger.info('交易的订单headers是{}'.format(headers))
        data = {
            "amount": amount,
            "code": code_type,
            "address": address,
            "method": "ERC20"
        }
        r = session.request('POST', url='{}/pay/withdraw/transactions'.format(env_url), data=json.dumps(data),
                            headers=headers)
        logger.info('获取的交易订单json是{}'.format(r.text))
        ApiFunction.add_headers()
        return r.json()['transaction_id']

    # 获取下次清算金额
    @staticmethod
    def get_interest(productId):
        r1 = session.request('GET', url='{}/earn/products/{}/next_yield'.format(env_url, productId), headers=headers)
        return r1.json()['next_yield']

    # 获取当前换汇报价
    @staticmethod
    def get_quote(pair):
        cryptos = pair.split('-')
        r = session.request('GET', url='{}/core/quotes/{}'.format(env_url, "{}-{}".format(cryptos[0], cryptos[1])), headers=headers)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(r.json()['valid_until'])))
        logger.info('获得报价的服务器时间是{}'.format(strTime))
        return r.json()

    # 获取钱包指定币种某个交易状态的数量
    @staticmethod
    def get_crypto_number(type='BTC', balance_type='BALANCE_TYPE_AVAILABLE', wallet_type='BALANCE'):
        r = session.request('GET', url='{}/core/account/wallets'.format(env_url), headers=headers, timeout=10)
        for i in r.json():
            if i['code'] == type and i['wallet_type'] == wallet_type:
                for y in i['balances']:
                    if y['type'] == balance_type:
                        balance_type_available_amount = y['amount']
        return balance_type_available_amount

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
                    print(y)
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
    def get_cfx_info(day_time='2021-05-26'):
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
    def make_access_sign(unix_time, method, url, body='', key=get_json()['kyc'][get_json()['env']]['kycSecretKey']):
        if body == '':
            data = '{}{}{}'.format(unix_time, method, url)
        else:
            data = '{}{}{}{}'.format(unix_time, method, url, body)
        key = key.encode('utf-8')
        message = data.encode('utf-8')
        sign = base64.b64encode(hmac.new(key, message, digestmod=sha256).digest())
        sign = str(sign, 'utf-8')
        return sign

    # 获得webhook
    @staticmethod
    def get_webhook():
        conn = http.client.HTTPSConnection('api.pipedream.com')
        webhook = get_json()['kyc'][get_json()['env']]['webhook']
        conn.request("GET", '/v1/sources/{}/events'.format(webhook), '', {'Authorization': 'Bearer {}'.format(get_json()['kyc'][get_json()['env']]['api_key'])})
        res = conn.getresponse()
        data = res.read()
        return data.decode("utf-8")

    # 删除webhook
    @staticmethod
    def delete_old_webhook():
        conn = http.client.HTTPSConnection('api.pipedream.com')
        webhook = get_json()['kyc'][get_json()['env']]['webhook']
        conn.request("DELETE", '/v1/sources/{}/events'.format(webhook), '', {'Authorization': 'Bearer {}'.format(get_json()['kyc'][get_json()['env']]['api_key'])})
        sleep(1)

    # 验证webhook需要的信息
    @staticmethod
    def check_webhook_info(path, caseSystemId, action='', suggestion='', decision=''):
        sleep_time = 0
        while sleep_time < 500:
            webhook_info = ApiFunction.get_webhook()
            for y in json.loads(webhook_info)['data']:
                if y['e']['path'] == path:
                    if 'operator' in path and y['e']['body']['message']['action'] == action and y['e']['body']['message']['caseSystemId'] == caseSystemId:
                        logger.info('找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, caseSystemId:{}, suggestion:{}, decision:{}'.format(path, caseSystemId, action, suggestion, decision))
                        return True
                    elif 'case' in path and y['e']['body']['caseSystemId'] == caseSystemId:
                        webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'], url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                        logger.info(
                            '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, caseSystemId:{}, suggestion:{}, decision:{}'.format(
                                path, caseSystemId, action, suggestion, decision))
                        return True
                    elif 'case/reviewed' in path and y['e']['body']['caseSystemId'] == caseSystemId and y['e']['body']['suggestion'] == suggestion:
                        webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'], url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                        logger.info(
                            '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, caseSystemId:{}, suggestion:{}, decision:{}'.format(
                                path, caseSystemId, action, suggestion, decision))
                        return True
                    elif 'case/completed' in path and y['e']['body']['caseSystemId'] == caseSystemId and y['e']['body']['decision'] == decision:
                        webhook_sign = ApiFunction.make_access_sign(unix_time=y['e']['headers']['access-timestamp'], method=y['e']['method'], url=y['e']['path'], body=y['e']['bodyRaw'])
                        assert webhook_sign == y['e']['headers']['access-sign'], "webhook验签错误，返回值是{}".format(y['e'])
                        logger.info(
                            '找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, caseSystemId:{}, suggestion:{}, decision:{}'.format(
                                path, caseSystemId, action, suggestion, decision))
                        return True
            sleep(10)
            sleep_time = sleep_time + 10
        assert False, '未找到相对应webhookwebhook的信息path:{}，caseSystemId:{}, caseSystemId:{}, suggestion:{}, decision:{}'.format(path, caseSystemId, action, suggestion, decision)

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
            amount = '20'
            interest_amount = str(((Decimal(amount) * (Decimal(product_list['apy']) / 100) / Decimal(365)).quantize(Decimal('0.000000'), ROUND_FLOOR)) * Decimal(product_list['tenor']))
        else:
            amount = "0.01327"
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

    # 收取验证码
    @staticmethod
    def get_verification_code(type, account):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(account=account)
        data = {
            "email": account,
            "type": type
        }
        r = session.request('POST', url='{}/account/verify-code/email'.format(env_url), data=json.dumps(data), headers=headers)
        logger.info('状态码是{}'.format(str(r.status_code)))
        logger.info('返回值是{}'.format(str(r.text)))
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert r.json() == {}, "收取验证码失败，返回值是{}".format(r.text)
        sleep_time = 0
        while sleep_time < 60:
            email_info = get_email()
            if type == 'REGISTRY':
                if '[Cabital] Verify Your Email' in email_info['title']:
                    break
                    sleep_time == 81
            elif type == 'FORGET_PASSWORD':
                if 'Reset Password Request' in email_info['title']:
                    break
                    sleep_time == 81
            elif type == 'ENABLE_MFA':
                if 'Enable Google Authenticator' in email_info['title']:
                    break
                    sleep_time == 81
            elif type == 'DISABLE_MFA':
                if 'Disable Google Authenticator' in email_info['title']:
                    break
                    sleep_time == 81
            elif type == 'MFA_EMAIL':
                sleep(20)
                if 'Withdrawal Request' in email_info['title']:
                    break
                    sleep_time == 81
            sleep_time = sleep_time + 5
            sleep(5)
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
    def cfx(pair):
        sql = "select books from split_setting where pair = '{}';".format(pair)
        books = sqlFunction().connect_mysql('hedging', sql=sql, type=1)
        a = {}
        books = json.dumps(books['books'])
        print(type(books))


