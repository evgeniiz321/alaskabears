import os

import pytest
import requests
from requests.exceptions import ConnectionError

from alaska.bears import Bear


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False


@pytest.fixture(scope='session')
def alaska(docker_ip, docker_services):
    port = docker_services.port_for("alaska", 8091)
    url = f'http://{docker_ip}:{port}'
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(f'{url}/info')
    )
    Bear.specify_alaska(url)
    yield


@pytest.fixture(scope="session")
def docker_compose_file(pytestconfig):
    return os.path.join(str(pytestconfig.rootdir), 'docker-compose.yml')
