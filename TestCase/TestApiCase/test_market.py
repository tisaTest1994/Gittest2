from Function.api_function import *
from Function.operate_sql import *


# market相关cases
class TestMarketApi:

    # 初始化
    def setup_method(self):
        AccountFunction.add_headers()

    @allure.testcase('test_market_001 获得价格曲线')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_market_001(self):
        for i in ['BTCEUR', 'BTCUSD', 'ETHEUR', 'ETHUSD', 'USDEUR']:
            for y in ['10', '60', 'D', 'W', 'M']:
                params = {
                    "pair": i,
                    "interval": y,
                    "from_time": "0",
                    "to_time": str(datetime.now().timestamp()).split('.')[0]
                }
                r = session.request('GET', url='{}/marketstat/public/quote-chart'.format(env_url), params=params,
                                     headers=headers)
                logger.info('货币{}的{}时间的曲线{}'.format(i, y, r.text))
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert 'items' in r.text, "获得价格曲线错误，返回值是{}".format(r.text)

    @allure.testcase('test_market_002 获得行情信息')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_market_002(self):
        with allure.step("获得行情信息"):
            List = ["BTC", "ETH", "USDT"]
            for i in List:
                params = {
                    "code": i
                }
                r = session.request('GET', url='{}/marketstat/public/ticker'.format(env_url), params=params,
                                 headers=headers)
                with allure.step("状态码和返回值"):
                    logger.info('状态码是{}'.format(str(r.status_code)))
                    logger.info('返回值是{}'.format(str(r.text)))
                with allure.step("校验状态码"):
                    assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
                with allure.step("校验返回值"):
                    assert 'price_24h_pcnt' in r.text, "获得价格曲线错误，返回值是{}".format(r.text)

    @allure.testcase('test_market_003 给测试环境注资')
    @pytest.mark.multiprocess
    def test_market_003(self):
        with allure.step("给测试环境注资"):
            r = session.request('GET', url='https://faucet.ropsten.be/donate/0xaE346B37A0A7ffd5F224Cc2fC2c4C0E1bC541D67')
            print(r.json())

    @allure.testcase('test_market_004 首页获得数字货币报价')
    @pytest.mark.multiprocess
    @pytest.mark.pro
    def test_market_004(self):
        with allure.step("首页获得数字货币报价"):
            params = {
                'codes': 'BTC,ETH'
            }
            r = requests.request('GET', url='{}/marketstat/public/tickers'.format(env_url), params=params, headers=headers)
            with allure.step("状态码和返回值"):
                logger.info('状态码是{}'.format(str(r.status_code)))
                logger.info('返回值是{}'.format(str(r.text)))
            with allure.step("校验状态码"):
                assert r.status_code == 200, "http状态码不对，目前状态码是{}".format(r.status_code)
            with allure.step("校验返回值"):
                assert 'abs_amount' in r.text, "首页获得数字货币报价失败，返回值是{}".format(r.text)