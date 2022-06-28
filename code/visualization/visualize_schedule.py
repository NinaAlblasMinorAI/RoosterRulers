from attr import attr
from code.classes.lesson import Lesson
import numpy as np
import pandas as pd
import itertools
from bokeh.io import curdoc
from bokeh.plotting import save, output_file
from bokeh.models import ColumnDataSource, Grid, LinearAxis, Plot, Rect, Text
from bokeh.models import HoverTool, DataTable, HTMLTemplateFormatter
from bokeh.models import LinearColorMapper, CustomJS, TableColumn, TapTool
from bokeh.layouts import row
from bokeh.palettes import RdYlGn


def visualize_schedule(schedule_obj, output_file_path):
    """
    Takes a Schedule instance and visualizes it into 
    an HTML file using the Bokeh library.
    """

    # specify where to store HTML schedule
    output_file(output_file_path)

    # create the plot on which we design the schedule
    bokeh_schedule = Plot(width=2300, height=1580, title="ROOSTER RULERS' SCHEDULE")

    # retrieve the dataframe of the schedule object
    schedule_df = schedule_obj.get_dataframe()

    # determine amount of time slots and rooms
    time_slots_per_day = 5
    days_of_the_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    total_time_slots = len(days_of_the_week) * time_slots_per_day
    number_of_rooms = len(schedule_obj.get_rooms())

    # create coordinates of the rectangles (lessons) in the schedule
    x_values = np.tile(np.arange(number_of_rooms), total_time_slots)
    y_values = np.repeat(np.arange(total_time_slots) + .25, number_of_rooms)

    # dictionary of each lesson's attributes
    attributes = lesson_attributes(schedule_df)

    # only keep coordinates with lessons assigned to them
    x_values, y_values = remove_empty_slots(schedule_obj, x_values, y_values)

    # width and height of each lesson's visual representation (rectangle)
    rectangle_width = np.full(len(x_values), .98)
    rectangle_height = np.full(len(x_values), .95)

    # create data source for rectangles
    rect_src = ColumnDataSource(dict(x=x_values, 
                                    y=y_values, 
                                    w=rectangle_width, 
                                    h=rectangle_height,
                                    types=attributes["Type"],
                                    group_nrs=attributes["Group nr."],
                                    nr_students=attributes["Nr. students"],
                                    conflict_points=attributes["MP conflicts"],
                                    gap_points=attributes["MP gaps"],
                                    capacity_points=attributes["MP capacity"],
                                    evening_points=attributes["MP evening"],
                                    days=attributes["Days"],
                                    colors=attributes["Colors"]))

    # add the lesson rectangles to the plot
    rectangles = Rect(x="x", y="y", width="w", height="h", fill_color="colors")
    all_rectangles = bokeh_schedule.add_glyph(rect_src, rectangles)

    # create data source for smaller rectangles containing malus points
    small_rect_src = ColumnDataSource(dict(x=x_values + .4, 
                                            y=y_values, 
                                            w=rectangle_width / 7.1, 
                                            h=rectangle_height / 1.75,
                                            points=attributes["Malus points"]))

    # color the small rectangles according to the range of malus points
    small_rect_colormapper = LinearColorMapper(palette=RdYlGn[3], 
                                    low=min(attributes["Malus points"]), 
                                    high=max(attributes["Malus points"]))

    # add the small rectangles to the plot
    small_rectangles = Rect(x="x", 
                            y="y", 
                            width="w", 
                            height="h", 
                            fill_color={
                                'field': 'points', 
                                'transform': small_rect_colormapper
                            }
                        )
    bokeh_schedule.add_glyph(small_rect_src, small_rectangles)

    # create data source for lesson names text
    text_src = ColumnDataSource(dict(x=x_values - .45, 
                                    y=y_values + .15, 
                                    text=attributes["Name"]))

    # add lesson names text to schedule
    lesson_text = Text(x="x", y="y", text="text")
    lesson_text.text_font_size = {'value': '13px'}
    bokeh_schedule.add_glyph(text_src, lesson_text)

    # create data source for malus points text
    malus_points_text_src = ColumnDataSource(dict(x=x_values + .37, 
                                                y=y_values + .1, 
                                                text=attributes["Malus points"]))

    # add malus points text to schedule
    malus_points_text = Text(x="x", y="y", text="text")
    malus_points_text.text_font_size = {'value': '13px'}
    malus_points_text.text_font_style = {'value': 'bold'}
    bokeh_schedule.add_glyph(malus_points_text_src, malus_points_text)

    # create data source for data table
    data_table_src = ColumnDataSource(data=dict(name=[], 
                                                course=[], 
                                                group_nr=[]))

    # create empty data table for students and their lessons
    data_table = create_empty_data_table(data_table_src)

    # add the ability to select lessons
    bokeh_schedule.add_tools(TapTool())

    # if lesson is selected, make it deeppink
    all_rectangles.selection_glyph = Rect(fill_color="deeppink")

    # handle lesson selection and addition to data table
    select_lessons(rect_src, data_table_src, attributes)

    # add a hover tool
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
    bokeh_schedule.add_tools(hover)
        
    # add x and y axes and labels
    xaxis = LinearAxis(axis_label="Rooms | Capacity")
    bokeh_schedule.add_layout(xaxis, 'above')
    yaxis = LinearAxis(axis_label='Time slots')
    bokeh_schedule.add_layout(yaxis, 'left')
    yaxis2 = LinearAxis(axis_label='Days')
    bokeh_schedule.add_layout(yaxis2, 'left')

    # add grid lines
    bokeh_schedule.add_layout(Grid(dimension=0, ticker=xaxis.ticker))
    bokeh_schedule.add_layout(Grid(dimension=1, ticker=yaxis.ticker))
    bokeh_schedule.add_layout(Grid(dimension=1, ticker=yaxis2.ticker))

    # flip y axis
    bokeh_schedule.y_range.flipped = True 

    # create tick labels for rooms
    bokeh_schedule.xaxis.major_label_overrides = dict(
                                                    zip(range(number_of_rooms), 
                                                    [str(elem) for elem in schedule_obj.get_rooms()])
                                                )
    bokeh_schedule.xaxis.minor_tick_line_color = None

    # create tick labels for time - including one for very last slot ("19:00")
    bokeh_schedule.yaxis[0].ticker = np.arange(total_time_slots + 1)
    bokeh_schedule.yaxis[0].major_label_overrides = {num : time_ticker_func(num) for num in range(total_time_slots + 1)}

    # create tick labels for days - each tick being in middle of each day
    bokeh_schedule.yaxis[1].ticker = np.arange(
                                        (time_slots_per_day / 2), 
                                        total_time_slots + (time_slots_per_day / 2), 
                                        len(days_of_the_week)
                                    )
    bokeh_schedule.yaxis[1].major_label_overrides = {num : day_ticker_func(num) for num in np.arange((time_slots_per_day / 2), total_time_slots + (time_slots_per_day / 2), len(days_of_the_week))}

    # set font size for x and y axes
    bokeh_schedule.xaxis.axis_label_text_font_size = "15px"
    bokeh_schedule.xaxis.major_label_text_font_size = "15px"
    bokeh_schedule.yaxis.axis_label_text_font_size = "15px"
    bokeh_schedule.yaxis.major_label_text_font_size = "15px"

    # configure layout
    layout = row(bokeh_schedule, data_table)
    curdoc().add_root(layout)

    # save the results
    save(curdoc())

def lesson_attributes(lessons_df):
    """
    Returns dictionary of the lesson attributes,
    e.g. {"Name" : [name1, name2, ...], "Type": [type1, type2, ...], ...}
    """

    attributes = {}

    lessons_list = list(itertools.chain(*lessons_df.values.tolist()))

    # names
    lesson_names_list = list(map(lambda lesson_obj:lesson_obj.get_name() if isinstance(lesson_obj, Lesson) else "", lessons_list))
    attributes["Name"] = list(filter(lambda value: value !=  "", lesson_names_list))

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

    # colors
    colors = []
    slot_number = 0
    for day_index in range(5): # TODO: niet hardcoden?
        for day_slot in range(35): # TODO: niet hardcoden?
            if isinstance(lessons_list[slot_number], Lesson):
                if day_index % 2 == 0:
                    colors.append("lightcyan")
                else:
                    colors.append("darkturquoise")

            slot_number += 1

    attributes["Colors"] = colors

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

def create_empty_data_table(data_src):
    """
    Creates an empty Data Table that will later be filled with
    students and their courses.
    """

    # define HTML format for the columns
    html_formatter_name = HTMLTemplateFormatter(template=
                        """
                            <div title="<%= name %>" style="font-size: 13px;">
                            <%= value %>
                            </div>
                        """
                    )
    html_formatter_course = HTMLTemplateFormatter(template=
                        """
                            <div title="<%= course %>" style="font-size: 13px;">
                            <%= value %>
                            </div>
                        """
                    )
    html_formatter_group_nr = HTMLTemplateFormatter(template=
                        """
                            <div title="<%= group_nr %>" style="font-size: 13px;">
                            <%= value %>
                            </div>
                        """
                    )

    # define column properties
    columns = [
        TableColumn(field="name", 
                    title="""<b style="font-size: 13px;">%s</b>""" % "name", 
                    formatter=html_formatter_name, 
                    width=150),

        TableColumn(field="course", 
                    title="""<b style="font-size: 13px;">%s</b>""" % "course", 
                    formatter=html_formatter_course, 
                    width=230),

        TableColumn(field="group_nr", 
                    title="""<b style="font-size: 13px;">%s</b>""" % "#", 
                    formatter=html_formatter_group_nr, 
                    width=30)
        ]

    # create empty data table
    data_table = DataTable(source=data_src,
                            columns=columns,
                            height=1500,
                            autosize_mode="none")

    return data_table

def select_lessons(rect_src, data_src, attributes):
    """   
    If lesson is selected, selects all lessons from same course 
    and adds each lesson's students to the data table.
    """

    rect_src.selected.js_on_change('indices', CustomJS(

        args=dict(src=data_src, 
                lesson_students=attributes["Students"],
                lesson_names=attributes["Name"],
                group_nrs=attributes["Group nr."]), 

        code="""

            // empty the data table
            src.data['name'] = []
            src.data['course'] = []
            src.data['group_nr'] = []

            // store manually selected index
            var inds = cb_obj.indices

            // retrieve the name of the manually selected lesson
            let selected_lesson_name = lesson_names[inds[0]]

            // loop over all lesson names
            for (let lesson_name_index = 0; lesson_name_index < lesson_names.length; lesson_name_index++) {

                // if this lesson is from the same course as the manually selected lesson
                if (lesson_names[lesson_name_index] == selected_lesson_name && lesson_name_index != inds[0]) {

                    // add the index to the list of selected indices
                    inds.push(lesson_name_index)
                }
            }

            // loop over all selected lessons
            for (let i = 0; i < inds.length; i++) {

                // retrieve this lesson's properties
                let selected_index = inds[i]
                let students = lesson_students[selected_index]
                let course = lesson_names[selected_index]
                let group_nr = group_nrs[selected_index]

                // loop over students in this lesson
                for (let j = 0; j < students.length; j++) {

                    // add student to the data table
                    let student = students[j]
                    src.data['name'].push(student)
                    src.data['course'].push(course)
                    src.data['group_nr'].push(group_nr)
                }
            }
            src.change.emit()
        """)
    )

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

### TODO
# alle code mooier schrijven + comments (alleen functies nog)
# eval_schedule_objects() eruit?
# verder opdelen in functies, bijv. add_hover()
# visualize_boxplot en visualize_iterative ook nakijken