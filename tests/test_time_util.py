import sys
sys.path.insert(0, 'src')
from freezegun import freeze_time
import datetime as dt
import pyjson5
import pytest
from time_util import ScheduleHandler  # , Event, Schedule,


# module imports
# from time_util import Event, Schedule, ScheduleHandler


class TestEvent:

    @pytest.fixture
    def initialize(self):
        pass

    @pytest.mark.skip(reason="test not implemented yet")
    def test_is_current(self):
        pass


class TestSchedule:
    def initialize(self):
        self.simple_sched = """
        "Flex Schedule": {
            "default": "Break",
            "weekdays": ["wednesday"],
            "priority": 1,
            "events": {
                "A Block": ["8:55", "9:40"],
                "B Block": ["9:50", "10:35"],
                "C Block": ["10:45", "11:30"],
                "D Block": ["11:40", "12:25"],
                "Lunch": ["12:25", "13:15"],
                "Flex 1": ["13:15", "14:15"],
                "Flex 2": ["14:15", "15:05"]
            }
        }
        """


class TestScheduleHandler:

    @pytest.fixture
    def initialize(self):
        self.simple_sched = """
        {
            "Flex Schedule": {
                "default": "Break",
                "weekdays": ["wednesday"],
                "priority": 1,
                "events": {
                    "A Block": ["8:55", "9:40"],
                    "B Block": ["9:50", "10:35"],
                    "C Block": ["10:45", "11:30"],
                    "D Block": ["11:40", "12:25"],
                    "Lunch": ["12:25", "13:15"],
                    "Flex 1": ["13:15", "14:15"],
                    "Flex 2": ["14:15", "15:05"]
                }
            }
        }
        """
        # make sure the schedule json is valid

        try:
            pyjson5.decode(self.simple_sched)
        except pyjson5.JSONDecodeError as e:
            assert False, f"Exception raised when trying to load json string: {e}"

        self.ablock_fake_time = dt.datetime.strptime("2022-6-15 9:30:00", '%Y-%m-%d %H:%M:%S')
        self.after_schedule_fake_time = dt.datetime.strptime("2022-6-15 15:06:00", '%Y-%m-%d %H:%M:%S')

    def test_json_load(self, initialize):
        """ It should be possible to load either a string of json or a json object into the ScheduleHandler """
        try:
            sched_handler1 = ScheduleHandler(sched_data=pyjson5.decode(self.simple_sched))
            sched_handler1.schedules
        except Exception as e:
            assert False, f"Exception raised when passing json to ScheduleHandler(): {e}"
        try:
            sched_handler2 = ScheduleHandler(sched_data=self.simple_sched)
            sched_handler2.schedules
        except Exception as e:
            assert False, f"Exception raised when passing json string to ScheduleHandler(): {e}"

    @freeze_time("2022-6-15 9:30:00")  # use a time right during a block
    def test_get_next_simple(self, initialize):
        assert dt.datetime.now() == self.ablock_fake_time  # make sure the fake time is working
        sched_handler = ScheduleHandler(sched_data=self.simple_sched)
        assert sched_handler.get_next().name == "B Block"  # the schedule should wrap around so that A Block is the next block

    @pytest.mark.skip(reason="retrieving of an event for the next day isn't implemented yet")
    @freeze_time("2022-6-15 15:06:00")  # use a time right after flex 2 has ended
    def test_get_next_complex(self, initialize):
        assert dt.datetime.now() == self.after_schedule_fake_time  # make sure the fake time is working
        sched_handler = ScheduleHandler(sched_data=self.simple_sched)
        assert sched_handler.get_next().name == "A Block"  # the schedule should wrap around so that A Block is the next block

    def test_get_previous(self):
        pass
