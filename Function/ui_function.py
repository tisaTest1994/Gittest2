from Function.ui_common_function import *


class UiFunction:

    @staticmethod
    def login(account, password):
        click(page_name='welcome_page', text_name='Log In')

