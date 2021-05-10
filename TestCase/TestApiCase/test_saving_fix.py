from Function.api_function import *
from run import *
from Function.log import *
from decimal import *
import allure


# saving相关cases
class TestSavingFixApi:

    @allure.testcase('test_saving_fix_001 获取定期产品列表')
    def test_saving_fix_001(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                for i in r.json():
                    assert i['code'] == 'BTC' or i['code'] == 'ETH' or i['code'] == 'USDT', "获取定期产品列表失败，返回值是{}".format(r.text)

    @allure.testcase('test_saving_fix_002 获取定期产品详情')
    def test_saving_fix_002(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            for y in i['products']:
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取定期产品详情"):
                    r = session.request('GET', url='{}/earn/fix/products/{}'.format(env_url, y['product_id']), headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        assert 'Earn Bit Fixed' in r.text, '获取定期产品详情失败,返回值是{}'.format(r.json())

    @allure.testcase('test_saving_fix_003 获取定期产品利息列表')
    def test_saving_fix_003(self):
        with allure.step("获取定期产品列表"):
            r = session.request('GET', url='{}/earn/fix/products'.format(env_url), headers=headers)
        for i in r.json():
            for y in i['products']:
                logger.info('定期产品product_id是{}'.format(y['product_id']))
                with allure.step("获取定期产品详情"):
                    params = {
                        'cursor': "0",
                        'size': 99999
                    }
                    r = session.request('GET', url='{}/earn/products/{}/interests'.format(env_url, y['product_id']), params=params, headers=headers)
                    with allure.step("状态码和返回值"):
                        logger.info('状态码是{}'.format(str(r.status_code)))
                        logger.info('返回值是{}'.format(str(r.text)))
                    with allure.step("校验状态码"):
                        assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
                    with allure.step("校验返回值"):
                        for z in r.json()['items']:
                            assert z['apy'] is not None, "获取定期产品利息列表失败，返回值是{}".format(r.text)
                            assert z['date'] is not None, "获取定期产品利息列表失败，返回值是{}".format(r.text)
