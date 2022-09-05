import pytest
import sys


@pytest.fixture(scope='session')
def partner():
    partner = sys.argv[2]
    # partner = 'infinni'
    return partner
