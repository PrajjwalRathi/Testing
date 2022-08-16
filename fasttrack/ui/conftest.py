import pytest

ENV_OPT = "--config-env"

def pytest_addoption(parser):
    parser.addoption(ENV_OPT)


@pytest.fixture
def config_env(request):
    return request.config.getoption(ENV_OPT)