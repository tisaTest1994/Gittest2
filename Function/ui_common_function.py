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


# 数量加入,
def add_comma_number(number):
    if '.' in str(number):
        number_int = str(number).split('.')[0]
        number_radix = str(number).split('.')[1]
    else:
        number_int = str(number)
        number_radix = ''
    count = 0
    sumstr = ''
    for one_str in number_int[::-1]:  # 注意循环是倒着输出的
        count += 1  # 计数
        if count % 3 == 0 and count != len(number_int):  # 如果count等于3或3的倍数并且不等于总长度
            one_str = ',' + one_str  # 当前循环的字符串前面加逗号
            sumstr = one_str + sumstr  # 拼接当前字符串
        else:
            sumstr = one_str + sumstr  # 正常拼接字符串
    if number_radix != '':
        sumstr = sumstr + '.' + number_radix
    return sumstr
