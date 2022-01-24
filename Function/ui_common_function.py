from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from run import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


def operate_element_app(page_name, element_string, type='click', wait_time_max=10, input_string=''):
    if page_name in get_json(file='app_tree.json').keys():
        if element_string in get_json(file='app_tree.json')[page_name].keys():
            translation_code = get_json(file='app_tree.json')[page_name][element_string]
            text_string = get_json(file='multiple_languages_app.json')[translation_code]
            if type == 'click':
                poco(text_string).click()
                logger.info('点击{}'.format(text_string))
            elif type == 'check':
                wait_time = 0
                while wait_time < wait_time_max:
                    wait_time = wait_time + 1
                    sleep(1)
                    if poco(text_string).exists() is True:
                        wait_time = wait_time_max + 1
                logger.info('检查{}元素，是否{}在当前页面'.format(text_string, poco(text_string).exists()))
                return poco(text_string).exists()
            elif type == 'input':
                poco(text_string).set_text(input_string)
                logger.info('点击{},输入{}'.format(text_string, input_string))
    else:
        assert False, "page name {}在app_tree中不存在".format(page_name)


# 查询页面元素存在
def check(page_name, element_string, wait_time_max=20, is_display=True):
    if page_name in get_json(file='app_tree.json').keys():
        if element_string in get_json(file='app_tree.json')[page_name].keys():
            text_string = get_json(file='app_tree.json')[page_name][element_string]
    else:
        assert False, "page name {}在app_tree中不存在".format(page_name)
    if is_display:
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


# 滑动
def slide(direction, cycle=1):
    xy = poco.get_screen_size()
    w = xy[0]
    h = xy[1]
    for i in range(cycle):
        if direction == 'up':
            swipe([w/2, h*0.8], [w/2, h*0.4])
        elif direction == 'down':
            swipe([w/2, h*0.3], [w/2, h*0.9])
        elif direction == 'left':
            swipe([w*0.9, h/2], [w*0.15, h/2])
        elif direction == 'right':
            swipe([w*0.15, h/2], [w*0.9, h/2])