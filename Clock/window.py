import tkinter as tk

font_size = 100
font_type = "Comic Sans MS" # normal = Helvetica

def background_color(color):
    frame.config(bg=color)
    clock.config(bg=color)
    date.config(bg=color)
    alertLabel.config(bg=color)
    currentLabel.config(bg=color)
    remainingLabel.config(bg=color)
    time_till_summer.config(bg=color)


frame = tk.Tk()
frame.title('Digital Clock')
frame.attributes("-fullscreen", True) #change to True for final program
frame.configure(background = 'grey')

#clock widget
clock = tk.Label(frame, font = (font_type, int(font_size*1.5), 'bold italic'), #change font size to 200 for final program
                 bg = 'grey25', fg = 'white')
clock.place(relx=.5, rely=.5, anchor="center")

#date widget
date = tk.Label(frame, font = (font_type, int(font_size/2), 'normal'), bg = 'grey25', fg = 'white')
date.place(relx=.5, rely=.65, anchor="n")

#fact of the day label
fact_label = tk.Label(frame, font = (font_type, int(font_size/2), 'normal'), bg = 'grey25', fg = 'white')
fact_label.place(relx=.5, rely=.1, anchor="n")

#alert for sutdents to change classes
alertLabel = tk.Label(frame, text = 'Change Classes', font = (font_type, int(font_size/2), 'normal'), bg = 'grey25', fg = 'grey25')
alertLabel.grid(row=0, column = 1)

#current block
currentLabel = tk.Label(frame, text = "Block: ", font = (font_type, int(font_size/2), 'normal'), bg = 'grey25', fg = 'white')
currentLabel.place(relx=.50, rely=.05, anchor="n")

#time remaining till next class (location is set in tick method)
remainingLabel = tk.Label(frame, text = "time remaining: ", font = (font_type, int(font_size/2), 'normal'), bg = 'grey25', fg = 'white')
#remainingLabel.place(relx=.4, rely=.8, anchor="n")
time_till_summer = tk.Label(frame, font = (font_type, int(font_size/4), 'normal'), bg = 'grey25', fg = 'white')
#time_till_summer.place(relx=.6, rely=.6, anchor="n")

#configure the grid of the frame
frame.grid_rowconfigure(0, weight=2)
frame.grid_rowconfigure(2, weight=2)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(2, weight=1)