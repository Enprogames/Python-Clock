import tkinter as tk
import datetime as dt
import os
import eel

from time_util import ScheduleHandler


ROOT_DIR = ''
if os.path.basename(os.getcwd()) == 'src':
    ROOT_DIR = ''
else:
    ROOT_DIR = 'src'
IMG_DIR = 'img'


class ClockFrameTk(tk.Frame):
    """
    A tkinter frame containing the clock content. It displays the following:
    - time
    - date
    - fact/joke
    - alert when event is beginning or ending
    - remaining time for the current event
    - optional time until summer
    """

    def __init__(self, parent, schedule_handler=None, fact_handler=None, background='#263238', foreground='white', width=600,
                 height=400, font='Arial', font_size=100, font_multiplier=1,
                 event_text='event', show_time=True, show_date=True, show_fact=True, show_alert=True,
                 show_remaining=True, show_summer=False, resize_dynamically=True, **kwargs):

        self.bg = background
        self.fg = foreground
        self.width = width
        self.height = height

        tk.Frame.__init__(self, parent, bg=self.bg, width=self.width, height=self.height)

        self.font = font
        self.font_size = font_size
        self.font_multiplier = font_multiplier
        self.event_text = event_text
        self.schedule_handler = schedule_handler
        self.fact_handler = fact_handler

        self.show_time = show_time
        self.show_date = show_date
        self.show_fact = show_fact
        self.show_alert = show_alert  # displays name of current event or whether it just ended
        self.show_remaining = show_remaining
        self.show_summer = show_summer

        self.widgets = []  # used to keep track of all widgets on the frame e.g. for changing their color

        self.digital_time_label = tk.Label(self, font=(self.font, int(font_size*1.5), 'bold'),  # change font size to 200 for final program
                                           bg=self.bg, fg=self.fg)
        self.widgets.append(self.digital_time_label)
        if show_time:
            self.digital_time_label.place(relx=.5, rely=.5, anchor='center')
        self.date_label = tk.Label(self, font=(self.font, int(font_size/2), 'normal'), bg=self.bg, fg=self.bg)
        self.widgets.append(self.date_label)
        if self.show_date:
            self.date_label.place(relx=.5, rely=.65, anchor="center")
        # fact (joke) of the day label
        self.fact_label = tk.Label(self, font=(self.font, int(font_size/4), 'normal'), bg=self.bg, fg=self.bg)
        self.widgets.append(self.fact_label)
        if self.show_fact:
            self.fact_label.place(relx=.5, rely=.1, anchor="n")
        self.last_fact_time = dt.datetime(1, 1, 1, 1, 1, 1)
        self.fact = ""

        self.alert_label = tk.Label(self, text='Error: Schedule data not found.', font=(self.font, int(font_size/2), 'bold'), bg=self.bg, fg=self.fg)
        self.current_alert = ""
        self.widgets.append(self.alert_label)
        if show_alert:
            self.alert_label.place(relx=.5, rely=.3, anchor='n')

        self.remaining_label = tk.Label(self, text="time remaining: ", font=(self.font, int(font_size/2), 'normal'), bg=self.bg, fg=self.fg)
        if self.show_remaining:
            self.remaining_label.place(relx=.5, rely=.8, anchor='s')
        self.widgets.append(self.remaining_label)
        self.time_till_summer_label = tk.Label(self, font=(self.font, int(font_size/4), 'normal'), bg=self.bg, fg=self.fg)
        if self.show_summer:
            self.time_till_summer_label.place(relx=.75, rely=.8, anchor='s')
        self.widgets.append(self.time_till_summer_label)

        if resize_dynamically:
            self.resize_dynamically()
            self.winfo_toplevel().bind("<Configure>", self.resize_dynamically)


    def set_fg(self, fg):
        self.fg = fg
        self.config(fg=fg)
        for w in self.widgets:
            w.config(fg=fg)

    def set_bg(self, bg):
        self.bg = bg
        self.config(bg=bg)
        for w in self.widgets:
            w.config(bg=bg)

    def set_font(self, font):
        self.font = font
        for w in self.widgets:
            current_font = w.cget("font")
            print(current_font)
            current_font[0] = font
            w.config(font=current_font)

    def resize_font(self, factor):
        self.font_multiplier = factor
        self.resize_dynamically()

    def set_font_size(self, font_size):
        self.font_size = font_size

        current_font = self.digital_time_label.cget("font").split(' ')
        current_font[1] = font_size*1.5
        self.digital_time_label.config(font=(current_font[0], int(current_font[1]), current_font[2]))

        current_font = self.date_label.cget("font").split(' ')
        current_font[1] = font_size/2
        self.date_label.config(font=(current_font[0], int(current_font[1]), current_font[2]))

        current_font = self.fact_label.cget("font").split(' ')
        current_font[1] = font_size/4
        self.fact_label.config(width=self.winfo_toplevel().winfo_width()-100, font=(current_font[0], int(current_font[1]), current_font[2]),
                               wraplength=self.fact_label.winfo_width())

        current_font = self.alert_label.cget("font").split(' ')
        current_font[1] = font_size/2
        self.alert_label.config(font=(current_font[0], int(current_font[1]), current_font[2]))

        current_font = self.remaining_label.cget("font").split(' ')
        current_font[1] = font_size/2
        self.remaining_label.config(font=(current_font[0], int(current_font[1]), current_font[2]))

        current_font = self.time_till_summer_label.cget("font").split(' ')
        current_font[1] = font_size/4
        self.time_till_summer_label.config(font=(current_font[0], int(current_font[1]), current_font[2]))

    def set_event_label(self, event_label):
        self.event_label = event_label

    def update_clock(self):
        now = dt.datetime.now()

        # update digital_time_label
        if self.show_clock:
            self.digital_time_label.config(fg=self.fg, text=now.strftime('%H:%M:%S'))
        else:
            self.digital_time_label.config(fg=self.bg)
        # update date_label
        if self.show_date:
            self.date_label.config(fg=self.fg, text=now.strftime('%A, %B %d, %Y'))
        else:
            self.date_label.config(fg=self.bg)
        # update fact_label if 60 seconds have passed since the last update
        if self.show_fact and self.fact_handler:
            if (now - self.last_fact_time).seconds > 60:
                self.fact = self.fact_handler.get()
            self.last_fact_time = dt.datetime.now()
            self.fact_label.config(fg=self.fg, text=self.fact)
        else:
            self.fact_label.config(fg=self.bg)

        # display the name of the current event
        if self.show_alert and self.schedule_handler:
            self.alert_label.config(fg=self.fg, text=self.schedule_handler.get_current_events_str())
        else:
            self.alert_label.config(fg=self.bg)

        # update remaining_label with time remaining until next event or event end
        if self.show_remaining and self.schedule_handler:
            self.remaining_label.config(fg=self.fg, text=self.schedule_handler.get_remaining_str_verbose())
        else:
            self.remaining_label.config(fg=self.bg)

        # update again in half a second
        self.current_task = self.winfo_toplevel().after(500, self.update_clock)

    def start(self):
        """
        Start displaying the current time, current date, time until event ends or until next event, and current event
        """
        self.update_clock()

    def stop(self):
        """
        End the updating of the clock by stopping and deleting the currently scheduled update task
        """
        self.winfo_toplevel().after_cancel(self.current_task)
        self.current_task = None

    def show_clock(self):
        pass

    def hide_clock(self):
        pass

    def show_date(self):
        pass

    def hide_date(self):
        pass

    def show_fact(self):
        pass

    def hide_fact(self):
        pass

    def show_alert(self):
        pass

    def hide_alert(self):
        pass

    def show_remaining(self):
        self.remaining_label = True
        self.remaining_label.place(relx=.4, rely=.8, anchor='n')

    def hide_remaining(self):
        self.show_remaining = False
        self.remaining_label.place_forget()

    def show_summer(self):
        self.show_summer = True
        self.time_till_summer_label.place(relx=.6, rely=.6, anchor='n')

    def hide_summer(self):
        self.show_summer = False
        self.time_till_summer_label.place_forget()

    def resize_dynamically(self, event=None):
        self.winfo_toplevel().update_idletasks()
        self.set_font_size((self.winfo_width()/20)*self.font_multiplier)


class GUIWindowTk(tk.Tk):
    """
    Main window for the whole program. Contains the clock frame.
    In the future, it may also have a settings frame.

    :param icon_file:
        Filename for window icon. This will be searched for in the IMG_DIR directory (e.g. src/img/clock_icon.png)
    :type icon_file: ``str``
    ...

    :param \**kwargs:
        See below

    :Keyword Arguments:
        * *foreground* (``str``) --
          Foreground color of frame e.g. 'black' or '#363238'
        * *background* (``str``) --
          Additional content
        ...
    """

    def __init__(self, icon_file='clock_icon.png', schedule_handler=None,
                 fact_handler=None, **kwargs):
        tk.Tk.__init__(self)
        self.bg = kwargs.get('background', '#263238')
        self.fg = kwargs.get('foreground', 'white')
        self.fullscreen = kwargs.get('fullscreen', False)
        self.frames = []

        self.title('Digital Clock')
        self.configure(bg=self.bg)
        self.iconphoto(False, tk.PhotoImage(file=os.path.join(ROOT_DIR, IMG_DIR, icon_file)))
        if self.fullscreen:
            self.attributes("-fullscreen", True)  # change to True for final program
        else:
            self.geometry("600x400")

        self.update_idletasks()
        self.clock_frame = ClockFrameTk(self, schedule_handler=schedule_handler, fact_handler=fact_handler, **kwargs)
        self.clock_frame.pack(fill="both", expand=True)
        self.frames.append(self.clock_frame)

    def set_bg(self, bg):
        self.bg = bg
        for f in self.frames:
            f.set_bg(bg)

    def set_fg(self, fg):
        self.fg = fg
        for f in self.frames:
            f.set_fg(fg)

    def set_font(self, font):
        for f in self.frames:
            f.set_font(font)

    def set_event_label(self, label):
        self.clock_frame.set_event_label(label)

    def start_clock(self):
        self.clock_frame.start()

    def stop_clock(self):
        self.clock_frame.stop()


class GUIWindowEel:
    """
    A clock window created using the eel gui framework
    """
    def __init__(self):
        eel.init()


class MainWindow:
    """

    """

    def __init__(self, window_manager='tkinter', schedule_handler=None, fact_handler=None, **kwargs):
        self.window = None
        if window_manager == 'tkinter' or window_manager == 'tk':
            self.handler = GUIWindowTk(schedule_handler=schedule_handler, fact_handler=fact_handler, **kwargs)
        elif window_manager == 'eel':
            pass  # eel hasn't been implemented yet :(

    def start_clock(self):
        self.handler.start_clock()

    def stop_clock(self):
        self.handler.stop_clock()

    def mainloop(self):
        self.start_clock()
        self.handler.mainloop()

    def set_fg(self, fg):
        self.handler.set_fg(fg)

    def set_bg(self, bg):
        self.handler.set_bg(bg)

    def set_font(self, font):
        self.handler.set_font(font)

    def set_event_label(self, label):
        self.handler.set_event_label(label)
