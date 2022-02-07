import logging
import pytest
import allure
from airtest.core.api import *
from Function.api_common_function import *

logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)
auto_setup(__file__)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    获取每个用例状态的钩子函数
    :param item:
    :param call:
    :return:
    """
    # 获取钩子方法的调用结果
    outcome = yield
    rep = outcome.get_result()
    # 仅仅获取用例call 执行结果是失败的情况, 不包含 setup/teardown
    if rep.when == "call" and rep.failed:
        with allure.step('添加失败截图'):
            path = os.path.split(os.path.realpath(__file__))[0] + '/../../Screenshot/App/{}.png'.format(get_now_time())
            snapshot(path)
            with open(path, mode='rb') as f:
                file = f.read()
                allure.attach(file, "失败截图", allure.attachment_type.PNG)


