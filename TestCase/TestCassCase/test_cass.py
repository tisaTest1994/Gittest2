from Function.web_function import *
from Function.api_function import *


# saving相关cases
class TestMonitorApi:

    # 初始化
    def setup_method(self):
        webFunction.launch_web(get_json()['caas'][get_json()['env']]['url'])
        pass

    @allure.testcase('test_cass_001 ')
    def test_cass_001(self):
        # 当前脚本工作的目录路径
        print(os.getcwd())
        # os.path.abspath()获得绝对路径
        print(os.path.abspath(os.path.dirname(__file__)))