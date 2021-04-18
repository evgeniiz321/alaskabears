import pytest
import requests

from alaska.bears import Bear, BearType


@pytest.fixture(scope='function')
def empty_alaska(alaska):
    Bear.delete_all()
    yield
    Bear.delete_all()


@pytest.mark.parametrize('bear_type, bear_name, bear_age', [
    pytest.param(BearType.BLACK, 'BARAK', 1.1),
    pytest.param(BearType.POLAR, 'STEPA', 2.0),
    pytest.param(BearType.BROWN, 'VASYAN', 3.0),
    pytest.param(BearType.GUMMY, 'PETROSYAN', 4.9, marks=pytest.mark.skip('Smth wrong with GUMMY bear')),
])
def test_create_bear(empty_alaska, bear_type, bear_name, bear_age):
    bear = Bear.create(bear_type=bear_type, bear_name=bear_name, bear_age=bear_age)
    bears = Bear.all()
    assert len(bears) == 1
    assert bears[0] == bear
    assert Bear.get(bear_id=bear.bear_id) == bear


def test_create_bear_upper_case_name(empty_alaska):
    bear = Bear.create(bear_type=BearType.BLACK, bear_name='vasyan', bear_age=1.0)
    assert Bear.get(bear_id=bear.bear_id).bear_name == 'VASYAN'


@pytest.mark.parametrize('bear_type, bear_name, bear_age', [
    pytest.param(BearType.UNKNOWN, 'vasyan', 25, marks=pytest.mark.skip('404 instead of 400 for bad bear type')),
    pytest.param(BearType.BLACK, '', 25, marks=pytest.mark.skip('No validation for bear name')),
    pytest.param(BearType.BROWN, 'vasyan', 0, marks=pytest.mark.skip('No validation for bear age')),
    pytest.param(BearType.BROWN, 'vasyan', -1, marks=pytest.mark.skip('No validation for bear age')),
])
def test_create_invalid_bear(empty_alaska, bear_type, bear_name, bear_age):
    def validator(response):
        assert response.status_code == requests.codes.bad_request
        assert len(Bear.all()) == 0

    pytest.raises(Exception, Bear.create(bear_type, bear_name, bear_age, validator))


def test_same_bear_creation(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear2 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    assert bear1.bear_id != bear2.bear_id

    bears = Bear.all()
    assert len(bears) == 2
    assert any(bear1 == bear for bear in bears)
    assert any(bear2 == bear for bear in bears)


def test_bear_recreation(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear2 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear2.delete()
    bear3 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    assert bear1.bear_id != bear3.bear_id

    bears = Bear.all()
    assert len(bears) == 2
    assert any(bear1 == bear for bear in bears)
    assert any(bear3 == bear for bear in bears)


def test_bear_update_name(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear1.bear_name = 'PETROSYAN'
    bear1.update()
    assert Bear.get(bear_id=bear1.bear_id) == bear1


@pytest.mark.skip('age is not updated :(')
def test_bear_update_age(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear1.bear_age = 27.0
    bear1.update()
    assert Bear.get(bear_id=bear1.bear_id) == bear1


@pytest.mark.skip('bear type is not updated :(')
def test_bear_update_type(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear1.bear_type = BearType.POLAR
    bear1.update()
    assert Bear.get(bear_id=bear1.bear_id) == bear1


@pytest.mark.skip('500 if no name is specified :(')
def test_bear_update_without_name(empty_alaska):
    bear1 = Bear.create(bear_type=BearType.BLACK, bear_name='VASYAN', bear_age=25.0)
    bear1.bear_name = None
    bear1.update()
    assert Bear.get(bear_id=bear1.bear_id) == bear1
