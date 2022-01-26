from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from run import *

poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# 元素操作
def operate_element_app(page_name, element_string, type='click', wait_time_max=5, input_string=''):
    if page_name in get_json(file='app_tree.json').keys():
        if element_string in get_json(file='app_tree.json')[page_name].keys():
            translation_code = get_json(file='app_tree.json')[page_name][element_string]
            text_string = get_json(file='multiple_languages_app.json')[translation_code]
            if type == 'click':
                poco(text_string).click()
                logger.info('点击{}元素'.format(text_string))
            elif type == 'check':
                wait_time = 0
                while wait_time < wait_time_max:
                    wait_time = wait_time + 1
                    sleep(1)
                    if poco(text_string).exists() is True:
                        logger.info('检查{}元素，是否存在前页面:{}'.format(text_string, poco(text_string).exists()))
                        return True
                return False
            elif type == 'input':
                poco(text_string).set_text(input_string)
                logger.info('点击{},输入{}'.format(text_string, input_string))
            else:
                return poco(text_string)
    else:
        assert False, "page name {}在app_tree中不存在".format(page_name)


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
