import requests


def status_code_is_ok(response):
    assert response.status_code == requests.codes.ok
