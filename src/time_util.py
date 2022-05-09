import datetime as dt
import traceback
from typing import List

import pyjson5


class Event:
    """A specific period of time in a schedule. Occurs at a time of day, but can occur at
    any date. The date is handled by the schedule.
    """

    def __init__(self, name, start, end):
        self.start = start
        self.end = end
        self.name = name

    def is_current(self):
        now = dt.datetime.now()

        return self.start < now.time() < self.end

    def force_start_dt(self, forced_time: dt.date):
        start_dt = dt.datetime(forced_time.year, forced_time.month, forced_time.day, self.start.hour,
                               self.start.minute, self.start.second, self.start.microsecond)
        return start_dt

    def force_end_dt(self, forced_time: dt.date):
        end_dt = dt.datetime(forced_time.year, forced_time.month, forced_time.day, self.end.hour,
                             self.end.minute, self.end.second, self.end.microsecond)
        return end_dt

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__(self)


class SpecificEvent(Event):
    """An event with a date and time instead of simply a time.
    Normally, events are meant to occur on multiple different days, and only the time during those days
    needs to be specified. In some cases, however, the specific event which will occur on a specific
    date and time is needed. For example, to see how many days until the next event in a schedule occurs.

    Args:
        Event (Event): This is a child of the Event class
    """

    def __init__(self, event, date):
        self.event = event
        self.name = self.event.name
        self.start = dt.datetime(date.year, date.month, date.day, self.event.start.hour,
                                 self.event.start.minute, self.event.start.second, self.event.start.microsecond)
        self.end = dt.datetime(date.year, date.month, date.day, self.event.end.hour,
                               self.event.end.minute, self.event.end.second, self.event.end.microsecond)

    def is_current(self):
        now = dt.datetime.now()

        return self.start < now < self.end


class Schedule:
    """
    Either provide json through sched_data, or read json from sched_path.
    NOTE: This is a schedule of events throughout a day, meaning the events shouldn't overlap.
    If the events overlap, behavior will be unpredictable.
    The json must be formatted like so:

    ```
    {
        "Default Schedule": {
            "default": "Break",
            "events": {
                "Before School": ["0:00", "8:55"],
                "A Block": ["8:55", "10:20"],
                "B Block": ["10:30", "11:45"],
                "C Block": [],
                "D Block": [],
                "School Over": []
            }
        }
    }
    ```
    """

    def __init__(self, sched_data=None, name="Default Schedule", sched_path=None):
        if not sched_data:
            try:
                with open(sched_path, 'r') as f:
                    sched_data = pyjson5.decode_io(f, None, False)
            except Exception:
                print(f"Schedule at '{sched_path}' not found. Exception: {traceback.format_exc()}")

        self.name = name
        try:
            self.sched_json = sched_data
            self.default_name = self.sched_json.get('default', '')  # if no default name is given, the name will be empty
            self.weekdays = self.sched_json.get('weekdays', None)
            if self.weekdays:
                self.weekdays = [weekday.lower() for weekday in self.weekdays]
            self.months = self.sched_json.get('days', None)
            if self.months:
                self.months = [month.lower() for month in self.months]
            self.days_of_month = self.sched_json.get('days_of_month', None)
            self.priority = self.sched_json.get('priority', -1)

            # Get all event data
            self.events = []
            for name, event_data in self.sched_json['events'].items():
                start_time_tuple = event_data[0].split(":")
                start_time = dt.time(hour=int(start_time_tuple[0]), minute=int(start_time_tuple[1]), second=0)
                end_time_tuple = event_data[1].split(":")
                end_time = dt.time(hour=int(end_time_tuple[0]), minute=int(end_time_tuple[1]), second=0)
                self.events.append(Event(name, start_time, end_time))
        except Exception:
            print(f"Schedule improperly configured. Exception: {traceback.format_exc()}")

    def get_current_event(self) -> Event:
        """
        Return the currently active event. If they overlap, an arbitrary one will be chosen.
        """
        active_events = []
        for event in self.events:
            if event.is_current():
                active_events.append(event)

        if len(active_events) > 0:
            return active_events[0]
        return None

    def get_prev(self):
        now = dt.datetime.now()
        prev = None
        for event in self.events:
            if event.start > now.time():
                return prev

    def get_next(self):
        now = dt.datetime.now()
        for event in self.events:
            if event.start > now.time():
                return event
        return None

    def event_is_active(self):
        """ Return whether or not there is currently an event going on """
        for event in self.events:
            if event.is_current():
                return True
        return False

    def is_current(self):
        """ Based on weekday, months, and days_of_week constraints, return whether this schedule should be active. """
        now = dt.datetime.now()
        is_current_weekday = True
        if self.weekdays:
            is_current_weekday = now.strftime('%A').lower() in self.weekdays
        is_current_month = True
        if self.months:
            is_current_month = now.strftime('%B').lower() in self.months
        is_current_day_of_month = True
        if self.days_of_month:
            is_current_day_of_month = now.strftime('%d').lower() in self.days_of_month

        return is_current_weekday and is_current_month and is_current_day_of_month

    def is_current_at(self, time: dt.datetime) -> bool:
        """Returns whether the schedule is active at the given time.
        For example, it will check to see if the weekdays and days_of_month match the given time.

        Args:
            time (dt.datetime): Time which will be tested

        Returns:
            bool: Whether or not the schedule is active at the given time
        """
        is_current_weekday = True
        if self.weekdays:
            is_current_weekday = time.strftime('%A').lower() in self.weekdays
        is_current_month = True
        if self.months:
            is_current_month = time.strftime('%B').lower() in self.months
        is_current_day_of_month = True
        if self.days_of_month:
            is_current_day_of_month = time.strftime('%d').lower() in self.days_of_month

        return is_current_weekday and is_current_month and is_current_day_of_month


class ScheduleHandler:
    """
    Container of multiple schedules. Schedules should occur on distinct days of the year, and shouldn't overlap.
    If they must overlap, a higher priority level should be given to one of them.
    If two schedules overlap and have the same priority level, an arbitrary one will be chosen.
    """

    def __init__(self, sched_path=None, sched_data=None, default_event_name=""):
        self.schedules = []
        self.sched_data_json = None
        self.default = None
        self.default_event_name = default_event_name
        if not sched_data:
            try:
                with open(sched_path, 'r') as f:
                    self.sched_data_json = pyjson5.decode_io(f, None, False)
            except Exception:
                print(f"Schedules at '{sched_path}' not found. Exception: {traceback.format_exc()}")

        else:
            # load sched_data as a json string if sched_data is a string. Otherwise, simply load it as json.
            self.sched_data_json = pyjson5.decode(sched_data) if isinstance(sched_data, str) else sched_data

        # create Schedule objects for each schedule in the json
        for sched_name, sched_data in self.sched_data_json.items():
            sched = Schedule(name=sched_name, sched_data=sched_data)
            self.schedules.append(sched)
            if sched_name.lower() == "default" or sched_name.lower() == "default schedule":
                self.default = sched

        # select an arbitrary default is one wasn't properly specified. The default schedule should
        # have the name "Default Schedule" or "Default"
        if not hasattr(self, 'default'):
            self.default = self.schedules[0]

    def get_current_sched(self) -> Schedule:
        """Return the schedule which applies to the current day and has a higher priority than conflicting schedules

        If a schedule has a higher priority, it will override any other schedules with a lower priority, meaning
        they won't be chosen.

        Returns:
            Schedule: The schedule which is active at the current time
        """

        # collect all valid schedules and determine what the highest priority is among current ones
        highest_priority = -1
        valid_scheds = []
        for sched in self.schedules:
            if sched.is_current():
                valid_scheds.append(sched)
                if sched.priority > highest_priority:
                    highest_priority = sched.priority

        # now remove schedules with a lower priority than the highest
        for sched in valid_scheds:
            if sched.priority < highest_priority:
                valid_scheds.remove(sched)

        if len(valid_scheds) > 0:
            return valid_scheds[0]  # if more than one have the same priority, an arbitrary one is selected at index 0
        else:
            return None

    def get_current_event(self) -> List[Event]:
        """Get which event is currently active. If more than one event is currently active, an arbitrary
        one will be selected.
        Remember that events (which are specified in settings.json) should not overlap!

        Returns:
            Event: The event which is currently active.
        """
        current_sched = self.get_current_sched()
        if current_sched:
            return current_sched.get_current_event()
        return None

    def get_current_event_str(self) -> str:
        """Return the name of the current event. If an event isn't active, return the default event
        name for the current schedule. If no schedule is active, return an empty string.

        Returns:
            str: Name of current event
        """
        output = ""
        current_event = self.get_current_event()
        if current_event:
            output = str(current_event)
        else:
            current_sched = self.get_current_sched()
            if current_sched:
                output = current_sched.default_name
            else:
                output = self.default_event_name

        return output

    def get_prev(self, max_test=365) -> SpecificEvent:
        """Return what the previous event was based on the given schedules. If an event didn't occur earlier
        on the current day, continually test using the is_current_at() function to see if there is an event
        on a given day in the past. Text for max_test days, then give up.

        Args:
            max_test (int, optional): How many days into the past to test for. Defaults to 365.

        Returns:
            SpecificEvent: An event with a datetime instead of just a time
        """
        now = dt.datetime.now()
        events: List[Event] = [event for sched in self.schedules for event in sched.events]
        prev_event = None

        # first try to find an event which is after the current one
        for event in events:
            # see if the current event has an end time earlier than now
            if not prev_event and event.end < now.time():
                prev_event = event
            # see if the event starts after the current prev_event
            elif prev_event and event.end > prev_event.end and event.end < now.time():
                prev_event = event

        event_date = now

        # if no previous event was found (we are currently before any events in the schedule, or on the first event),
        # then find the earliest one which starts before now.
        if not prev_event:
            days_behind = 1

            # keep going forward and see if there is an event in the next day. If not more events exist in the coming
            # days, this could go on forever, so only test for max_test days (1 year by default)
            while days_behind < max_test:
                event_date = dt.datetime(now.year, now.month, now.day - days_behind, 0, 0, 0)
                current_scheds = [sched for sched in self.schedules if sched.is_current_at(event_date)]
                events = [event for sched in current_scheds for event in sched.events]
                for event in events:
                    if not prev_event:
                        prev_event = event
                    elif event.end > prev_event.end:
                        prev_event = event
                if not prev_event:
                    days_behind -= 1
                else:
                    break

        return SpecificEvent(prev_event, event_date)

    def get_next(self, max_test=365) -> SpecificEvent:
        """Return what the next event will be based on the given schedules. If another event won't occur
        on the current day, continually test using the is_current_at() function to see if there is an event
        on a given day in the future. Text for max_test days, then give up.

        Args:
            max_test (int, optional): How many days into the future to test for. Defaults to 365.

        Returns:
            SpecificEvent: An event with a datetime instead of just a time
        """
        now = dt.datetime.now()
        events: List[Event] = [event for sched in self.schedules for event in sched.events]
        next_event = None

        # first try to find an event which is after the current one
        for event in events:
            # see if the current event has a start time later than now
            if not next_event and event.start > now.time():
                next_event = event
            # see if the event starts earlier than the current next_event
            elif next_event and event.start < next_event.start and event.start > now.time():
                next_event = event

        event_date = now

        # if no next event was found (all events take place before now on the schedule),
        # then find the earliest one which starts before now.
        if not next_event:
            days_ahead = 1

            # keep going forward and see if there is an event in the next day. If not more events exist in the coming
            # days, this could go on forever, so only test for max_test days (1 year by default)
            while days_ahead < max_test:
                event_date = dt.datetime(now.year, now.month, now.day + days_ahead, 0, 0, 0)
                current_scheds = [sched for sched in self.schedules if sched.is_current_at(event_date)]
                events = [event for sched in current_scheds for event in sched.events]
                for event in events:
                    if not next_event:
                        next_event = event
                    elif event.start < next_event.start:
                        next_event = event
                if not next_event:
                    days_ahead += 1
                else:
                    break

        return SpecificEvent(next_event, event_date)

    def get_remaining_str(self):
        """ Forcibly get the time until the next event, then return a string of it """
        now = dt.datetime.now()
        if self.event_is_active():
            rem_time = self.get_current_event().force_end_dt(now) - now  # get start from current event from current schedule
        else:
            rem_time = self.get_next().start - now

        days = rem_time.seconds // (3600 * 24)
        hours = (rem_time.seconds % 3600 * 24) // 3600
        minutes = (rem_time.seconds % 3600) // 60
        seconds = (rem_time.seconds % 60)

        if days > 0:
            return f'{days}:{hours}:{minutes:02}:{seconds:02}'
        else:
            return f'{hours}:{minutes:02}:{seconds:02}'

    def get_remaining_str_verbose(self):
        """
        Return a string which will display how long until the current event ends or the next one starts
        """
        now = dt.datetime.now()
        next_event = self.get_next()
        # Pick the first current event
        if self.event_is_active():
            rem_time = self.get_current_event().force_end_dt(now) - now  # get start from current event from current schedule
        else:
            rem_time = next_event.start - now

        days = rem_time.days
        hours = rem_time.seconds // 3600
        minutes = (rem_time.seconds % 3600) // 60
        seconds = (rem_time.seconds % 60)

        current_sched = self.get_current_sched()
        event_is_active = False
        if current_sched:
            event_is_active = current_sched.event_is_active()
        remaining_text = "remaining" \
                         if event_is_active \
                         else f"until {next_event}"

        if days > 0:
            return f'{days} days, {hours}:{minutes:02}:{seconds:02} {remaining_text}'
        else:
            return f'{hours}:{minutes:02}:{seconds:02} {remaining_text}'

    def event_is_active(self):
        """ Return whether or not there is currently an active event going on """
        current_sched = self.get_current_sched()
        if current_sched:
            return current_sched.event_is_active()
        else:
            return False


# hide hours if it equals 0, minutes and seconds always 2 digits
def hours_minutes_seconds(td):
    hours = td.seconds // 3600
    minutes = (td.seconds % 3600) // 60
    seconds = (td.seconds % 60)

    return '{}:{:02}:{:02}'.format(hours, minutes, seconds)


def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs(int(seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s%d days %d hours\n%d minutes %d seconds' % (sign_string, days, hours, minutes, seconds)
    elif hours > 0:
        return '%s%dh\n%dm%ds' % (sign_string, hours, minutes, seconds)
    elif minutes > 0:
        return '%s%dm%ds' % (sign_string, minutes, seconds)
    else:
        return '%s%ds' % (sign_string, seconds)
