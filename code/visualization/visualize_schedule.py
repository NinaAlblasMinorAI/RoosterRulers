import numpy as np
from bokeh.io import curdoc
from bokeh.plotting import figure, save, output_file
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect, Text, HoverTool, DataTable, HTMLTemplateFormatter, TableColumn, LinearColorMapper, CategoricalColorMapper, CustomJS, TapTool
from bokeh.layouts import column, row
from bokeh.palettes import RdYlGn
import pandas as pd
from code.classes.lesson import Lesson
import itertools

def visualize_schedule(schedule_obj, output_file_path):

    output_file(output_file_path)
    
    schedule_obj.eval_schedule_objects()

    # create the plot on which we design the roster
    roster = Plot(width=2300, height=1580, title="ROOSTER RULERS' SCHEDULE")

    roster.add_tools(TapTool())

    # retrieve the dataframe of the schedule object
    schedule_df = schedule_obj.get_dataframe()

    # get the minimum and maximum malus points
    malus_points_df = schedule_df.applymap(lambda lesson_obj:lesson_obj.get_malus_points() if isinstance(lesson_obj, Lesson) else np.nan)
    min_malus_points = int(malus_points_df.min().min())
    max_malus_points = int(malus_points_df.max().max())

    nr_time_slots = 5
    number_of_rooms = len(schedule_obj.get_rooms()) # 7

    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # all_days = [day for day in days_of_the_week for time_slot in range(number_of_rooms * nr_time_slots)]
    total_time_slots = len(days_of_the_week) * nr_time_slots # 25

    x_values = np.tile(np.arange(number_of_rooms), total_time_slots)     # 0 1 2 3 4 5 6 0 1 2 3 4 5 6 ...
    y_values = np.repeat(np.arange(total_time_slots) + .25, number_of_rooms)   # 0.5 0.5 0.5 0.5 0.5 0.5 0.5 1.5 1.5 1.5 1.5 1.5 1.5 1.5 ...

    # dictionary of lists of the lesson attributes in the order the rectangles are created in
    lesson_dict = lesson_attributes(schedule_df)
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
    lesson_all_days = lesson_dict["Days"]

    # TODO: rename these variables
    todays_x, todays_y = remove_empty_slots(schedule_obj, x_values, y_values)

    # width and height of each lesson's visual representation (rectangle)
    width = np.full(len(todays_x), .98)
    height = np.full(len(todays_x), .95)

    # add one day's rectangles to roster
    rect_source = ColumnDataSource(data=dict(x=todays_x, 
                                        y=todays_y, 
                                        w=width, 
                                        h=height,
                                        types=lesson_types,
                                        group_nrs=lesson_group_nrs,
                                        nr_students=lesson_nr_students,
                                        conflict_points=lesson_mp_conflicts,
                                        gap_points=lesson_mp_gaps,
                                        capacity_points=lesson_mp_capacity,
                                        evening_points=lesson_mp_evening,
                                        days=lesson_all_days))

    rect_colormapper = CategoricalColorMapper(factors=["0", "1", "2", "3", "4"], palette=["lightcyan", "darkturquoise", "lightcyan", "darkturquoise", "lightcyan"])


    rectangles = Rect(x="x", y="y", width="w", height="h", fill_color={'field': 'days', 'transform': rect_colormapper})
    all_rectangles = roster.add_glyph(rect_source, rectangles)

    small_rect_source = ColumnDataSource(dict(x=todays_x + .4, 
                                        y=todays_y, 
                                        w=width / 7.1, 
                                        h=height / 1.75,
                                        points=lesson_malus_points,))

    # color the small rectangles
    small_rect_colormapper = LinearColorMapper(palette=RdYlGn[3], 
                                    low=min_malus_points, 
                                    high=max_malus_points)

    small_rectangles = Rect(x="x", y="y", width="w", height="h", fill_color={'field': 'points', 'transform': small_rect_colormapper})
    roster.add_glyph(small_rect_source, small_rectangles)

    # add course name text       # hier wil je niet de lege waarden uithalen want die maak ik al lege strings!
    text_source = ColumnDataSource(dict(x=x_values - .45, y=y_values + .35, text=lesson_names))
    lesson_text = Text(x="x", y="y", text="text")
    lesson_text.text_font_size = {'value': '13px'}
    roster.add_glyph(text_source, lesson_text)

    # add malus point text
    malus_points_text_source = ColumnDataSource(dict(x=todays_x + .37, y=todays_y + .1, text=lesson_malus_points))
    malus_points_text = Text(x="x", y="y", text="text")
    malus_points_text.text_font_size = {'value': '13px'}
    malus_points_text.text_font_style = {'value': 'bold'}
    roster.add_glyph(malus_points_text_source, malus_points_text)

    # create the students data table in bokeh
    html_formatter_name = HTMLTemplateFormatter(template="""
                        <div title="<%= name %>" style="font-size: 16px;">
                        <%= value %>
                        </div>
                    """)
    title_name = """<b style="font-size: 18px;">%s</b>""" % "name"

    html_formatter_course = HTMLTemplateFormatter(template="""
                        <div title="<%= course %>" style="font-size: 16px;">
                        <%= value %>
                        </div>
                    """)
    title_course = """<b style="font-size: 18px;">%s</b>""" % "course"

    columns = [
        TableColumn(field="name", title=title_name, formatter=html_formatter_name, width=210),
        TableColumn(field="course", title=title_course, formatter=html_formatter_course, width=340),
        ]

    student_source = ColumnDataSource(data=dict(name=[], course=[]))

    data_table = DataTable(source=student_source,
                            columns=columns,
                            height=1500,
                            autosize_mode="none")

    all_rectangles.selection_glyph = Rect(fill_color="deeppink")

    lesson_name_list = list(filter(lambda value: value !=  None, lesson_names))

    rect_source.selected.js_on_change('indices', CustomJS(
        args=dict(s1=student_source, 
                s2=lesson_students,
                s3=lesson_name_list), 
        code="""

            // manually selected index
            var inds = cb_obj.indices

            // retrieve the name of the manually selected lesson
            let selected_lesson_name = s3[inds[0]]

            // loop over all lesson names
            for (let lesson_name_index = 0; lesson_name_index < s3.length; lesson_name_index++) {

                // if this lesson is from the same course as the manually selected lesson
                if (s3[lesson_name_index] == selected_lesson_name && lesson_name_index != inds[0]) {

                    // add the index to the list of automatically selected indices
                    inds.push(lesson_name_index) // needs to be inds
                }
            }

            s1.data['name'] = []
            s1.data['course'] = []

            // TODO: skip lectures in adding? or check if name is already in there?

            // loop over all selected indices
            for (let i = 0; i < inds.length; i++) {

                let selected_index = inds[i]
                let lesson_students = s2[selected_index]
                let course = s3[selected_index]

                // loop over students in this lesson
                for (let j = 0; j < lesson_students.length; j++) {

                    // add student to the data table
                    let student = lesson_students[j]
                    s1.data['name'].push(student)
                    s1.data['course'].push(course)
                }
            }
            s1.change.emit()
        """)
    )





    # def print_selected_inds(attrname, old, new):
    #     # print(rect_source.selected.indices)
    #     pass

    # rect_source.selected.on_change("indices", print_selected_inds)

    # def country_select(attrname, old, new):
    #     rect_source.data = get_data(rect_source.selected.indices, country_dict)

    # rect_source.selected.on_change('indices')

    # students_source = ColumnDataSource(dict(
    #                                     dates=[i + 10 for i in range(10)],
    #                                     downloads=[i + 100 for i in range(10)],
    #                                 ))

    # print(dict(
    #             dates=[i + 10 for i in range(10)],
    #             downloads=[i + 100 for i in range(10)],
    #         ))

    # print(schedule_obj.get_student_name_dict())







    # hover tool that only works for the rectangles
    hover = HoverTool(renderers=[all_rectangles])
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
    xaxis = LinearAxis(axis_label="Rooms (capacity)")
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
    roster.yaxis[1].ticker = np.arange((nr_time_slots / 2), total_time_slots + (nr_time_slots / 2), len(days_of_the_week))
    roster.yaxis[1].major_label_overrides = {num : day_ticker_func(num) for num in np.arange((nr_time_slots / 2), total_time_slots + (nr_time_slots / 2), len(days_of_the_week))}

    roster.xaxis.axis_label_text_font_size = "15px"
    roster.xaxis.major_label_text_font_size = "15px"
    roster.yaxis.axis_label_text_font_size = "15px"
    roster.yaxis.major_label_text_font_size = "15px"

    layout = row(roster, data_table)

    curdoc().add_root(layout)

    # save the results
    save(curdoc())

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

    lessons_list = list(itertools.chain(*lessons_df.values.tolist()))

    # names
    lesson_names_list = list(map(lambda lesson_obj:lesson_obj.get_name() if isinstance(lesson_obj, Lesson) else None, lessons_list))
    attributes["Name"] = lesson_names_list
   
    # types
    lesson_types_list = list(map(lambda lesson_obj:lesson_obj.get_type() if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Type"] = list(filter(lambda value: value !=  "", lesson_types_list))

    # group numbers
    lesson_group_nrs_list = list(map(lambda lesson_obj:lesson_obj.get_group_nr() if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Group nr."] = list(filter(lambda value: value !=  "", lesson_group_nrs_list))

    # students
    lesson_students_list = list(map(lambda lesson_obj:lesson_obj.get_students() if isinstance(lesson_obj, Lesson) else "", lessons_list))     # df filled with lists of student objects
    lesson_student_names_list = list(map(lambda student_obj_list: list(map(lambda student: student.get_name(), student_obj_list)) if isinstance(student_obj_list, list) else "", lesson_students_list)) # lesson_students_list.applymap(lambda student_obj_list: list(map(lambda student: student.get_name(), student_obj_list)) if isinstance(student_obj_list, list) else "")
    attributes["Students"] = list(filter(lambda value: value !=  "", lesson_student_names_list))

    # nr of students
    lesson_nr_students_list = list(map(lambda lesson_obj:len(lesson_obj.get_students()) if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Nr. students"] = list(filter(lambda value: value !=  "", lesson_nr_students_list))

    # malus points
    lesson_points_list = list(map(lambda lesson_obj:lesson_obj.get_malus_points() if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Malus points"] = list(filter(lambda value: value !=  "", lesson_points_list))

    # conflicts
    mp_conflicts_list = list(map(lambda lesson_obj:lesson_obj.get_malus_points_dict()["conflicts"] if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["MP conflicts"] = list(filter(lambda value: value !=  "", mp_conflicts_list))

    # gaps
    mp_gaps_list = list(map(lambda lesson_obj:lesson_obj.get_malus_points_dict()["gaps"] if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["MP gaps"] = list(filter(lambda value: value !=  "", mp_gaps_list))

    # capacity
    mp_capacity_list = list(map(lambda lesson_obj:lesson_obj.get_malus_points_dict()["capacity"] if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["MP capacity"] = list(filter(lambda value: value !=  "", mp_capacity_list))

    # evening
    mp_evening_list = list(map(lambda lesson_obj:lesson_obj.get_malus_points_dict()["evening"] if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["MP evening"] = list(filter(lambda value: value !=  "", mp_evening_list))

    # days of the week
    days_list = list(map(lambda lesson_obj:str(lesson_obj.get_day()) if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Days"] = list(filter(lambda value: value !=  "", days_list))

    return attributes

def get_all_empty_slots(schedule_obj):

    unused_slots = [(row, column) for row, column in zip(*np.where(schedule_obj.get_dataframe().values == "-"))]

    return schedule_obj.get_empty_slots() + unused_slots

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
# Als je op student klikt: zie zijn rooster
# - ik denk dat ik OF JScode moet gebruiken OF een bokeh server
# - state maken van het rooster in z'n geheel, zodat je er altijd weer naartoe terug kunt. 
# - Dan van individuele roosters hele nieuwe states maken, die veranderen de 'value' als .selected
# - OF dan maken we de geselecteerde dingen een andere kleur!
# - OF we kleuren dan alle lessen die niet bij dit vak horen wit? Nee want ook tekst etc...

# Buitenste assen omdraaien

# alle code mooier schrijven + comments