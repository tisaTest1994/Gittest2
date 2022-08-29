import pytest
import sys


@pytest.fixture(scope='session')
def partner():
    sys.argv[2]
    return 'bybit'
