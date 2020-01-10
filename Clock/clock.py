#import tkinter as tk
from time_util import *
import window as w
#import time as t
from datetime import time, datetime
import argparse
# these must be installed on raspberry pi
import requests
#from bs4 import BeautifulSoup as soup
from threading import Thread, Timer, Event
#import random
#import urllib.request
import sys
import traceback
import os.path
import os

parser = argparse.ArgumentParser(description = 'Control Elements of the Clock')
parser.add_argument('-f', '--font', type = int, default=100, dest='font', required = False, help = '-f multiply font size for clock elements by an int')
parser.add_argument('-s', '--schedule', type = str, default=None, dest='schedule', required = False, help = '-s change what schedule to use (n = normal schedule, f = flex schedule, c = custom schedule, w = weekend')
args = parser.parse_args()

font_size = parser.parse_args().font

schedule_override = parser.parse_args().schedule

got_joke = False

class perpetualTimer():

   def __init__(self,hFunction, t):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

def get_block(now):

    for x in range(len(blocks)-1):
        #print(blocks[x].name, blocks[x].start, blocks[x].end)
        if blocks[x].is_current_block(now):
            #print(blocks.index(blocks[x]))
            return blocks[x]
    return blocks[-1]


def get_joke():
    try:
        headers = {'User-Agent': 'My Library (https://github.com/Enprogames/Python-Clock/)', 'Accept': 'application/json'}
        return requests.get('https://icanhazdadjoke.com/', headers=headers).json().get('joke')
    except:
        f = open('/tmp/dadjoke', 'r')
        return f.read()

def set_joke():
    try:

        joke = get_joke()
        w.fact_label.config(text = joke)

    except Exception:
        try:
            #w.fact_label.config(text = "Error Getting Joke{}".format(random.randint(0,9)))
            error = traceback.format_exc()
            f = open("error_file.txt", "w+")
            f.write(error)
            w.fact_label.config(text="error recorded")
        except:
            print("keyboard interrupt")
            quit(0)

    
def check_alert(now):

    block = get_block(now)
    if now.strftime('%H:%M') == block.get_start(now).time().strftime('%H:%M'):
        w.background_color("red")

        if block.get_type() == 'before_school':
            w.alertLabel.config(text="It is Now Midnight", fg="white")
        elif block.get_type() == 'first':
            w.alertLabel.config(text="School in Session", fg="white")
        elif block.get_type() == 'normal':
            w.alertLabel.config(text="Block Ended", fg="white")
        elif block.get_type() == 'break':
            w.alertLabel.config(text="Block has Started", fg="white")
        elif block.get_type() == 'lunch':
            w.alertLabel.config(text="Lunch Started", fg="white")
        elif block.get_type() == 'after_school':
            w.alertLabel.config(text="School has Ended", fg="white")

    else:
        w.alertLabel.config(text="Block: {}".format(get_block(now)))
        w.background_color("grey25")
  

def is_school(block):
    if block.name == "before" or block.name == "after":
        return False
    return True

def does_file_exist(url):
    if os.path.isfile(url):
        return True
    else:
        return False


def tick(time1 = '', date1 = ''):
    global schedule_override

    now = datetime.now() #datetime object
    #now = datetime(now.year, now.month, 18, 15, 0, 1, 0)
    #now = datetime(now.year, now.month, 18, 11, 45, 1, 0)

    ############### Problem Zone ##################
    
    day = datetime.now().weekday()

    if does_file_exist('/tmp/flex') and schedule_override == None:
        schedule_override = 'f'
    elif does_file_exist('/tmp/normal') and schedule_override == None:
        schedule_override = 'n'
    elif not does_file_exist('/tmp/flex') and not does_file_exist('/tmp/normal') and parser.parse_args().schedule == None:
        schedule_override = None


    if (schedule_override == None and day == 2) or schedule_override == 'f':
        Read_Schedule(now, 'f')
    elif schedule_override == 'c':
        Read_Schedule(now, 'c')
    else:
        Read_Schedule(now)



    ############### Problem Zone ##################


    block = get_block(now)

    time_till_start = block.get_start(now) - now

    time_till_start = hours_minutes_seconds(time_till_start)
    time_till_end = block.get_end(now) - now

    time_till_end = hours_minutes_seconds(time_till_end)
    summer = datetime(now.year, 7, 1, 0, 0, 0, 0)
    if now > summer:
        summer = datetime(now.year+1, 7, 1, 0, 0, 0, 0)
    days_till_summer = summer - now
    days_till_summer = pretty_time_delta(days_till_summer.total_seconds())
    time2 = now.strftime('%H:%M:%S')
    date2 = now.strftime('%A, %B %d, %Y')

    #configure the clock gui
    w.clock.config(text=time2)
    #w.currentLabel.config(text = "Block: {}".format(block))
    w.date.config(text=date2)
    if block.get_type == 'break' or block.get_type == 'lunch':
        w.remainingLabel.config(text="Time Until Block Start:\n {}".format(time_till_end))
        w.time_till_summer.config(text="Summer Starts In:\n{}".format(days_till_summer))
    else:
        w.remainingLabel.config(text = "Time Until Block End:\n {}".format(time_till_end))
        w.time_till_summer.config(text ="Summer Starts In:\n{}".format(days_till_summer))

    #shoes time till summer if school is not in session
    if is_school(block):
        w.time_till_summer.config(fg = 'grey25')
        #w.time_till_summer.config(fg = 'white')
        w.time_till_summer.place(relx=.9, rely=0.85, anchor="n")
        w.remainingLabel.config(font = ('Helvetica', int(font_size/2), 'normal')) # default font/2
        w.remainingLabel.place(relx=.5, rely=.8, anchor="n")
    else:
        w.time_till_summer.place(relx=.6, rely=.6, anchor="n")
        w.time_till_summer.config(fg = 'white')
        w.remainingLabel.config(font = ('Helvetica', int(font_size/4), 'normal')) # default font/4
        w.remainingLabel.place(relx=.6, rely=.6, anchor="n")

    # check to see if an alert should be given
    # the screen is only red for one minute because it uses a shortened version of the current time (short_now),
    # which only has takes the current hours and minutes into account
    check_alert(now)
    w.clock.after(500, tick) #calls tick every 1 millisecond

set_joke()

# s = perpetualTimer(sched_set_joke, 679.8)
s = perpetualTimer(set_joke, 300)
s.start()
tick()
w.frame.mainloop()
