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
    
    schedule_obj.eval_schedule_objects()

    # create the plot on which we design the roster
    roster = Plot(width=2000, height=2000)

    # retrieve the dataframe of the schedule object
    schedule_df = schedule_obj.get_dataframe()

    number_of_rooms = len(schedule_obj.get_rooms())

    # TODO: niet hardcoden?
    number_of_days = 5
    time_slots_per_day = 5

    total_time_slots = number_of_days * time_slots_per_day # 25

    # width and height of each lesson's visual representation (rectangle)
    width = np.full(number_of_rooms * time_slots_per_day, .95) # 35
    height = np.full(number_of_rooms * time_slots_per_day, .8) # 35

    x_values = np.tile(np.arange(7), 5)     # 0 1 2 3 4 5 6 0 1 2 3 4 5 6 ...
    y_values = np.repeat(np.arange(5) + .5, 7)   # 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5 ...

    # loop over the days
    for i in range(0, total_time_slots, time_slots_per_day):

        # one day's lessons     
        lessons_df = schedule_df.iloc[i:i+5]

        # dictionary of lists of the lesson attributes in the order the rectangles are created in
        lesson_dict = lesson_attributes(lessons_df)
        lesson_names = lesson_dict["Name"]
        lesson_types = lesson_dict["Type"]
        lesson_group_nrs = lesson_dict["Group nr."]
        lesson_nr_students = lesson_dict["Nr. students"]
        lesson_malus_points = lesson_dict["Malus points"]

        # add one day's rectangles to roster
        rect_source = ColumnDataSource(dict(x=x_values, 
                                            y=y_values + i, 
                                            w=width, 
                                            h=height,
                                            types=lesson_types,
                                            group_nrs=lesson_group_nrs,
                                            nr_students=lesson_nr_students,
                                            points=lesson_malus_points))

        rectangles = Rect(x="x", y="y", width="w", height="h", fill_color=color_of_the_day(i))
        roster.add_glyph(rect_source, rectangles)

        # create arrays for the text's x and y coordinates to make sure the text aligns nicely with rectangles
        text_x_values = x_values - .45
        text_y_values = y_values + i + .1

        # add text
        text_source = ColumnDataSource(dict(x=text_x_values, y=text_y_values, text=lesson_names))
        lesson_text = Text(x="x", y="y", text="text")
        lesson_text.text_font_size = {'value': '11px'}
        roster.add_glyph(text_source, lesson_text)

        # TODO: ??? weghalen
        hover = HoverTool()
        hover.tooltips = """
            <div>
                <div><strong>Type: </strong>@types</div>
                <div><strong>Group nr.: </strong>@group_nrs</div>
                <div><strong>Nr. of students: </strong>@nr_students</div>
                <div><strong>Malus points: </strong>@points</div>
            </div>
        """

        roster.add_tools(hover)
        
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

    # save the results
    save(roster)

def color_of_the_day(day_index):
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
    
    tick_to_day_dict = {2.5: "Monday", 7.5: "Tuesday", 12.5: "Wednesday", 17.5: "Thursday", 22.5: "Friday"}

    return tick_to_day_dict[tick_value]

def lesson_attributes(lessons_df):
    """
    Returns dictionary of the lesson attributes,
    e.g. {"Name" : [name1, name2, ...], "Type": [type1, type2, ...], ...}
    """

    attributes = {}

    lesson_names_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_name() if isinstance(lesson_obj, Lesson) else None)
    attributes["Name"] = list(itertools.chain(*lesson_names_df.values.tolist()))
   
    lesson_types_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_type() if isinstance(lesson_obj, Lesson) else "")
    attributes["Type"] = list(itertools.chain(*lesson_types_df.values.tolist()))

    lesson_group_nrs_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_group_nr() if isinstance(lesson_obj, Lesson) else "")
    attributes["Group nr."] = list(itertools.chain(*lesson_group_nrs_df.values.tolist()))

    lesson_students_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_students() if isinstance(lesson_obj, Lesson) else "")
    attributes["Students"] = list(itertools.chain(*lesson_students_df.values.tolist()))

    lesson_nr_students_df = lessons_df.applymap(lambda lesson_obj:len(lesson_obj.get_students()) if isinstance(lesson_obj, Lesson) else "")
    attributes["Nr. students"] = list(itertools.chain(*lesson_nr_students_df.values.tolist()))

    lesson_points_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points() if isinstance(lesson_obj, Lesson) else "")
    attributes["Malus points"] = list(itertools.chain(*lesson_points_df.values.tolist()))

    return attributes

### TODO
# - ook nog welke studenten in hovertool?
# - (selection tool voor individuele roosters)
# - Interactieve kostenplot
# - zorgen dat er geen rectangle komt als er geen tekst in staat 
# (wss als je in de CDS die waarden gewoon verwijdert)
# (of toch een dubbele for-loop...)
