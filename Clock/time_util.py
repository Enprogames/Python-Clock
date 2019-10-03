from datetime import time, date, datetime
import csv

blocks = [] # an array of block objects
startsstring = []
endsstring   = []
starts = [] # an array of starting times for the blocks
ends   = [] # an array of ending times for the blocks
nowTotalSeconds = 0
current_block = ''
time_till_next = 0
block_delta = 0
file_path = "E:\e_pos\Documents\School\Grade 12\Hackerspace\Python-Clock-master\Clock\sched.csv"

class Block:

    def __init__(self, start, end, name):
        self.start = start
        self.end = end
        self.name = name

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

def Read_Schedule(day = "n"):
    num_lines = sum(1 for line in open(file_path))
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

            #print(starts[count], ends[count], line[0])
            if not line[0][0] == 'F':
                blocks.append(Block(starts[count], ends[count], line[0]))
            else:
                blocks.append(Block(starts[count], ends[count], line[0]))

            if count > duration:
                break
            count += 1
            
        #blocks.append(Block(time(),time(),"Break"))

        #for x in range(len(blocks)):
        #    print(blocks[x].name, blocks[x].start, blocks[x].end)
        #print(str(blocks))


