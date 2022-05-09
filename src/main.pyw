#!/usr/bin/env python
import os

# module level imports
from window import MainWindow
from time_util import ScheduleHandler
from fact_util import FactHandler
from settings import SettingsHandler


ROOT_DIR = ''
if os.path.basename(os.getcwd()) == 'src':
    ROOT_DIR = ''
else:
    ROOT_DIR = 'src'
SETTINGS_PATH = os.path.join(ROOT_DIR, 'settings.json')

setting_handler = SettingsHandler(setting_file=SETTINGS_PATH)

sched_handler = ScheduleHandler(sched_data=setting_handler.schedules,
                                default_event_name=setting_handler.default_event_name)

fact_handler = FactHandler(fact_type=setting_handler.fact_type)

window = MainWindow(schedule_handler=sched_handler,
                    fact_handler=fact_handler,
                    **setting_handler.window_settings
                    )
window.mainloop()
