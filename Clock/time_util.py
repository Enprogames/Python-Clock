from datetime import time, date, datetime, timedelta
import csv
#import platform

global blocks
blocks = [] # an array of block objects
startsstring = []
endsstring   = []
starts = [] # an array of starting times for the blocks
ends   = [] # an array of ending times for the blocks
nowTotalSeconds = 0
current_block = ''
time_till_next = 0
block_delta = 0
file_path = "/home/pi/Python-Clock/Clock/sched.csv"
#file_path = 'sched.csv'
# try:
#     dist_name = platform.dist()[0]
# except:
#     pass

class Block:

    def __init__(self, start, end, name, block_type):
        self.start = start
        self.end = end
        self.name = name
        self.block_type = block_type # types of blocks: before_school, first, normal, break, lunch, after_school

    def __str__(self):
        return self.name

    def is_current_block(self, now):
        now = now.time()

        if self.start < now < self.end:
            return True
        return False

    def get_start(self, now):
        start_dt = datetime(now.year, now.month, now.day, self.start.hour, self.start.minute, self.start.second, self.start.microsecond)
        return start_dt

    def get_end(self, now):
        end_dt = datetime(now.year, now.month, now.day, self.end.hour, self.end.minute, self.end.second, self.end.microsecond)
        return end_dt
    def get_type(self):
        return self.block_type
    
def totalSeconds(x):
    hour = x.hour * 3600
    minutes = x.minute * 60
    seconds = x.second
    nowTotal = hour + minutes + seconds
    return nowTotal

def hours_minutes_seconds(td): #hide hours if it equals 0, minutes and seconds always 2 digits
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

def Read_Schedule(now, day = "n"):

    #global blocks
    del blocks[:]

    num_lines = sum(1 for _ in open(file_path))
    custom_length = num_lines - 24 #length of the custom schedule
    with open(file_path, 'r') as file:
        #days of week
        #0 = monday, 1 = tuesday, 2 = wednesday, 3 = thursday, 4 = friday, 5 = saturday, 6 = sunday
        reader = csv.reader(file)
        count = 0 #iteration count for loop

        next(reader) #skips the instructional line in the csv file

        if day == 'f':
            duration = 11
            for i in range(9):
                next(reader)
                
        elif day == 'c':
            duration = custom_length - 2 #length of the custom schedule minus the before and after school times
            for i in range(23):
                next(reader)
            
        else:
            duration = 7 #how many blocks are in the day not including before and after school
        

        #Note to self: Redo everything after this point
        if len(blocks) - 1 < duration: # does not run because blocks is not reset
            for line in reader:
                startsstring.append(line[1])
                endsstring.append(line[2])

                # a horrible way to create a datetime object. these variables are used to split up the starting and ending
                # times (which are in the form of strings) into lists ([hours, minutes, seconds]). At least 2 steps
                # of this process could be cut out
                listS = startsstring[count].split(':')
                listE = endsstring[count].split(':')

                for i in range(len(listS)):
                    listS[i] = int(listS[i])
                num = time(listS[0], listS[1], listS[2])
                starts.append(num)

                for i in range(len(listE)):
                    listE[i] = int(listE[i])
                num = time(listE[0], listE[1], listE[2])
                ends.append(num)

                if now.weekday() == 4: # friday end blocks 5 minutes early.
                    
                    #blocks will be ended 5 minutes early by subtracting 5 minutes from the end of each block 
                    # and subtracting 5 minutes from the start of each break/lunch

                    if count == 1: # first block

                        endminus5minutes = datetime.combine(date.today(), (starts[count])) - datetime.combine(date.today(), time(0,5,0))
                        endminus5minutes = (datetime.min+endminus5minutes).time()
                        blocks.append(Block(starts[count], endminus5minutes, line[0], 'first'))

                    elif line[0][0:5].lower() == 'break':

                        startminus5minutes = datetime.combine(date.today(), (starts[count])) - datetime.combine(date.today(), time(0,5,0))
                        startminus5minutes = (datetime.min+startminus5minutes).time()
                        blocks.append(Block(startminus5minutes, ends[count], line[0], 'break'))

                    elif line[0][0:5].lower() == 'lunch': # (break)

                        startminus5minutes = datetime.combine(date.today(), (starts[count])) - datetime.combine(date.today(), time(0,5,0))
                        startminus5minutes = (datetime.min+startminus5minutes).time()
                        blocks.append(Block(startminus5minutes, ends[count], line[0], 'lunch'))

                    elif count == 0: # before school (doesn't need to be changed)

                        blocks.append(Block(starts[count], ends[count], line[0], 'before_school'))

                    elif count == duration + 1: # working (break)

                        startminus5minutes = datetime.combine(date.today(), (starts[count])) - datetime.combine(date.today(), time(0,5,0))
                        startminus5minutes = (datetime.min+startminus5minutes).time()
                        blocks.append(Block(startminus5minutes, ends[count], line[0], 'after_school'))

                    elif count == duration: # working

                        startminus5minutes = datetime.combine(date.today(), (ends[count])) - datetime.combine(date.today(), time(0,5,0))
                        startminus5minutes = (datetime.min+startminus5minutes).time()
                        blocks.append(Block(starts[count], startminus5minutes, line[0], 'last'))
                        
                    else:
                        blocks.append(Block(starts[count], ends[count], line[0], 'normal'))
                else: # not friday

                    if count == 1:
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'first'))

                    elif line[0][0:5].lower() == 'break':
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'break'))

                    elif line[0][0:5].lower() == 'lunch':
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'lunch'))

                    elif count == 0:
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'before_school'))

                    elif count == duration + 1:
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'after_school'))

                    elif count == duration:
                        
                        blocks.append(Block(starts[count], ends[count], line[0], 'last'))
                        
                    else:
                        blocks.append(Block(starts[count], ends[count], line[0], 'normal'))
                    

                if count > duration:
                    break
                count += 1

    #print(len(blocks))
                
        #blocks.append(Block(time(),time(),"Break"))

        #for x in range(len(blocks)):
        #    print(blocks[x].name, blocks[x].start, blocks[x].end)
        #print(str(blocks))


