import pytest
from main import create_random_user


class TestCreate(object):
    @classmethod
    def setup_class(cls):
        print('start')

    @classmethod
    def teardown_class(cls):
        print('end')

    def test_create_random_user():
        pass
