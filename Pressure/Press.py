from run import *
from locust import HttpUser, task, between
from Function.ApiFunction import *


class MyUser(HttpUser):
    wait_time = between(0.5, 3)

    @task(1)
    def login(self):
        data = {
            "username": 'yilei3@cabital.com',
            "password": 'Zcdsw123'
        }
        r = self.client.post(url="/account/user/signIn", headers=headers, data=json.dumps(data))
        print(r.text)
        if r.status_code == 200:
            print("success")
        else:
            print("fails")

    @task(6)
    def core(self):
        accessToken = AccountFunction.get_account_token(account=email['email'], password=email['password'])[
            'accessToken']
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        r = self.client.get(url="/core/account", headers=headers)
        print(r.text)
        if r.status_code == 200:
            print("success")
        else:
            print("fails")

    @task(2)
    def index(self):
        params = {
            "pair": 'BTCEUR',
            "interval": '60',
            "from_time": "0",
            "to_time": ""
        }
        r = self.client.get(url="/marketstat/public/quote-chart", headers=headers, params=params)
        print(r.text)
        if r.status_code == 200:
            print("success")
        else:
            print("fails")


if __name__ == "__main__":
    import os

    os.system("locust -f press.py --host=https://testapi.latibac.com/api/v1")
