from Function.ui_common_function import *


class UiFunction:

    @staticmethod
    def login(account, password):
        # 先判断是否已经登录
        if check('CB214', type=1) is True:
            pass
        else:
            # 点击登录
            click('CB172')
            # 检查到达welcome Back
            check('CB306')
            # 判断是否存在预设账户
            if check('CB008', type=1) is True:
                click('CB008')
            else:
                poco(get_json(file='multiple_languages.json')['CB306']).offspring("android.view.View")[0].click()
                # 输入账户密码
                text(account)
                text(password)
                # 判断登录到首页
                click('CB214')

    @staticmethod
    def logout():
        # 点击 Account 页面
        click('CB008')
        # 点击 log out
        click('CB173')
        # 检查log out 弹框文案
        check('CB354')
        # 点击 log out
        poco(get_json(file='multiple_languages.json')['CB173'])[1].click()
        # 检车退出到登录页面
        click('CB172')

