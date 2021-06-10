from locust import HttpUser, task, between
from Function.api_function import *
import os


class MyUser(HttpUser):
    account_list = ['yilei1@cabital.com', 'yilei2@cabital.com', 'yilei3@cabital.com', 'yilei4@cabital.com',
                    'yilei5@cabital.com', 'yilei6@cabital.com', 'yilei7@cabital.com', 'yilei8@cabital.com',
                    'yilei9@cabital.com', 'yilei10@cabital.com', 'yilei11@cabital.com', 'yilei12@cabital.com',
                    'yilei13@cabital.com', 'yilei14@cabital.com']
    min_wait = 100
    max_wait = 6000

    @task(6)
    def core(self):
        accessToken = AccountFunction.get_account_token(account=random.choice(MyUser.account_list), password='Zcdsw123')
        headers['Authorization'] = "Bearer " + accessToken
        headers['X-Currency'] = 'USD'
        r = self.client.get(url="/core/account", headers=headers)
        print(r.text)
        if r.status_code == 200:
            print("success")
        else:
            print("fails")


if __name__ == "__main__":
    os.system("locust -f press.py --host={}".format(get_json()['test']))
