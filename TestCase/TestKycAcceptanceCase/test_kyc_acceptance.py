from Function.api_function import *
from Function.operate_sql import *


# kyc acceptance相关cases
class TestKycAcceptanceApi:

    @pytest.mark.flaky(reruns=5, reruns_delay=1)
    def test_e3g_mgt_001(self):
        a = random.random()
        assert a > 0.3, 'error a={}'.format(a)