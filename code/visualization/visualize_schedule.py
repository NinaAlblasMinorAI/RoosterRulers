import numpy as np
from bokeh.plotting import figure, show, save, output_file
from bokeh.io import output_notebook
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect, Text, HoverTool, Ticker
import pandas as pd
from code.classes.schedule import Schedule
from code.classes.lesson import Lesson
from code.classes.student import Student
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

    x_values = np.tile(np.arange(7), 5)     # 0 1 2 3 4 5 6 0 1 2 3 4 5 6 ...
    y_values = np.repeat(np.arange(5) + .25, 7)   # 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5 ...

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
        lesson_students = lesson_dict["Students"]
        lesson_malus_points = lesson_dict["Malus points"]
        lesson_mp_conflicts = lesson_dict["MP conflicts"]
        lesson_mp_gaps = lesson_dict["MP gaps"]
        lesson_mp_capacity = lesson_dict["MP capacity"]
        lesson_mp_evening = lesson_dict["MP evening"]

        todays_x, todays_y = remove_empty_slots(schedule_obj, x_values, y_values + i)

        # width and height of each lesson's visual representation (rectangle)
        width = np.full(len(todays_x), .95)
        height = np.full(len(todays_x), .8)

        # add one day's rectangles to roster
        rect_source = ColumnDataSource(dict(x=todays_x, 
                                            y=todays_y, 
                                            w=width, 
                                            h=height,
                                            types=lesson_types,
                                            group_nrs=lesson_group_nrs,
                                            nr_students=lesson_nr_students,
                                            conflict_points=lesson_mp_conflicts,
                                            gap_points=lesson_mp_gaps,
                                            capacity_points=lesson_mp_capacity,
                                            evening_points=lesson_mp_evening))

        rectangles = Rect(x="x", y="y", width="w", height="h", fill_color=color_of_the_day(i))
        roster.add_glyph(rect_source, rectangles)

        small_rect_source = ColumnDataSource(dict(x=todays_x + .38, 
                                            y=todays_y, 
                                            w=width / 7, 
                                            h=height / 1.75,
                                            points=lesson_malus_points,))

        small_rectangles = Rect(x="x", y="y", width="w", height="h", fill_color="white")
        roster.add_glyph(small_rect_source, small_rectangles)

        # add course name text       # hier wil je niet de lege waarden uithalen want die maak ik al lege strings!
        text_source = ColumnDataSource(dict(x=x_values - .45, y=y_values + i + .35, text=lesson_names))
        lesson_text = Text(x="x", y="y", text="text")
        lesson_text.text_font_size = {'value': '11px'}
        roster.add_glyph(text_source, lesson_text)

        # add malus point text
        malus_points_text_source = ColumnDataSource(dict(x=todays_x + .34, y=todays_y + .1, text=lesson_malus_points))
        malus_points_text = Text(x="x", y="y", text="text")
        malus_points_text.text_font_size = {'value': '11px'}
        roster.add_glyph(malus_points_text_source, malus_points_text)

        hover = HoverTool()
        hover.tooltips = """
            <div>
                <div><strong>Type: </strong>@types</div>
                <div><strong>Group nr.: </strong>@group_nrs</div>
                <div><strong>Nr. of students: </strong>@nr_students</div>

                <div><br><strong>Conflict pts: </strong>@conflict_points</div>
                <div><strong>Gap pts: </strong>@gap_points</div>
                <div><strong>Capacity pts: </strong>@capacity_points</div>
                <div><strong>Evening slot pts: </strong>@evening_points</div>
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
        return "darkturquoise"
    
    return "lightcyan"

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

    # names
    lesson_names_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_name() if isinstance(lesson_obj, Lesson) else None)
    attributes["Name"] = list(itertools.chain(*lesson_names_df.values.tolist()))
   
    # types
    lesson_types_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_type() if isinstance(lesson_obj, Lesson) else "")
    lesson_types_list = list(itertools.chain(*lesson_types_df.values.tolist()))
    attributes["Type"] = list(filter(lambda value: value !=  "", lesson_types_list))

    # group numbers
    lesson_group_nrs_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_group_nr() if isinstance(lesson_obj, Lesson) else "")
    lesson_group_nrs_list = list(itertools.chain(*lesson_group_nrs_df.values.tolist()))
    attributes["Group nr."] = list(filter(lambda value: value !=  "", lesson_group_nrs_list))

    # students
    lesson_students_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_students() if isinstance(lesson_obj, Lesson) else "")     # df filled with lists of student objects
    lesson_student_names_df = lesson_students_df.applymap(lambda student_obj_list: list(map(lambda student: student.get_name(), student_obj_list)) if isinstance(student_obj_list, list) else "")
    lesson_student_names_list = list(itertools.chain(*lesson_student_names_df.values.tolist()))
    attributes["Students"] = list(filter(lambda value: value !=  "", lesson_student_names_list))

    # nr of students
    lesson_nr_students_df = lessons_df.applymap(lambda lesson_obj:len(lesson_obj.get_students()) if isinstance(lesson_obj, Lesson) else "")
    lesson_nr_students_list = list(itertools.chain(*lesson_nr_students_df.values.tolist()))
    attributes["Nr. students"] = list(filter(lambda value: value !=  "", lesson_nr_students_list))

    # malus points
    lesson_points_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points() if isinstance(lesson_obj, Lesson) else "")
    lesson_points_list = list(itertools.chain(*lesson_points_df.values.tolist()))
    attributes["Malus points"] = list(filter(lambda value: value !=  "", lesson_points_list))

    # conflicts
    mp_conflicts_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points_dict()["conflicts"] if isinstance(lesson_obj, Lesson) else "")
    mp_conflicts_list = list(itertools.chain(*mp_conflicts_df.values.tolist()))
    attributes["MP conflicts"] = list(filter(lambda value: value !=  "", mp_conflicts_list))

    # gaps
    mp_gaps_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points_dict()["gaps"] if isinstance(lesson_obj, Lesson) else "")
    mp_gaps_list = list(itertools.chain(*mp_gaps_df.values.tolist()))
    attributes["MP gaps"] = list(filter(lambda value: value !=  "", mp_gaps_list))

    # capacity
    mp_capacity_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points_dict()["capacity"] if isinstance(lesson_obj, Lesson) else "")
    mp_capacity_list = list(itertools.chain(*mp_capacity_df.values.tolist()))
    attributes["MP capacity"] = list(filter(lambda value: value !=  "", mp_capacity_list))

    # evening
    mp_evening_df = lessons_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points_dict()["evening"] if isinstance(lesson_obj, Lesson) else "")
    mp_evening_list = list(itertools.chain(*mp_evening_df.values.tolist()))
    attributes["MP evening"] = list(filter(lambda value: value !=  "", mp_evening_list))

    return attributes

def get_all_empty_slots(schedule_obj):

    unused_slots = [(row, column) for row, column in zip(*np.where(schedule_obj.get_dataframe().values == "-"))]

    return schedule_obj.get_empty_slots() + unused_slots

# def get_student_names(stud_obj_list):


def remove_empty_slots(schedule_obj, x_vals, y_vals):
    empty_slots = get_all_empty_slots(schedule_obj)

    i = x_vals.size - 1

    for (y, x) in list(zip(y_vals - .25, x_vals))[::-1]:
        if (y, x) in empty_slots:
            x_vals = np.delete(x_vals, i)
            y_vals = np.delete(y_vals, i)

        i -= 1

    return x_vals, y_vals + .25


### TODO
# - als je op les klikt: zie alle lessen van dit vak
# - als je op les klikt: zie alle studenten van deze les
# - als je op student klikt: zie zijn rooster
# - ??? weghalen -> Hover tools alleen toevoegen aan rectangles
# - Hover: specifieren van maluspunten -> DONE
# - Buitenste assen omdraaien
# - Rood en groene vakjes?
# - lesson_attributes() mooier?
# - plot shape niet vierkant

# - Pushen