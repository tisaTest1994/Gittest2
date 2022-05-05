from Function.api_function import *
from Function.operate_sql import *


@allure.feature("mobile api convert 相关 testcases")
class TestLightModeApi:

    # 初始化class
    def setup_method(self):
        with allure.step("登录客户账户获得后续操作需要的token"):
            ApiFunction.add_headers()

    @allure.title('test_light_mode_001')
    @allure.description('根据id编号查询单笔交易')
    def test_light_mode_001(self):
        with allure.step("获得交易transaction_id"):
            r = session.request('GET', url='{}/light/config'.format(env_url, headers=headers))
        with allure.step("状态码和返回值"):
            logger.info('状态码是{}'.format(str(r.status_code)))
            logger.info('返回值是{}'.format(str(r.text)))
        with allure.step("校验状态码"):
            assert r.status_code == 200, "http 状态码不对，目前状态码是{}".format(r.status_code)
        with allure.step("light mode配置校验"):
            # json = {"currencies":[{"symbol":"BTC","type":2,"deposit":{"methods":["BTC"]},"withdraw":{"methods":["BTC"],"limit":{"min":"0.001","max":"-1"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"0.0006"}},"conversion":{"limit":{"min":"0.0002","max":"5"}}},{"symbol":"ETH","type":2,"deposit":{"methods":["ERC20"]},"withdraw":{"methods":["ERC20"],"limit":{"min":"0.02","max":"-1"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"0.004"}},"conversion":{"limit":{"min":"0.002","max":"100"}}},{"symbol":"USDT","type":2,"deposit":{"methods":["ERC20"]},"withdraw":{"methods":["ERC20"],"limit":{"min":"40","max":"-1"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"12"}},"conversion":{"limit":{"min":"10","max":"200000"}}},{"symbol":"EUR","type":1,"deposit":{"methods":["SEPA"]},"withdraw":{"methods":["SEPA"],"limit":{"min":"25","max":"50000"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"2.5"}},"conversion":{"limit":{"min":"10","max":"200000"}}},{"symbol":"GBP","type":1,"deposit":{"methods":["FPS"]},"withdraw":{"methods":["FPS"],"limit":{"min":"20","max":"40000"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"2.5"}},"conversion":{"limit":{"min":"10","max":"200000"}}},{"symbol":"CHF","type":1,"deposit":{"methods":["SIC"]},"withdraw":{"methods":["SIC"],"limit":{"min":"25","max":"50000"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"4.5"}},"conversion":{"limit":{"min":"10","max":"200000"}}},{"symbol":"BRL","type":1,"deposit":{"methods":["PIX"]},"withdraw":{"methods":["PIX"],"limit":{"min":"20","max":"300000"},"fee":{"is_single":True,"object":"Customer","method":"Fixed","value":"3.6"}},"conversion":{"limit":{"min":"50","max":"1000000"}}}],"pairs":[{"pair":"BTC-ETH"},{"pair":"BTC-USDT"},{"pair":"ETH-USDT"},{"pair":"BTC-EUR"},{"pair":"ETH-EUR"},{"pair":"USDT-EUR"},{"pair":"BTC-GBP"},{"pair":"ETH-GBP"},{"pair":"USDT-GBP"},{"pair":"BTC-CHF"},{"pair":"ETH-CHF"},{"pair":"USDT-CHF"},{"pair":"BTC-BRL"},{"pair":"ETH-BRL"},{"pair":"USDT-BRL"},{"pair":"BTC-VND"},{"pair":"ETH-VND"},{"pair":"USDT-VND"}]}
            json = {
                "currencies": [{
                    "symbol": "BTC",
                    "type": 2,
                    "deposit": {
                        "methods": ["BTC"]
                    },
                "withdraw": {
                    "methods": ["BTC"],
                    "limit": {
                        "min": "0.001",
                        "max": "-1"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "0.0006"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "0.0002",
                        "max": "5"
                    }
                }
            }, {
                "symbol": "ETH",
                "type": 2,
                "deposit": {
                    "methods": ["ERC20"]
                },
                "withdraw": {
                    "methods": ["ERC20"],
                    "limit": {
                        "min": "0.02",
                        "max": "-1"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "0.004"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "0.002",
                        "max": "100"
                    }
                }
            }, {
                "symbol": "USDT",
                "type": 2,
                "deposit": {
                    "methods": ["ERC20"]
                },
                "withdraw": {
                    "methods": ["ERC20"],
                    "limit": {
                        "min": "40",
                        "max": "-1"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "12"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "10",
                        "max": "200000"
                    }
                }
            }, {
                "symbol": "EUR",
                "type": 1,
                "deposit": {
                    "methods": ["SEPA"]
                },
                "withdraw": {
                    "methods": ["SEPA"],
                    "limit": {
                        "min": "25",
                        "max": "50000"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "2.5"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "10",
                        "max": "200000"
                    }
                }
            }, {
                "symbol": "GBP",
                "type": 1,
                "deposit": {
                    "methods": ["FPS"]
                },
                "withdraw": {
                    "methods": ["FPS"],
                    "limit": {
                        "min": "20",
                        "max": "40000"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "2.5"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "10",
                        "max": "200000"
                    }
                }
            }, {
                "symbol": "CHF",
                "type": 1,
                "deposit": {
                    "methods": ["SIC"]
                },
                "withdraw": {
                    "methods": ["SIC"],
                    "limit": {
                        "min": "25",
                        "max": "50000"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "4.5"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "10",
                        "max": "200000"
                    }
                }
            }, {
                "symbol": "BRL",
                "type": 1,
                "deposit": {
                    "methods": ["PIX"]
                },
                "withdraw": {
                    "methods": ["PIX"],
                    "limit": {
                        "min": "20",
                        "max": "300000"
                    },
                    "fee": {
                        "is_single": True,
                        "object": "Customer",
                        "method": "Fixed",
                        "value": "3.6"
                    }
                },
                "conversion": {
                    "limit": {
                        "min": "50",
                        "max": "1000000"
                    }
                }
            }],
            "pairs": [{
                "pair": "BTC-ETH"
            }, {
                "pair": "BTC-USDT"
            }, {
                "pair": "ETH-USDT"
            }, {
                "pair": "BTC-EUR"
            }, {
                "pair": "ETH-EUR"
            }, {
                "pair": "USDT-EUR"
            }, {
                "pair": "BTC-GBP"
            }, {
                "pair": "ETH-GBP"
            }, {
                "pair": "USDT-GBP"
            }, {
                "pair": "BTC-CHF"
            }, {
                "pair": "ETH-CHF"
            }, {
                "pair": "USDT-CHF"
            }, {
                "pair": "BTC-BRL"
            }, {
                "pair": "ETH-BRL"
            }, {
                "pair": "USDT-BRL"
            }, {
                "pair": "BTC-VND"
            }, {
                "pair": "ETH-VND"
            }, {
                "pair": "USDT-VND"
            }]
        }
            assert r.json() == json, "light mode配置校验错误"