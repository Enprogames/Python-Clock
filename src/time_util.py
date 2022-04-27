import datetime as dt
import json
import traceback
from typing import List


class Event:

    def __init__(self, name, start, end):
        self.start = start
        self.end = end
        self.name = name

    def __str__(self):
        return self.name

    def is_current(self):
        now = dt.datetime.now()

        return self.start < now.time() < self.end

    def get_start(self):
        now = dt.datetime.now()
        start_dt = dt.datetime(now.year, now.month, now.day, self.start.hour,
                               self.start.minute, self.start.second, self.start.microsecond)
        return start_dt

    def get_end(self):
        now = dt.datetime.now()
        end_dt = dt.datetime(now.year, now.month, now.day, self.end.hour,
                             self.end.minute, self.end.second, self.end.microsecond)
        return end_dt


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
                    sched_data = json.load(f)
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

    def get_current_events(self):
        """
        Return a list of events in this schedule which are currently going on. If no events are active, return an in-between event.
        """
        active_events = []
        for event in self.events:
            if event.is_current():
                active_events.append(event)

        # if no event is currently in effect (e.g. during break time), find the two closest events and create a temporary in-between event
        if len(active_events) == 0:
            prev = self.get_prev()
            next = self.get_next()

            now = dt.datetime.now()
            if not (prev or next):  # no events exist, so return an event spanning the entire day
                active_events.append(Event(self.default_name, dt.datetime(now.year, now.month, now.day, 0, 0, 0), dt.datetime(now.year, now.month, now.day, 23, 59, 59)))
            elif not prev:
                active_events.append(Event(self.default_name, dt.datetime(now.year, now.month, now.day, 0, 0, 0), self.get_next().get_start()))
            elif not next:
                active_events.append(Event(self.default_name, self.get_prev().get_end(), dt.datetime(now.year, now.month, now.day, 23, 59, 59)))
            active_events.append(Event(self.default_name, self.get_prev().get_end(), self.get_next().get_start()))

        return active_events

    def get_prev(self):
        now = dt.datetime.now()
        prev = None
        for event in self.events:
            if event.get_start() > now:
                return prev

    def get_next(self):
        now = dt.datetime.now()
        for event in self.events:
            if event.get_start() > now:
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


class ScheduleHandler:
    """
    Container of multiple schedules
    """
    def __init__(self, sched_path=None, sched_data=None):
        self.schedules = []
        self.sched_data_json = None
        self.sched_days = {}
        if not sched_data:
            try:
                with open(sched_path, 'r') as f:
                    self.sched_data_json = json.load(f)
            except Exception:
                print(f"Schedules at '{sched_path}' not found. Exception: {traceback.format_exc()}")

        else:
            self.sched_data_json = sched_data
        for sched_name, sched_data in self.sched_data_json.items():
            sched = Schedule(name=sched_name, sched_data=sched_data)
            self.schedules.append(sched)
            if 'days' in sched_data:
                for day in sched_data['days']:
                    self.sched_days[day] = sched

        self.default = self.schedules[0]

    def get_current_scheds(self):
        """
        Return all schedules which apply to the current time and have the highest priority.

        If a schedule has a higher priority, it will override any other schedules with a lower priority, meaning
        they won't be returned.
        """
        now = dt.datetime.now()

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

        return valid_scheds

    def get_current_events(self) -> List[Event]:
        events = []

        for sched in self.get_current_scheds():
            for event in sched.get_current_events():
                events.append(event)

        return events

    def get_current_events_str(self) -> str:
        """
        Return what events are currently going on in the form "event1, event2, and event3"
        """
        result = ""
        events = self.get_current_events()
        for i, event in enumerate(self.get_current_events()):
            if i >= len(events)-1 and i > 0:  # if this is the last item of several, return e.g. " and event"
                result += f" and {event.name}"
            elif i > 0:
                result += f", {event.name}"
            else:
                result += event.name
        return result

    def get_prev(self):
        return self.get_current_sched().get_prev()

    def get_next(self):
        return self.get_current_sched().get_next()

    def get_remaining_str(self):
        """ Forcibly get the time until the next event, then return a string of it """
        now = dt.datetime.now()
        rem_time = self.get_current_events()[0].get_end() - now  # get start from current event from current schedule
        hours = rem_time.seconds // 3600
        minutes = (rem_time.seconds % 3600) // 60
        seconds = (rem_time.seconds % 60)

        return f'{hours}:{minutes:02}:{seconds:02}'

    def get_remaining_str_verbose(self):
        """
        Return a string which will display how long until the current event ends or the next one starts
        """
        now = dt.datetime.now()
        # Pick the first current event
        rem_time = self.get_current_events()[0].get_end() - now  # get start from current event from current schedule
        hours = rem_time.seconds // 3600
        minutes = (rem_time.seconds % 3600) // 60
        seconds = (rem_time.seconds % 60)

        current_sched = self.get_current_scheds()[0]
        remaining_text = "remaining" \
                         if current_sched.event_is_active() \
                         else f"until {current_sched.get_next().name}"

        return f'{hours}:{minutes:02}:{seconds:02} {remaining_text}'

    def event_is_active(self):
        """ Return whether or not there is currently an active event going on """
        current_sched = self.get_current_sched()
        if current_sched:
            return current_sched.event_is_active()
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
