#!/usr/bin/env python

import datetime as dt
import argparse
import json
# these must be installed on raspberry pi
import requests
from threading import Timer
import traceback
import os
import pyjson5

# module level imports
from window import MainWindow
from time_util import ScheduleHandler
from fact_util import FactHandler


ROOT_DIR = ''
if os.path.basename(os.getcwd()) == 'src':
    ROOT_DIR = ''
else:
    ROOT_DIR = 'src'
SETTINGS_PATH = os.path.join(ROOT_DIR, 'settings.json')

DEFAULT_SETTINGS = """
{
    "window_settings": {
        "background": "#263238",
        "foreground": "white",  // text and other widgets
        "fullscreen": false,
        "window_manager": "tkinter",  // options: ["tkinter"]. Future options: ["tkinter-canvas", "eel", "electron"]
        "event_text": "Block",
        "show_time": true,
        "show_date": true,
        "show_fact": true,
        "show_alert": true,  // e.g. "Block: Lunch"
        "show_remaining": true,
        "show_summer": false,  // displays how long until the summer holidays start
        "fact_type": "dadjoke", // options: ["fact", "joke", "dadjoke"]
        "font_multiplier": 1,
        "resize_dynamically": true,
        "font_size": 100,  // use if dynamic resizing isn't enabled
    },
    "schedules": {
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
            // schedules with a higher priority will override other ones so that only the highest priority
            // schedules will be active. Schedules without a priority attribute will be given one of -1
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
        },
        "Remebrance Day Schedule": {
            "default": "Break",
            "months": ["november"],
            "days_of_month": [8],
            // schedules with a higher priority will override other ones so that only the highest priority
            // schedules will be active. Schedules without a priority attribute will be given one of -1
            "priority": 2,
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

# if the file doesn't exist, create a new one with the default settings
if not os.path.exists(SETTINGS_PATH):
    with open(SETTINGS_PATH, 'w') as f:
        default_settings = pyjson5.decode(DEFAULT_SETTINGS)
        pyjson5.encode_io(default_settings, f)
with open(SETTINGS_PATH, 'r') as f:
    setting_json = pyjson5.decode_io(f, None, False)

sched_handler = ScheduleHandler(sched_data=setting_json['schedules'])

fact_handler = FactHandler()

window = MainWindow(schedule_handler=sched_handler,
                    fact_handler=fact_handler,
                    **setting_json['window_settings']
                    )
window.mainloop()
