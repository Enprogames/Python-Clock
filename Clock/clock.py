from time_util import *
from window import *
import time
from datetime import time, datetime
import argparse

message = "never gonna give you up"

parser = argparse.ArgumentParser(description = 'Control the Font Size of the Clock')
parser.add_argument('-f', '--font', type = int, metavar = '', required = False, help = 'font size for clock elements')
args = parser.parse_args()

#font = args.font
# font = 100

def get_block(now):
    for x in range(len(blocks)-1):
        if blocks[x].is_current_block(now):
            return blocks[x]
    return blocks[-1]



def check_alert(now):

    #  weekdays
    #monday:    0
    #tuesday:   1
    #wednesday: 2
    #thursday:  3
    #friday:    4
    #saturday:  5
    #sunday:    6

    day = now.weekday()
    short_now = time(now.hour, now.minute, 0, 0)
    if day >= 5: #weekend
        print()
    elif day == 2: #flex day
        if short_now == starts[1]:
            # print("School in Session")
            alertLabel.config(text="School in Session", fg="white")
            background_color("red")
        elif short_now == starts[3] or short_now == starts[5] or short_now == starts[7] or short_now == starts[9] or short_now == starts[11]:
            # print("Block Started")
            alertLabel.config(text="Block Started", fg="white")
            background_color("red")
        elif short_now == ends[1] or short_now == ends[3] or short_now == ends[5] or short_now == ends[7] or short_now == ends[9]:
            # print("Block has Ended")
            alertLabel.config(text="Block has Ended", fg="white")
            background_color("red")
        elif short_now == ends[11]:
            # print("School has Ended")
            alertLabel.config(text="School has Ended", fg="white")
            background_color("red")
        else:
            alertLabel.config(fg = "grey25")
            background_color("grey25")
    else: #normal school day
        if short_now == starts[1]:
            # print("School in Session")
            alertLabel.config(text="School in Session", fg="white")
            background_color("red")
        elif short_now == starts[3] or short_now == starts[5] or short_now == starts[7]:
            # print("Block Started")
            alertLabel.config(text="Block Started", fg="white")
            background_color("red")
        elif short_now == ends[1] or short_now == ends[3] or short_now == ends[5]:
            # print("Block has Ended")
            alertLabel.config(text="Block has Ended", fg="white")
            background_color("red")
        elif short_now == ends[7]:
            # print("School has Ended")
            alertLabel.config(text="School has Ended", fg="white")
            background_color("red")
        else:
            alertLabel.config(fg="grey25")
            background_color("grey25")
            #background_color("red")

def is_school(block):
    if block.name == "before" or block.name == "after":
        return False
    return True


#Read_Schedule()
def tick(time1 = '', date1 = ''):

    now = datetime.now() #datetime object

    ############### Problem Zone ##################
    day = datetime.now().weekday()
    if day == 2:
        Read_Schedule('flex')
    Read_Schedule()
    ############### Problem Zone ##################

    #now = datetime(now.year, now.month, now.day, 15, 56, 0, 0)
    block = get_block(now)

    block_start = block.get_start(now)
    block_end = block.get_end(now)

    time_till_start = block_start - now
    #print(time_till_start)
    time_till_start = hours_minutes_seconds(time_till_start)
    time_till_end = block_end - now
    #print(time_till_end)
    time_till_end = hours_minutes_seconds(time_till_end)
    summer = datetime(2019, 7, 1, 0, 0, 0, 0)
    days_till_summer = summer - now
    days_till_summer = pretty_time_delta(days_till_summer.total_seconds())
    time2 = now.strftime('%H:%M:%S')
    date2 = now.strftime('%A, %B %d, %Y')

    if (time2 == '08:55:00'):
        Read_Schedule()

    #configure the clock gui
    clock.config(text=time2)
    currentLabel.config(text = "Block: {}".format(block))
    date.config(text=date2)
    if block.name == "Break 1" or block.name == "Lunch" or block.name == "Break 2":
        remainingLabel.config(text="Time Till Block Start:\n {}".format(time_till_end))
        time_till_summer.config(text="Summer Starts In:\n{}".format(days_till_summer))
    else:
        remainingLabel.config(text = "Time Till Block End:\n {}".format(time_till_end))
        time_till_summer.config(text ="Summer Starts In:\n{}".format(days_till_summer))

    #shoes time till summer if school is not in session
    if is_school(block):
        time_till_summer.config(fg = 'grey25')
        #time_till_summer.config(fg = 'white')
        time_till_summer.place(relx=.85, rely=0.8, anchor="n")
        remainingLabel.config(font = ('consolas', int(font/2), 'normal'))
        remainingLabel.place(relx=.5, rely=.7, anchor="n")
    else:
        time_till_summer.place(relx=.6, rely=.6, anchor="n")
        time_till_summer.config(fg = 'white')
        remainingLabel.config(font = ('consolas', int(font/4), 'normal'))
        remainingLabel.place(relx=.6, rely=.6, anchor="n")

    #check to see if an alert should be given
    check_alert(now)

    clock.after(500, tick) #calls tick every 1 millisecond

tick()
frame.mainloop()
