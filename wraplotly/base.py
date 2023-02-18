"""
Mother classes of wraplotly.
"""
import pandas
import warnings
import numpy as np
import seaborn as sns
from plotly import subplots
from wraplotly import discrete_palette, utils
from plotly_resampler import FigureWidgetResampler


MIN_OBJECTS_UNTIL_HEATMAP = 2


class make_grid:
    """
    The super class for any arragement of wraplotly's custom objects. This class should be
    used as a mother class for more general classes like grid or combine. It can still be
    called directly.

    Usage:

    make_grid([[0]], [[(wp.line([1,2,3], {}))]])

    First argument is the grid and the secound is a list of every object linked to the identifiers
    defined in the grid. The object is not passed directly but is a tuple of the plotly object and
    a dictionary which will be passed to the .add_trace plotly method (this makes it possible to pass
    explicit plotly's paramaters to the trace).

    Attributes
    ----------
    + grid: list
        A list displaying how the arragement of plots should look like.
    + objects: list
        A list of tuples of plotly objects and dictionaries which will be passed to the .add_trace 
        plotly method (this makes it possible to pass explicit plotly's paramaters to the trace).
    + show_unnammed_traces: bool
        If true displays a default name for each plot in the arragements' legend.
    + kwargs:
        Extra arguments passed to the make_subplot plotly function.
    
    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    def __init__(self, grid, objects, show_unnamed_traces=False, **kwargs):
        assert grid is not None, "grid argument cannot be None."
        assert objects is not None, "objects argument cannot be None."

        self.grid = np.array(grid)
        self.objects = objects
        self.kwargs = kwargs
        self.rows = self.grid.shape[0]
        self.cols = self.grid.shape[1]
        self.show_unnamed_traces = show_unnamed_traces

        self.flatten_objects = [obj[0] for object in self.objects for obj in object]


    def update_color(self, flatten_objects_idx, color):
        """
        This method is used to change the .color argument in an object.
        Every instance of the object stored in this class will be modified,
        so both self.objects and self.flatten_objects will be changed.

        Attributes
        ----------

        + flatten_objects_idx: int
            The index of the object that will be modified (this index is given with respect
            to the flatten list object so it is the actual index of the object not the one
            in the grid)
        """
        self.flatten_objects[flatten_objects_idx].color = color

        obj_cnt = 0

        for i in range(len(self.objects)):
            for j in range(len(self.objects[i])):
                if obj_cnt == flatten_objects_idx:
                    self.objects[i][j][0].color = color
                    return
                obj_cnt += 1


    def make_specs(self):
        """
        Generates the specs that will be passed to the 'make_subplots' function of plotly.

        This creates the grid based on the given input grid but also adds the type specific
        to the objects that are being passed to the grid.
        """
        self.specs = [[None for _ in range(self.cols)] for _ in range(self.rows)]

        for i, line in enumerate(self.grid):
            if len(set(line)) == 1 and len(line) > 1:
                self.specs[i] = [{"colspan": self.cols}] + [None]*(self.cols - 1)
        
        for j, column in enumerate(self.grid.T):
            if len(set(column)) == 1:
                for i in range(self.rows): 
                    self.specs[i][j] = {"rowspan": self.rows} if i == 0 else None

        used_objects_indexes = set()

        for i in range(self.rows):
            for j in range(self.cols):
                object_idx = self.grid[i][j]

                object_types = list(set(obj[0].type for obj in self.objects[object_idx]))

                if len(object_types) > 1:
                    raise ValueError(f"More than one type in object collection (grid index '{object_idx}').")

                if object_idx not in used_objects_indexes:
                    if self.specs[i][j]:
                        self.specs[i][j]["type"] = object_types[0]
                    else:
                        self.specs[i][j] = {"type": object_types[0]}
                    used_objects_indexes.add(object_idx)


    def make_subplots(self):
        """
        Creates the subplot by calling the plotly's function make_subplots

        Prior to creating the suplots, this function also infers the name
        of the overall x-axis and y-axis if it makes sense to do so. This means
        that if every object passed to the grid share the same x-axis name, the
        overall axis will change to avoid repetitions in each subplot.
        """
        self.shared_x_axis, self.shared_y_axis = False, False

        # Infering axis
        if any("x y" in x.args_type for x in self.flatten_objects):
            all_x_axis = list(set(obj.x_axis for obj in self.flatten_objects))
            if len(all_x_axis) == 1 and "x_title" not in self.kwargs:
                self.kwargs["x_title"] = all_x_axis[0]
                self.shared_x_axis = True

            all_y_axis = list(set(obj.y_axis for obj in self.flatten_objects))
            if len(all_y_axis) == 1 and "y_title" not in self.kwargs:
                self.kwargs["y_title"] = all_y_axis[0]
                self.shared_y_axis = True

        return subplots.make_subplots(
            rows=self.rows, 
            cols=self.cols, 
            specs=self.specs,
            **self.kwargs
        )


    def make_objects_coordinates(self):
        """
        Makes the correspondance between each wraplotly object and their
        position in the grid.
        """
        used_objects_indexes = set()

        for i in range(self.rows):
            for j in range(self.cols):
                object_idx = self.grid[i][j]

                if object_idx not in used_objects_indexes:
                    for object in self.objects[object_idx]:
                        # updating the trace dict kwargs
                        object[1]["row"] = i+1
                        object[1]["col"] = j+1
                    
                    used_objects_indexes.add(object_idx)


    def make_color_palette(self):
        """
        Generates a list of colors (self.color_list) that will be used to color
        elements in the list.

        This is not only to separate subplots from each other but also to allow
        the color argument to be used in grids. Since grids only work with graph_objects
        we have to manualy deal with colors (adding a trace for each subset of the dataset
        associated with a specific class in the color column)
        """
        self.palette = {}
        self.heatmaps = {}
        self.color_titles = set()
        nb_of_colors = 0
        visited_colors = set()

        for i, obj in enumerate(self.flatten_objects):
            if 'c' not in obj.args_type:
                continue
            
            if obj.color is not None and isinstance(obj.color, str):
                self.color_titles.add(obj.color)

            if obj.df is not None and obj.color is not None:
                object_color_len = len(set(obj.df[obj.color]))
                if obj.use_heatmaps and object_color_len > MIN_OBJECTS_UNTIL_HEATMAP:
                    color_column = obj.df[obj.color]
                    self.update_color(i, f"Colorscale {i+1}") # Why not the actual color ?
                    self.heatmaps[obj.color] = list(color_column)
                else:
                    nb_of_colors += object_color_len
            else:
                nb_of_colors += 1

        colors = [
            '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))\
            for r, g, b in sns.color_palette(discrete_palette, n_colors=nb_of_colors)
        ]

        color_idx = 0

        for i, object in enumerate(self.flatten_objects):
            if 'c' not in object.args_type:
                continue

            if object.color is None:
                self.update_color(i, f"{object.name} {i+1}")
                self.palette[object.color] = colors[color_idx]
                color_idx += 1
            elif object.df is not None and object.color not in self.heatmaps:
                for color in set(object.df[object.color]):
                    if color not in visited_colors:
                        self.palette[color] = colors[color_idx]
                        visited_colors.add(color)
                        color_idx += 1

        if len(self.heatmaps) > 1:
            warnings.warn("Multiple heatmaps will result in overlaping legends.")

        self.color_list = list(self.palette.keys()) + list(self.heatmaps.keys())


    def select_from_df(self, wp_object, c=None):
        """
        Returns the value of x and y depending on the input given by the user 
        (if a dataframe was given use the columns, else use the data directly)

        It is important to notice this function is never called if the args_type
        of object does not contain x or y or c
        """
        df, x, y, color = wp_object.df, wp_object.x, wp_object.y, wp_object.color

        if c is not None:
            if x and isinstance(x, str):
                xout = df[df[color] == c][x]
            else:
                xout = x

            if y and isinstance(y, str):
                yout = df[df[color] == c][y]
            else:
                yout = y
        else:
            if x and isinstance(x, str):
                xout = df[x]
            else:
                xout = x
            
            if y and isinstance(y, str):
                yout = df[y]
            else:
                yout = y

        return xout, yout


    def make_go_objects(self, wp_object, row):
        """
        Builds the plotly graph_object based on the wrapper wp_object (given by wraplotly)
        This returns a list of graph_objects that contains only one graph_object if there are
        no colors in the data or multiple elements in the list when a color is given.
        """
        def get_color(c):
            if c is None:
                return None
            if c in self.palette:
                return self.palette[c]
            return self.heatmaps[c]

        go_objects = []

        if wp_object.color is not None and wp_object.df is not None and wp_object.color in wp_object.df:
            for c in set(wp_object.df[wp_object.color]):
                if c in self.color_list:
                    self.color_list.remove(c)
                    show_name = True
                else:
                    show_name = False

                x, y = self.select_from_df(wp_object, c)
                go_objects.append(wp_object.__go__(x, y, get_color(c), c, show_name, row))
        elif wp_object.df is not None:
            if wp_object.color in self.color_list: self.color_list.remove(wp_object.color)
            x, y = self.select_from_df(wp_object)
            go_objects = [wp_object.__go__(
                x, 
                y,
                get_color(wp_object.color), 
                wp_object.color, 
                self.show_unnamed_traces,
                row
            )]
        else:
            if wp_object.color in self.color_list: self.color_list.remove(wp_object.color)
            go_objects = [wp_object.__go__(
                wp_object.x, 
                wp_object.y,
                get_color(wp_object.color), 
                wp_object.color, 
                self.show_unnamed_traces,
                row
            )]

        return go_objects


    def add_trace(self, go_object, **trace_kwargs):
        if self.needs_resample:
            hf_x = go_object['x'] if 'x' in go_object else None
            hf_y = go_object['y'] if 'y' in go_object else None
            self._fig.add_trace(go_object, hf_x=hf_x, hf_y=hf_y, **trace_kwargs)
        else:
            self._fig.add_trace(go_object, **trace_kwargs)


    def make_traces(self):
        """
        Generates every trace needed to complete the grid arrangement.

        If there are two different traces that are sharing colors, this function
        will disable the option to hidde traces by clicking. Indeed, the trace in the
        legend is linked to an arbitrary trace only and hidding it will still keep the
        other elements sharing the same color in the grid, which doesn't make sense.
        """
        def same_colors_in_different_traces(object_colors, key):
            key_colors = object_colors[key]
            for object, color in object_colors.items():
                if object != key:
                    for c in color:
                        if c in key_colors:
                            return True
            return False

        object_colors = {}
        # If two traces will act like the same color, dissable clicking
        self.disable_legend_click = False

        for objects in self.objects:
            for object, trace_kwargs in objects:
                if object.args_type == "plain": # might not be general enough
                    self.add_trace(object.__go__(), **trace_kwargs)
                    continue
                
                if object.color is not None and object.df is not None:
                    if not self.disable_legend_click and object.color in object.df:
                        key = (trace_kwargs['row'], trace_kwargs['col'])
                        object_colors[key] = set(object.df[object.color])
                        self.disable_legend_click = same_colors_in_different_traces(object_colors, key)

                for go_object in self.make_go_objects(object, trace_kwargs["row"]):
                    self.add_trace(go_object, **trace_kwargs)


    def update_layout(self, **kwargs):
        """
        Updates the figure layout
        """
        kwargs = kwargs if kwargs else {}

        if len(self.color_titles) == 1 and "legend_title_text" not in kwargs:
            kwargs["legend_title_text"] = list(self.color_titles)[0]
        
        user_overwrite = "legend_itemclick" in kwargs and "legend_itemdoubleclick" in kwargs

        if self.disable_legend_click and not user_overwrite:
            kwargs["legend_itemclick"] = False
            kwargs["legend_itemdoubleclick"] = False
            warnings.warn("Legend actions were disabled since different traces share the same color.")
            
        self._fig.update_layout(legend_tracegroupgap=30, **kwargs)

    
    def make_axis(self):
        """
        Inferes the names of the x-axis and y-axis based on the column names of the
        dataframe (if a dataframe was passed)

        This function will not overwrite the global titles set up by the make_subplots
        method
        """
        if not self.shared_x_axis:
            for i, trace_objects in enumerate(self.objects):
                all_x_trace_axis = list(set(obj.x_axis for obj, _ in trace_objects))
                if len(all_x_trace_axis) == 1:
                    self._fig['layout'][f'xaxis{i+1}']['title'] = all_x_trace_axis[0]
            
        if not self.shared_y_axis:
            for i, trace_objects in enumerate(self.objects):
                all_y_trace_axis = list(set(obj.y_axis for obj, _ in trace_objects))
                if len(all_y_trace_axis) == 1:
                    self._fig['layout'][f'yaxis{i+1}']['title'] = all_y_trace_axis[0]


    @property
    def fig(self):   
        self.make_specs()

        # Call FigureWidgetResampler (plotly-resampler) if necessary
        self.needs_resample = any(obj.needs_resample for obj in self.flatten_objects)
        if self.needs_resample:
            self._fig = FigureWidgetResampler(self.make_subplots())
        else:
            self._fig = self.make_subplots()

        self.make_objects_coordinates()
        self.make_color_palette()
        self.make_traces()
        self.update_layout()
        self.make_axis()
        return self._fig


    def show(self):
        self.fig.show()

    def __repr__(self):
        self.show(); return ''


class draw:
    """
    The super class for any drawings done in wraplotly.
    
    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    # The type given to the specs when using plotly's subplots
    type = "scatter"
    args_type = "plain"
    use_heatmaps = False
    needs_resample = False
    x_axis, y_axis = None, None
    color_discrete_sequence = None

    def set_color_discrete_sequence(self, nb_of_colors=None, color_key="color_discrete_sequence"):
        if color_key in self.kwargs:
            return

        if nb_of_colors is None:
            if self.color is not None:
                if self.df is not None and isinstance(self.df, pandas.core.frame.DataFrame):
                    nb_of_colors = len(set(self.df[self.color]))
                else:
                    nb_of_colors = len(set(self.color))
            else:
                return

        self.kwargs[color_key] = [
            '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))\
            for r, g, b in sns.color_palette(discrete_palette, n_colors=nb_of_colors)
        ]

    @property
    def fig(self):   
        if self.needs_resample:
            warnings.warn("Data was too large and had to be downsampled using plotly-resampler.")
            return make_grid([[0]], [[(self, {})]]).fig
        return self.__px__()    
        
    def show(self):
        self.fig.show()

    def __repr__(self):
        self.show(); return ''


class plot2d(draw):
    """
    The super class for any object generating a plot in 2D.

    Attributes
    ----------
    + df: DataFrame
        A dataframe that contains columns that will be used in the generated plot.
    + x: str|array
        Either a string that represents a column in a dataframe (if a dataframe is used)
        or an array containing the data that should be uses as x-axis
    + y: str|array
        Either a string that represents a column in a dataframe (if a dataframe is used)
        or an array containing the data that should be uses as y-axis
    + color: str
        A string representing a column in a dataframe (the df argument should therefore be given)
        that will color the data with respect to the elements of the color column.
    + x_axis: str
        A string namming the x-axis in the plot
    + y_axis: str
        A string namming the y-axis in the plot
    + title: str
        A title for the plot
    
    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    args_type = "df x y c"
    default_x_axis, default_y_axis = "x", "y"


    def _init_from_dataframe(self, df, x, y, color, x_axis, y_axis):
        """
        A function called when the first argument passed to plot2d is of type
        DataFrame.

        Initializes self.df, self.x, self.y, color, self.x_axis and self.y_axis.
        """
        if x is not None: utils.str_assertion(x, "'x' argument", "When using a dataframe")
        if y is not None: utils.str_assertion(y, "'y' argument", "When using a dataframe")
        if color is not None: utils.str_assertion(color, "'color' argument", "When using a dataframe")

        self.df = df
        self.x, self.y, self.color = x, y, color
        self.x_axis = x_axis if x_axis else self.default_x_axis if x is None or not isinstance(x, str) else x
        self.y_axis = y_axis if y_axis else self.default_y_axis if y is None or not isinstance(y, str) else y

    
    def _init_from_array(self, x, y, color, x_axis, y_axis):
        """
        A function called when the first argument passed to plot2d is an array.

        Initializes self.df, self.x, self.y, color, self.x_axis and self.y_axis.
        """
        if x is not None: utils.itt_assertion(x, "'x' argument", "Without a dataframe")
        if y is not None: utils.itt_assertion(y, "'y' argument", "Without a dataframe") 
        if color is not None and not isinstance(color, str): utils.itt_assertion(color, "'color' argument")

        if color is not None:
            self.df = pandas.DataFrame({"x": x, "y": y, "color": color})
            self.x, self.y, self.color = "x", "y", "color"
        else:
            self.df, self.x, self.y, self.color = None, x, y, color

        self.x_axis = x_axis if x_axis else self.default_x_axis
        self.y_axis = y_axis if y_axis else self.default_y_axis


    def __init__(self, df, x, y, color, x_axis, y_axis, title):
        if isinstance(df, pandas.core.frame.DataFrame):
            self._init_from_dataframe(df, x, y, color, x_axis, y_axis)
            utils.count_nans_in_df_and_alert(self.df, self.x, self.y)
        elif df is not None:
            if x is None:
                self._init_from_array(list(range(len(df))), df, color, x_axis, y_axis)
            else:
                self._init_from_array(df, x, color, x_axis, y_axis)
            utils.count_nans_and_alert(self.x, self.y)
        elif x is not None and y is not None:
            self._init_from_array(x, y, color, x_axis, y_axis)
            utils.count_nans_and_alert(self.x, self.y)
        elif x is not None:
            self._init_from_array(x, list(range(len(x))), color, x_axis, y_axis)
            utils.count_nans_and_alert(self.x, self.y)
        elif y is not None:
            self._init_from_array(list(range(len(y))), y, color, x_axis, y_axis)
            utils.count_nans_and_alert(self.x, self.y)
        else:
            raise ValueError(f"Too many arguments without a dataframe: '{df}', '{x}', '{y}'.")
        
        self.title = title
        self.needs_resample = utils.needs_resample(self.df, self.x, self.y)


    def __color__(self, color):
        raise RuntimeError("__color__ was not defined.")

    def __color_args__(self, color, name, show_name, row):
        # for now no legendgroups
        row = '1'
        
        if 'name' not in self.kwargs:
            return dict(name=name, showlegend=show_name, legendgroup=str(row), **self.__color__(color, name))
        else:
            return dict(legendgroup=str(row), **self.__color__(color, name))