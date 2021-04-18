from dataclasses import dataclass
from enum import Enum
from typing import Callable, ClassVar

import requests

from processors.rest import status_code_is_ok


class BearType(Enum):
    BLACK = "BLACK"
    POLAR = "POLAR"
    BROWN = "BROWN"
    GUMMY = "GUMMY"
    UNKNOWN = "UNKNOWN"


_default_headers = {'Accept': 'application/json'}
_default_validators = [status_code_is_ok]


def validate(response: requests.Response, *response_validators: Callable):
    actual_validators = response_validators
    if not actual_validators:
        actual_validators = _default_validators
    for response_validator in actual_validators:
        response_validator(response)


@dataclass
class Bear:
    bear_id: int
    bear_type: BearType
    bear_name: str
    bear_age: float
    alaska_url: ClassVar[str]
    alaska_session: ClassVar[requests.Session]

    @classmethod
    def specify_alaska(cls, alaska_url: str):
        cls.alaska_url = alaska_url
        cls.alaska_session = requests.Session()

    @classmethod
    def all(cls, *response_validators: Callable) -> list['Bear']:
        resp = cls.alaska_session.get(f'{cls.alaska_url}/bear', headers=_default_headers)

        validate(resp, *response_validators)

        return [
            Bear(
                bear_id=bear['bear_id'],
                bear_type=BearType(bear['bear_type']),
                bear_name=bear['bear_name'],
                bear_age=bear['bear_age']
            ) for bear in resp.json()
        ]

    @classmethod
    def delete_all(cls, *response_validators: Callable):
        resp = cls.alaska_session.delete(f'{cls.alaska_url}/bear', headers=_default_headers)
        validate(resp, *response_validators)

    @classmethod
    def get(cls, bear_id: int, *response_validators: Callable) -> 'Bear':
        resp = cls.alaska_session.get(f'{cls.alaska_url}/bear/{bear_id}', headers=_default_headers)
        validate(resp, *response_validators)
        bear = resp.json()
        return Bear(
            bear_id=bear['bear_id'],
            bear_type=BearType(bear['bear_type']),
            bear_name=bear['bear_name'],
            bear_age=bear['bear_age']
        )

    @classmethod
    def create(cls, bear_type: BearType, bear_name: str, bear_age: float, *response_validators: Callable) -> 'Bear':
        resp = cls.alaska_session.post(
            f'{cls.alaska_url}/bear',
            json={
                'bear_type': bear_type.value,
                'bear_name': bear_name,
                'bear_age': bear_age
            },
            headers={'Content-Type': 'application/json'}.update(_default_headers)
        )
        validate(resp, *response_validators)
        return Bear(bear_id=int(resp.text), bear_type=bear_type, bear_name=bear_name, bear_age=bear_age)

    def update(self, *response_validators: Callable):
        json_data = {}

        if self.bear_id:
            json_data['bear_id'] = self.bear_id
        if self.bear_type:
            json_data['bear_type'] = self.bear_type.value
        if self.bear_name:
            json_data['bear_name'] = self.bear_name
        if self.bear_age:
            json_data['bear_age'] = self.bear_age

        resp = self.alaska_session.put(
            f'{self.alaska_url}/bear/{self.bear_id}',
            json=json_data,
            headers={'Content-Type': 'application/json'}.update(_default_headers)
        )
        validate(resp, *response_validators)

    def delete(self, *response_validators: Callable):
        resp = self.alaska_session.delete(
            f'{self.alaska_url}/bear/{self.bear_id}',
            headers={'Content-Type': 'application/json'}.update(_default_headers)
        )
        validate(resp, *response_validators)
