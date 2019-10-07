from time_util import *
import window as w
import time
from datetime import time, datetime
import argparse

message = "never gonna give you up"

parser = argparse.ArgumentParser(description = 'Control Elements of the Clock')
parser.add_argument('-f', '--font', type = int, default=100, dest='font', required = False, help = '-f multiply font size for clock elements by an int')
parser.add_argument('-s', '--schedule', type = str, default=None, dest='schedule', required = False, help = '-s change what schedule to use (n = normal schedule, f = flex schedule, c = custom schedule, w = weekend')
args = parser.parse_args()

font_size = parser.parse_args().font

schedule_override = parser.parse_args().schedule

def get_block(now):
    for x in range(len(blocks)-1):
        if blocks[x].is_current_block(now):
            return blocks[x]
    return blocks[-1]


#note to self: redo this whole function
def check_alert(now):

    day = now.weekday()

    #after this point, the method manually changes the alert message based on being between certain times and what day it is one. It is bad and must be fixed.
    block = get_block(now)
    #short_now = time(now.hour, now.minute, 0, 0) #just hour and minutes
    if now.strftime('%H:%M') == block.get_start(now).time().strftime('%H:%M'):
        w.background_color("red")

        if block.get_type() == 'before_school':
            w.alertLabel.config(text="It is Now Midnight", fg="white")
        elif block.get_type() == 'first':
            w.alertLabel.config(text="School in Session", fg="white")
        elif block.get_type() == 'normal':
            w.alertLabel.config(text="Block Started", fg="white")
        elif block.get_type() == 'break':
            w.alertLabel.config(text="Block has Ended", fg="white")
        elif block.get_label() == 'lunch':
            w.alertLabel.config(text="Lunch Started", fg="white")
        elif block.get_label() == 'after_school':
            w.alertLabel.config(text="School has Ended", fg="white")

    else:
        w.alertLabel.config(fg="grey25")
        w.background_color("grey25")
    # if (schedule_override == None and day >= 5) or schedule_override == 'w': #weekend
    #     pass
    # elif (schedule_override == None and day == 2) or schedule_override == 'f': #flex day
    #     if short_now == starts[1]: # first block started
    #         # print("School in Session")
    #         w.alertLabel.config(text="School in Session", fg="white")
    #         w.background_color("red")
    #     elif short_now == starts[3] or short_now == starts[5] or short_now == starts[7] or short_now == starts[9] or short_now == starts[11]: #normal block started
    #         # print("Block Started")
    #         w.alertLabel.config(text="Block Started", fg="white")
    #         w.background_color("red")
    #     elif short_now == ends[1] or short_now == ends[3] or short_now == ends[5] or short_now == ends[7] or short_now == ends[9]: #break started
    #         # print("Block has Ended")
    #         w.alertLabel.config(text="Block has Ended", fg="white")
    #         w.background_color("red")
    #     elif short_now == ends[11]: # home time has started
    #         # print("School has Ended")
    #         w.alertLabel.config(text="School has Ended", fg="white")
    #         w.background_color("red")
    #     else: # don't show alert
    #         w.alertLabel.config(fg = "grey25")
    #         w.background_color("grey25")
    # elif (schedule_override == None and not day == 2 and not day >= 5) or schedule_override == 'n': #normal school day
    #     if short_now == starts[1]:
    #         # print("School in Session")
    #         w.alertLabel.config(text="School in Session", fg="white")
    #         w.background_color("red")
    #     elif short_now == starts[3] or short_now == starts[5] or short_now == starts[7]:
    #         # print("Block Started")
    #         w.alertLabel.config(text="Block Started", fg="white")
    #         w.background_color("red")
    #     elif short_now == ends[1] or short_now == ends[3] or short_now == ends[5]:
    #         # print("Block has Ended")
    #         w.alertLabel.config(text="Block has Ended", fg="white")
    #         w.background_color("red")
    #     elif short_now == ends[7]:
    #         # print("School has Ended")
    #         w.alertLabel.config(text="School has Ended", fg="white")
    #         w.background_color("red")
    #     else:
    #         w.alertLabel.config(fg="grey25")
    #         w.background_color("grey25")
    #         #background_color("red")

def is_school(block):
    if block.name == "before" or block.name == "after":
        return False
    return True


def tick(time1 = '', date1 = ''):

    now = datetime.now() #datetime object

    ############### Problem Zone ##################
    day = datetime.now().weekday()
    if (schedule_override == None and day == 2) or schedule_override == 'f':
        Read_Schedule(day='f')
    elif schedule_override == 'c':
        Read_Schedule(day='c')
    else:
        Read_Schedule()

    ############### Problem Zone ##################

    #now = datetime(now.year, now.month, now.day, 10, 30, 1, 0)
    block = get_block(now)

    block_start = block.get_start(now)
    block_end = block.get_end(now)

    time_till_start = block_start - now
    #print(time_till_start)
    time_till_start = hours_minutes_seconds(time_till_start)
    time_till_end = block_end - now
    #print(time_till_end)
    time_till_end = hours_minutes_seconds(time_till_end)
    summer = datetime(now.year, 7, 1, 0, 0, 0, 0)
    if now > summer:
        summer = datetime(now.year+1, 7, 1, 0, 0, 0, 0)
    days_till_summer = summer - now
    days_till_summer = pretty_time_delta(days_till_summer.total_seconds())
    time2 = now.strftime('%H:%M:%S')
    date2 = now.strftime('%A, %B %d, %Y')

    if (time2 == '08:55:00'):
        Read_Schedule()

    #configure the clock gui
    w.clock.config(text=time2)
    w.currentLabel.config(text = "Block: {}".format(block))
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
        w.time_till_summer.place(relx=.85, rely=0.8, anchor="n")
        w.remainingLabel.config(font = ('Helvetica', int(font_size/2), 'normal')) # default font/2
        w.remainingLabel.place(relx=.5, rely=.75, anchor="n")
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

tick()
w.frame.mainloop()
