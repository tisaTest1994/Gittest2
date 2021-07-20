from airtest.core.api import *
from poco.drivers.android.uiautomation import AndroidUiautomationPoco
from run import *
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# 点击某个text
def click(page_name, text_name, language=get_json()['language']):
    text_string = get_json(file='multiple_languages.json')[page_name][text_name][language]
    poco(text_string).wait_for_appearance(timeout=20)
    poco(text_string).click()

