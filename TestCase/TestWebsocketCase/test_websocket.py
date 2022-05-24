import json

from Function.api_function import *
from Function.operate_sql import *
from Function.api_websocket import *


@allure.feature("websocket 相关 testcases")
class TestCoreApi:

    # 初始化class
    def setup_method(self):
        ApiFunction.add_headers()

    @allure.title('test_websocket_001')
    @allure.description('通过websocket订阅')
    def test_websocket_001(self):
        for i in ApiFunction.get_cfx_list():
            pair = i.split('-')
            asyncio.get_event_loop().run_until_complete(main_logic(params=["cfx_quote@{}{}".format(pair[0], pair[1])]))
            sleep(10)
