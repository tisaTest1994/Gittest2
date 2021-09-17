

def pytest_configure(config):
    marker_list = ["multiprocess", "singleProcess", "pro", "complianceService"]
    for markers in marker_list:
        config.addinivalue_line("markers", markers)
