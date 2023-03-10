from run import *
from Function.operate_sql import *
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import MD5, SHA1, SHA256
from Crypto.Signature import PKCS1_v1_5 as Signature_PKC
import base64
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
            if type == 'USDC' or type == 'USDs':
                type = 'USD'
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

    # 获取当前某个币的当前资产价值，用USD结算
    @staticmethod
    def get_crypto_abs_amount(type='BTC'):
        r = session.request('GET', url='{}/core/account'.format(env_url), headers=headers)
        for i in r.json()['wallets']:
            if i['code'] == type:
                return i['abs_amount']

    # 查询交易状态
    @staticmethod
    def get_transaction_status(transaction_id, type):
        params = {
            'txn_sub_type': type
        }
        r = session.request('GET', url='{}/txn/{}'.format(env_url, transaction_id), params=params, headers=headers)
        return r.json()['transaction']['status']

    # webhook解码
    @staticmethod
    def webhook_verify(signature, unix_time, method, url, body='', nonce=''):
        """
        RSA公钥验签
        :param data: 明文数据,签名之前的数据
        :param signature: 接收到的sign签名
        :return: 验签结果,布尔值
        """
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
        # 接收到的sign签名 base64解码
        sign_data = base64.b64decode(signature.encode("utf-8"))
        # 加载公钥
        path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/my_rsa_public.pem'
        public_key = RSA.importKey(open(path).read())
        # 根据SHA256算法处理签名之前内容data
        sha_data = SHA256.new(str(data).encode("utf-8"))
        # 验证签名
        signer = Signature_PKC.new(public_key)
        return signer.verify(sha_data, sign_data)

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
            path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/my_private_rsa_key.bin'
            private_key = RSA.import_key(open(path).read())
            signer = PKCS1_v1_5.new(private_key,)
            hash_obj = SHA256.new(data.encode('utf-8'))
            sign = base64.b64encode(signer.sign(hash_obj))
            sign = str(sign, 'utf-8')
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

    # partner and cabital pay 验签
    @staticmethod
    def make_signature(unix_time, method, url, connect_type, body='', nonce=''):
        if connect_type == 'cabital pay':
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
            path = os.path.split(os.path.realpath(__file__))[0] + '/../Resource/my_private_rsa_key.bin'
            private_key = RSA.import_key(open(path).read())
            signer = PKCS1_v1_5.new(private_key,)
            hash_obj = SHA256.new(data.encode('utf-8'))
            sign = base64.b64encode(signer.sign(hash_obj))
            sign = str(sign, 'utf-8')
        else:
            if get_json(file='partner_info.json')[get_json()['env']][connect_type] != '':
                key = get_json(file='partner_info.json')[get_json()['env']][connect_type]['Secret_Key']
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
    def get_link_sign(url, partner):
        key = get_json(file='partner_info.json')[get_json()['env']][partner]['Secret_Key']
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

    # 收取验证码（先发再收）
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
        sleep(3)
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
            if '{}-{}'.format(z.split('-')[1], z.split('-')[0]) in cfx_list:
                cfx_list.remove('{}-{}'.format(z.split('-')[1], z.split('-')[0]))
        return cfx_list

    # 换汇
    @staticmethod
    def cfx_random(pair, major_ccy, buy_amount=random.uniform(10, 100.999999), url=env_url, headers=headers, account_id='', partner=''):
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
                    elif buy_type == 'USDC':
                        buy_amount = random.uniform(40, 100.999999)
                    else:
                        buy_amount = random.uniform(20, 100.99)
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
                    elif sell_type == 'USDC':
                        sell_amount = random.uniform(40, 100.999999)
                    else:
                        sell_amount = random.uniform(20, 100.99)
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
                "major_ccy": major_ccy
            }
            logger.info('发送换汇参数是{}'.format(data))
            if partner == '':
                r = session.request('POST', url='{}/txn/cfx'.format(url), data=json.dumps(data), headers=headers)
            else:
                with allure.step("验签"):
                    unix_time = int(time.time())
                    nonce = generate_string(20) + str(time.time()).split('.')[0]
                    sign = ApiFunction.make_signature(unix_time=str(unix_time), method='POST',
                                                      url='/api/v1/accounts/{}/conversions'.format(account_id),
                                                      connect_type=partner, nonce=nonce, body=json.dumps(data))
                    headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                        'Partner_ID']
                    headers['ACCESS-SIGN'] = sign
                    headers['ACCESS-TIMESTAMP'] = str(unix_time)
                    headers['ACCESS-NONCE'] = nonce
                r = session.request('POST', url='{}/accounts/{}/conversions'.format(url, account_id), data=json.dumps(data), headers=headers)
            if r.status_code == 200 or r.status_code == 201:
                return {'data': data, 'returnJson': r.json()}
            cycle = cycle + 1
        assert False, '换汇失败，接口返回{}'.format(r.text)

    # 获取buy crypto所有支持的币种
    @staticmethod
    def get_buy_crypto_currency(partner, type='all'):
        params = {
            'partner_id': get_json(file='partner_info.json')[get_json()['env']][partner]['Partner_ID']
        }
        r = session.request('GET', url='{}/acquiring/buy/prepare'.format(env_url), headers=headers, params=params)
        if '101034' in r.text:
            return []
        else:
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
            logger.info('trace id是{}'.format(str(r.headers['Traceparent'])))
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
                if 'CLP' in pairs or 'VND' in pairs or 'KRW' in pairs or 'JPY' in pairs:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            total_spend_amount = Decimal(amount)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0'), ROUND_CEILING)
                            spend_amount = total_spend_amount - service_charge
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        else:
                            total_spend_amount = Decimal(amount)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0'), ROUND_CEILING)
                            spend_amount = total_spend_amount - service_charge
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                else:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            total_spend_amount = Decimal(amount)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0.00'), ROUND_CEILING)
                            spend_amount = total_spend_amount - service_charge
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
                        else:
                            total_spend_amount = Decimal(amount)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0.00'), ROUND_CEILING)
                            spend_amount = total_spend_amount - service_charge
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'), ROUND_FLOOR)
            else:
                if 'CLP' in pairs or 'VND' in pairs or 'KRW' in pairs or 'JPY' in pairs:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0'),
                                                                                         ROUND_FLOOR)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.019)).quantize(Decimal('0'),
                                                                                              ROUND_FLOOR)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0'),
                                                                                            ROUND_CEILING)
                            if total_spend_amount != Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount:
                                total_spend_amount = Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount
                        else:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                         ROUND_FLOOR)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.038)).quantize(Decimal('0.000'),
                                                                                              ROUND_FLOOR)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0.000'),
                                                                                            ROUND_CEILING)
                            if total_spend_amount != Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount:
                                total_spend_amount = Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount
                else:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                         ROUND_FLOOR)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.019)).quantize(Decimal('0.00'),
                                                                                              ROUND_FLOOR)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0.00'),
                                                                                            ROUND_CEILING)
                            if total_spend_amount != Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount:
                                total_spend_amount = Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount
                        else:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                         ROUND_FLOOR)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.038)).quantize(Decimal('0.00'),
                                                                                              ROUND_FLOOR)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0.00'),
                                                                                            ROUND_CEILING)
                            if total_spend_amount != Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount:
                                total_spend_amount = Decimal(
                                    get_precision(service_charge, precision, True)) + spend_amount
            return {'major_code': major_code, 'pairs': pairs, 'quote_id': quote_id, 'quote': quote, 'total_spend_amount': get_precision(total_spend_amount, precision), 'spend_amount': get_precision(spend_amount, precision), 'service_charge': get_precision(service_charge, precision, True), 'buy_amount': get_precision(buy_amount, 6)}

    # 获取buy crypto指定币种的手续费，买入卖出数量。
    @staticmethod
    def get_buy_crypto_transfer_list(amount, t_fee, pairs='USDT-EUR', ccy='spend', country='TH'):
        with allure.step("获取汇率"):
            r = session.request('GET', url='{}/acquiring/buy/quotes/{}'.format(env_url, pairs), headers=headers)
            quote = r.json()['quote']['amount']
            quote_id = r.json()['quote']['id']
            t_fee = Decimal(t_fee)
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
                if 'CLP' in pairs or 'VND' in pairs or 'KRW' in pairs or 'JPY' in pairs:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            total_spend_amount = Decimal(amount)
                            processing_fee = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0'),
                                                                                             ROUND_CEILING)
                            spend_amount = total_spend_amount - processing_fee
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'),
                                                                                  ROUND_FLOOR) - t_fee
                            service_charge = (
                                        total_spend_amount - (buy_amount * Decimal(quote)).quantize(Decimal('0'),
                                                                                                    ROUND_CEILING) - (
                                                    Decimal(t_fee) * Decimal(quote).quantize(Decimal('0'),
                                                                                             ROUND_CEILING))).quantize(
                                Decimal('0'), ROUND_FLOOR)
                            spend_amount = total_spend_amount - service_charge
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0'), ROUND_CEILING)
                        else:
                            total_spend_amount = Decimal(amount)
                            processing_fee = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0'),
                                                                                             ROUND_CEILING)
                            spend_amount = total_spend_amount - processing_fee
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'),
                                                                                  ROUND_FLOOR) - t_fee
                            service_charge = (
                                        total_spend_amount - (buy_amount * Decimal(quote)).quantize(Decimal('0'),
                                                                                                    ROUND_CEILING) - (
                                                    Decimal(t_fee) * Decimal(quote).quantize(Decimal('0'),
                                                                                             ROUND_CEILING))).quantize(
                                Decimal('0'), ROUND_FLOOR)
                            spend_amount = total_spend_amount - service_charge
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0'), ROUND_CEILING)
                else:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            total_spend_amount = Decimal(amount)
                            processing_fee = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING)
                            spend_amount = total_spend_amount - processing_fee
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'),
                                                                                  ROUND_FLOOR) - t_fee
                            service_charge = (
                                        total_spend_amount - (buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                                    ROUND_CEILING) - (
                                                    Decimal(t_fee) * Decimal(quote).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING))).quantize(
                                Decimal('0.00'), ROUND_FLOOR)
                            spend_amount = total_spend_amount - service_charge
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0.00'), ROUND_CEILING)
                        else:
                            total_spend_amount = Decimal(amount)
                            processing_fee = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING)
                            spend_amount = total_spend_amount - processing_fee
                            buy_amount = (spend_amount / Decimal(quote)).quantize(Decimal('0.000000'),
                                                                                  ROUND_FLOOR) - t_fee
                            service_charge = (
                                        total_spend_amount - (buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                                    ROUND_CEILING) - (
                                                    Decimal(t_fee) * Decimal(quote).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING))).quantize(
                                Decimal('0.00'), ROUND_FLOOR)
                            spend_amount = total_spend_amount - service_charge
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0.00'), ROUND_CEILING)
            else:
                if 'CLP' in pairs or 'VND' in pairs or 'KRW' in pairs or 'JPY' in pairs:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0'),
                                                                                          ROUND_CEILING) + Decimal(t_fee * Decimal(quote)).quantize(Decimal('0'),
                                                                          ROUND_CEILING)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.019)).quantize(Decimal('0'),
                                                                                               ROUND_CEILING)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0'),
                                                                                             ROUND_CEILING)
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0'), ROUND_CEILING)
                        else:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0'),
                                                                                          ROUND_CEILING) + Decimal(t_fee * Decimal(quote)).quantize(Decimal('0'),
                                                                          ROUND_CEILING)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.038)).quantize(Decimal('0.'),
                                                                                               ROUND_CEILING)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0'),
                                                                                             ROUND_CEILING)
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0'), ROUND_CEILING)
                else:
                    with allure.step("判断地区"):
                        if country in get_json()['EAList']:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                          ROUND_CEILING) + Decimal(t_fee * Decimal(quote)).quantize(Decimal('0.00'),
                                                                          ROUND_CEILING)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.019)).quantize(Decimal('0.00'),
                                                                                               ROUND_CEILING)
                            service_charge = (total_spend_amount * Decimal(0.019)).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING)
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0.00'), ROUND_CEILING)
                        else:
                            buy_amount = Decimal(amount)
                            spend_amount = Decimal(buy_amount * Decimal(quote)).quantize(Decimal('0.00'),
                                                                                          ROUND_CEILING) + Decimal(t_fee * Decimal(quote)).quantize(Decimal('0.00'),
                                                                          ROUND_CEILING)
                            total_spend_amount = (spend_amount / Decimal(1 - 0.038)).quantize(Decimal('0.00'),
                                                                                               ROUND_CEILING)
                            service_charge = (total_spend_amount * Decimal(0.038)).quantize(Decimal('0.00'),
                                                                                             ROUND_CEILING)
                            transfer_fee = (t_fee * Decimal(quote)).quantize(Decimal('0.00'), ROUND_CEILING)
            return {'major_code': major_code, 'pairs': pairs, 'quote_id': quote_id, 'quote': quote, 'total_spend_amount': get_precision(total_spend_amount, precision), 'spend_amount': get_precision(spend_amount, precision), 'service_charge': get_precision(service_charge, precision), 'buy_amount': get_precision(buy_amount, 6), 'transfer_fee': str(transfer_fee)}

    # 获取用户可用单币种balance
    @staticmethod
    def connect_get_balance(partner, account_vid, currency):
        with allure.step("验签"):
            unix_time = int(time.time())
            nonce = generate_string(20) + str(time.time()).split('.')[0]
            sign = ApiFunction.make_signature(unix_time=str(unix_time), method='GET',
                                              url='/api/v1/accounts/{}/balances/{}'.format(account_vid, currency),
                                              connect_type=partner, nonce=nonce)
            connect_headers['ACCESS-KEY'] = get_json(file='partner_info.json')[get_json()['env']][partner][
                'Partner_ID']
            connect_headers['ACCESS-SIGN'] = sign
            connect_headers['ACCESS-TIMESTAMP'] = str(unix_time)
            connect_headers['ACCESS-NONCE'] = nonce
        with allure.step("账户可用余额列表"):
            r = session.request('GET', url='{}/accounts/{}/balances/{}'.format(connect_url, account_vid, currency),
                                headers=connect_headers)
        return r.json()['balance']
