import pytest


class TestEvent:

    @pytest.fixture
    def initialize(self):
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_is_current(self):
        pass


class TestSchedule:
    def initialize(self):
        pass


class TestScheduleHandler:
    pass
