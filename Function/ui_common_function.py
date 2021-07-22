from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from run import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# 点击某个text
def click(text):
    if text in get_json(file='multiple_languages.json').keys():
        text_string = get_json(file='multiple_languages.json')[text]
    else:
        text_string = text
    poco(text_string).wait_for_appearance(timeout=20)
    poco(text_string).click()


# 查询页面元素存在
def check(text, type=2, wait_time_max=20):
    # type 为1 返回结果(true, false)，type为2直接断言判断
    if text in get_json(file='multiple_languages.json').keys():
        text_string = get_json(file='multiple_languages.json')[text]
    else:
        text_string = text
    if type == 1:
        wait_time = 0
        while wait_time < wait_time_max:
            wait_time = wait_time + 1
            sleep(1)
            if poco(text_string).exists() is True:
                wait_time = 21
        return poco(text_string).exists()
    elif type == 'textMatches':
        assert poco(textMatches=text_string).exists() is True, "页面元素{}不存在,翻译码是{}".format(text_string, text)
    elif type == 'nameMatches':
        assert poco(nameMatches=text_string).exists() is True, "页面元素{}不存在,翻译码是{}".format(text_string, text)
    else:
        poco(text_string).wait_for_appearance(timeout=20)
        assert poco(text_string).exists() is True, "页面元素{}不存在,翻译码是{}".format(text_string, text)


