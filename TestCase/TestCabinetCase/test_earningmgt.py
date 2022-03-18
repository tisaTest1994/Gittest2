import datetime

from Function.api_function import *
from Function.operate_sql import *


# operate相关cases
class TestEarningMgtApi:

    # 初始化class
    def setup_method(self):
        headers['Authorization'] = "Bearer " + ApiFunction.get_account_token(
            account=get_json()['operate_admin_account']['email'],
            password=get_json()['operate_admin_account']['password'], type='operate')

    @allure.title('test_earning_mgt_001')
    @allure.description('修改USDC toB 利率')
    def test_earning_mgt_001(self):
        with allure.step("修改USDC toB 利率"):
            USDC_Flexible_Savings_2B = "eaa55390-745e-11ec-ae7e-0a3898443cb8"
            USDC_Fixed_Savings_1_Day_2B = "eaa5595d-745e-11ec-ae7e-0a3898443cb8"
            date_list = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
            data = {
                'interests': [{'product_id': USDC_Flexible_Savings_2B,
                               'apy': '0.031',
                               'date': date_list,
                               'created_by': 'richard auto test'
                               },
                              {'product_id': USDC_Fixed_Savings_1_Day_2B,
                               'apy': '0.041',
                               'date': date_list,
                               'created_by': 'richard auto test'
                               }
                              ]
            }
            r = session.request('PUT', url='{}/operatorapi/earningmgt/interests'.format(operateUrl),
                                data=json.dumps(data),
                                headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert {} == r.json(), "用户修改邮箱错误，返回值是{}".format(r.text)
        with allure.step("查询USDC toB 利率"):
            params = {
                'product_id': USDC_Flexible_Savings_2B,
                'page_no': '1',
                'page_size': '10'
            }
            r = session.request('GET', url='{}/operatorapi/earningmgt/interests'.format(operateUrl), params=params, headers=headers)
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("校验返回值"):
            assert r.json()['record_count'] is not None, "查询USDC toB 利率错误，返回值是{}".format(r.text)
