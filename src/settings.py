import os
import pyjson5

DEFAULT_SETTINGS = """
{
    "fact_type": "fact", // options: ["dadjoke", "fact"]

    "window_settings": {
        "background": "#263238",
        "foreground": "white",  // text and other widgets
        "fullscreen": false,
        "window_manager": "tkinter",  // options: ["tkinter"]. Future options: ["tkinter-canvas", "eel"]
        "event_text": "Block",
        "show_time": true,
        "show_date": true,
        "show_fact": true,
        "show_alert": true,  // e.g. "Block: Lunch"
        "show_remaining": true,
        "show_summer": false,  // displays how long until the summer holidays start

        "font_multiplier": 1,
        "resize_dynamically": true,
        "font_size": 100  // only used if dynamic resizing is false
    },
    "default_event_name": "Break",  // what will show on the clock when no schedule is active e.g. on weekends
    "schedules": {
        "Default Schedule": {
            "default": "Break",
            "weekdays": ["monday", "tuesday", "thursday", "friday"],
            // Events should not overlap each other
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
            // schedules with a higher priority will override other ones so that only the highest priority
            // schedules will be active. Schedules without a priority attribute will be given one of -1
            "priority": 1,
            // Events should not overlap each other
            "events": {
                "A Block": ["8:55", "9:40"],
                "B Block": ["9:50", "10:35"],
                "C Block": ["10:45", "11:30"],
                "D Block": ["11:40", "12:25"],
                "Lunch": ["12:25", "13:15"],
                "Flex 1": ["13:15", "14:15"],
                "Flex 2": ["14:15", "15:05"]
            }
        },
        "Remembrance Day Schedule": {
            "default": "Break",
            "months": ["november"],
            "days_of_month": [8],
            // schedules with a higher priority will override other ones so that only the highest priority
            // schedules will be active. Schedules without a priority attribute will be given one of -1
            "priority": 2,
            // Events should not overlap each other
            "events": {
                "A Block": ["8:55", "9:40"],
                "B Block": ["9:50", "10:35"],
                "C Block": ["10:45", "11:30"],
                "D Block": ["11:40", "12:25"],
                "Lunch": ["12:25", "13:15"],
                "Remebrance Day Ceremony": ["13:15", "15:05"]
            },
            "Christmas Celebration Schedule": {
                "default": "Break",
                "months": ["Demember"],
                "days_of_month": [10],
                // schedules with a higher priority will override other ones so that only the highest priority
                // schedules will be active. Schedules without a priority attribute will be given one of -1
                "priority": 2,
                // Events should not overlap each other
                "events": {
                    "A Block": ["8:55", "9:40"],
                    "B Block": ["9:50", "10:35"],
                    "C Block": ["10:45", "11:30"],
                    "D Block": ["11:40", "12:25"],
                    "Lunch": ["12:25", "13:15"],
                    "Christmas Celebration": ["13:15", "15:05"]
                }
            }
        }
    }
}
"""


class SettingsHandler:

    def __init__(self, setting_json=None, setting_file=None):
        self.default_settings = pyjson5.decode(DEFAULT_SETTINGS)
        # if the file doesn't exist, create a new one with the default settings
        if not setting_json:
            if not os.path.exists(setting_file):
                with open(setting_file, 'w') as f:
                    pyjson5.encode_io(self.default_settings, f)
            with open(setting_file, 'r') as f:
                self.setting_json = pyjson5.decode_io(f, None, False)

        # Loop through default settings and try to get the value from the provided settings data.
        # If the value doesn't exist in the provided data, default values will be used.
        for key, value in self.default_settings.items():
            default_val = value
            setting_val = self.setting_json.get(key, default_val)
            setattr(self, key, setting_val)  # create attributes e.g. self.fact_type = "dadjoke"
