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

        self.complex_sched = """
        {
            "Default Schedule": {
                "default": "Break",
                "weekdays": ["monday", "tuesday", "thursday", "friday"],
                "events": {
                    "A Block": ["8:55", "10:20"],
                    "B Block": ["10:30", "11:45"],
                    "Lunch": ["11:45", "12:25"],
                    "C Block": ["12:25", "13:40"],
                    "D Block": ["13:50", "15:05"]
                }
            },
            "Flex Schedule": {
                "default": "Break",
                "weekdays": ["wednesday"],
                //  schedules with a higher priority will override other ones so that only the highest priority
                //  schedules will be active. Schedules without a priority attribute will be given one of -1
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
        except pyjson5.pyjson5.Json5IllegalCharacter as e:
            assert False, f"Exception raised when trying to load json string: {e}"

        try:
            pyjson5.decode(self.complex_sched)
        except pyjson5.pyjson5.Json5IllegalCharacter as e:
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

    def test_get_next_simple(self, initialize):
        with freeze_time("2022-6-15 9:30:00"):
            sched_handler = ScheduleHandler(sched_data=self.simple_sched)
            assert sched_handler.get_next().name == "B Block"  # the schedule should wrap around so that A Block is the next block
        with freeze_time("2022-6-15 15:06:00"):
            sched_handler = ScheduleHandler(sched_data=self.complex_sched)
            assert sched_handler.get_next().name == "A Block"  # the schedule should wrap around so that A Block is the next block

    # @pytest.mark.skip(reason="retrieving of an event for the next day isn't implemented yet")
    @freeze_time("2022-6-15 15:06:00")  # use a time right after flex 2 has ended
    def test_get_next_complex(self, initialize):
        pass

    def test_get_prev(self):
        pass
