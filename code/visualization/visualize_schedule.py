import numpy as np
from bokeh.plotting import figure, show, save, output_file
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect, Text, HoverTool, Ticker
import pandas as pd
from code.classes.schedule import Schedule
from code.classes.lesson import Lesson
import itertools

def visualize_schedule(schedule_obj, output_file_path):

    output_file(output_file_path)

    # create the plot on which we design the roster
    roster = Plot(width=2000, height=2000)

    # retrieve the dataframe of the schedule object
    schedule_df = schedule_obj.get_dataframe()

    number_of_rooms = len(schedule_obj.get_rooms())

    # width and height of each lesson's visual representation (rectangle)               # TODO: niet hardcoden?
    w = np.full(35, .95)
    h = np.full(35, .8)

    # TODO: niet hardcoden?
    number_of_days = 5
    time_slots_per_day = 5
    total_time_slots = number_of_days * time_slots_per_day # 25

    x_values = np.tile(np.arange(7), 5)     # 0 1 2 3 4 5 6 0 1 2 3 4 5 6 ...
    y_values = np.repeat(np.arange(5) + .5, 7)   # 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5 ...

    # loop over the days        # TODO: niet hardcoden?
    for i in range(0, 25, 5):

        # monday = x_values & y_values[0:5]
        # tuesday = x_values & y_values [5:10]

        # add one day's rectangles to roster
        rect_source = ColumnDataSource(dict(x=x_values, y=y_values + i, w=w, h=h))
        rectangles = Rect(x="x", y="y", width="w", height="h", fill_color=color_pick(day_index=i))
        roster.add_glyph(rect_source, rectangles)

        # create arrays for the text's x and y coordinates to make sure the text aligns nicely with rectangles
        text_x_values = x_values - .45
        text_y_values = y_values + i + .1

        # one day's courses                         # monday_courses = df[0:5, :].flatten()
        lessons = schedule_df.iloc[i:i+5]
        lesson_names = lessons.applymap(lambda lesson_obj:lesson_obj.get_name() if isinstance(lesson_obj, Lesson) else "")
        lesson_names = list(itertools.chain(*lesson_names.values.tolist()))

        # TODO: zorgen dat er geen rectangle komt als er geen tekst in staat

        # add text
        text_source = ColumnDataSource(dict(x=text_x_values, y=text_y_values, text=lesson_names))
        lesson_text = Text(x="x", y="y", text="text")
        lesson_text.text_font_size = {'value': '11px'}
        roster.add_glyph(text_source, lesson_text)
        
    # add x and y axis - ???
    xaxis = LinearAxis(axis_label="Rooms")
    roster.add_layout(xaxis, 'above')
    yaxis = LinearAxis(axis_label='Time slots')
    roster.add_layout(yaxis, 'left')
    yaxis2 = LinearAxis(axis_label='Days')
    roster.add_layout(yaxis2, 'left')

    # ???
    roster.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    roster.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    roster.add_layout(Grid(dimension=1, ticker=yaxis2.ticker))

    # create room tick labels
    roster.xaxis.major_label_overrides = dict(zip(range(7), [str(elem) for elem in schedule_obj.get_rooms()]))
    roster.xaxis.minor_tick_line_color = None

    # make sure we start at 0 in the upper left corner
    roster.y_range.flipped = True 

    # create time tick labels (0 up to and including 25, to get a "19:00" tick)         
    roster.yaxis[0].ticker = np.arange(total_time_slots + 1)
    roster.yaxis[0].major_label_overrides = {num : time_ticker_func(num) for num in range(total_time_slots + 1)}

    # create day tick labels (starting at 2.5 with steps of 5, to get ticks halfway through each day)
    roster.yaxis[1].ticker = np.arange((time_slots_per_day / 2), total_time_slots + (time_slots_per_day / 2), number_of_days)
    roster.yaxis[1].major_label_overrides = {num : day_ticker_func(num) for num in np.arange((time_slots_per_day / 2), total_time_slots + (time_slots_per_day / 2), number_of_days)}

    # TODO: de lesson waarden achterhalen -> df maken met type, group, students en malus points?
    # laad de rooms in en sla ze op in een dict. Deze omzetten in df.
    # lekker hoveren 
    hover = HoverTool()
    hover.tooltips = """
        <div>
            <div><strong>Type: </strong>Lab</div>
            <div><strong>Group: </strong>3</div>
            <div><strong>Students: </strong>18</div>
            <div><strong>Malus points: </strong>454</div>
        </div>
    """

    roster.add_tools(hover)

    # show the results
    save(roster)

def color_pick(day_index):
    """
    Takes the day index (Monday = 0, Tuesday = 5, Wednesday = 10, Thursday = 15, Friday = 20) and
    returns one of two colors, in order to distinguish the days from each other in the schedule.
    """
    
    if day_index % 2 == 0:
        return "lavenderblush"
    
    return "pink"

def time_ticker_func(tick_value):
    """
    Takes the tick value and returns the corresponding time.
    """
    
    if tick_value == 25:
        return "19:00"
    elif tick_value % 5 == 1:
        return "11:00"
    elif tick_value % 5 == 2:
        return "13:00"
    elif tick_value % 5 == 3:
        return "15:00"
    elif tick_value % 5 == 4:
        return "17:00"
    else:
        return "09:00"
    
def day_ticker_func(tick_value):
    """
    Takes the tick_value and returns the corresponding day.
    """
    
    # TODO: magic numbers weg
    tick_to_day = {2.5: "Monday", 7.5: "Tuesday", 12.5: "Wednesday", 17.5: "Thursday", 22.5: "Friday"}
    
    return tick_to_day[tick_value]







### TODO
# - lesson info achterhalen uit bestaande code -> implementeren in hovertool
# - ook nog welke studenten in hovertool?
# - (selection tool voor individuele roosters)
# - Interactieve kostenplot
