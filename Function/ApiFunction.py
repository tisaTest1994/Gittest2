from run import *
from time import sleep
import requests


class AccountFunction:

    @staticmethod
    def get_account_token(account, password):
        data = {
            "username": account,
            "password": password
        }
        r = requests.request('POST', url='{}/account/user/signIn'.format(env_url), data=json.dumps(data),
                             headers=headers)
        assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        assert 'accessToken' in r.text, "成功注册用户错误，返回值是{}".format(r.json())
        return r.json()
