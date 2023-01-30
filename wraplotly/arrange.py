import numpy as np
from plotly.subplots import make_subplots
from wraplotly.base import arrange


class grid(arrange):
    """
    A class used to create grids in Plotly whitout using the usual subfigures method.

    In order to create a grid you have to define one with a given layout a populate it
    by calling this class.
    
    Usage:

    grid = wp.grid([
        [0,1], 
        [0,2]
    ])

    grid(line(x=[1,2,3], y=[5,6,5], name="Test 1"))
    grid(line(x=[1,2,3], y=[12,12,5], name="Test 2"))
    grid(line(x=[1,2,3], y=[-1,-1,5], name="Test 3"))
    grid.show()


    Attributes
    ----------
    + layout : list
        A list representing the layout of the grid. Each element represents the index of a plot (starts from 0)
        and can be arranged as the users wishes. If you want for different graphs:
        [[0,1], [2,3]]
        If you want a large first plot followed by two smaller ones:
        [[0,0], [1,2]]
        ect...
    + column_widths : list
        A list specifying the percentage of space each column should take. If you want a 70% left and 30% right layout,
        the paramater column_widths sould be [0.7, 0.3]. By default space is split equaly.
    + row_heights : list
        A list specifying the percentage of space each row should take (similar to column_widths)
    + fig:
        The actual object fig that is initialized with make_subplots. In order to access it (to do things like update_layout)
        you need to call the build_fig() method first.

    Methods
    -------
    + build_fig()
        Populates the fig object by creating every traces and adding them to the subfigure constructor.
    + plot()
        Plots the Grid (defined in the mother class arange)
    """
    objects, object_cnt= {}, 0

    def __init__(self, layout: list, column_widths=None, row_heights=None, **kwargs):
        self.kwargs = kwargs
        self.layout = np.array(layout)
        self.rows = self.layout.shape[0]
        self.cols = self.layout.shape[1]
        self.row_heights = row_heights
        self.column_widths = column_widths
        self.nb_of_objs = len(set(self.layout.flatten()))
        if self.nb_of_objs < self.rows + self.cols:
            self.__build_objects_base_specs__()
        else:
            self.specs = None

    def __build_objects_base_specs__(self):
        """
        Builds the specs argument that will be passed to make_subplots
        """
        self.specs = [[None for j in range(self.cols)] for i in range(self.rows)]

        for i, line in enumerate(self.layout):
            if len(set(line)) == 1 and len(line) > 1:
                self.specs[i] = [{"colspan": self.rows}] + [None]*(self.rows - 1)

        for j, column in enumerate(self.layout.T):
            if len(set(column)) == 1:
                for i in range(self.rows): 
                    if i == 0:
                        self.specs[i][j] = {"rowspan": self.rows}
                    else:
                        self.specs[i][j] = None

    def __call__(self, *objects):
        """
        Adds a subplot. Every call to this class increases a counter (object_cnt) so the order
        calls matters. It is linked to the indexes that were defined in the layout (during class construction).
        """
        if self.object_cnt > self.nb_of_objs:
            raise RuntimeError(f"Too many objects added to grid. Maximum calls available is {self.nb_of_objs}.")
            
        self.objects[self.object_cnt] = list(objects)
        self.object_cnt += 1

    def build_fig(self):
        """
        Builds the fig object containing the grid.
        """
        prefig = []
        used_objects_indexes = set()

        for i in range(self.rows):
            for j in range(self.cols):
                obj_idx = self.layout[i][j]

                if obj_idx in used_objects_indexes:
                    continue

                objects = self.objects[obj_idx]
                for obj in objects:
                    obj._wraplotly_context = "go"

                prefig.append((
                    [obj for objects in self.objects[obj_idx] for obj in objects.__plot_fn__()], 
                    {"row": i+1, "col": j+1}
                ))

                objects_type = set(obj.type for obj in self.objects[obj_idx])

                if len(objects_type) > 1:
                    raise ValueError(f"More than one type in object collection (grid index '{obj_idx}').")
                
                if self.specs and self.specs[i][j] is None:
                    self.specs[i][j] = {"type": list(objects_type)[0][0]}
                elif self.specs and self.specs[i][j]:
                    self.specs[i][j]["type"] = list(objects_type)[0][0]
                
                used_objects_indexes.add(obj_idx)

        self._fig = make_subplots(
            rows=self.rows, 
            cols=self.cols, 
            column_widths=self.column_widths, 
            row_heights=self.row_heights, 
            specs=self.specs
        )

        for objects, kwargs in prefig:
            for obj in objects:
                self._fig.add_trace(obj, **kwargs)


class vstack(arrange):
    """
    Stack figures verticaly
    """
    def __init__(self, *args):
        self.args = args

    def build_fig(self):
        g = grid([[i] for i in range(len(self.args))])

        for object in self.args:
            g(object)

        g.build_fig()
        self._fig = g.fig


class hstack(arrange):
    """
    Stack figures horizontaly
    """
    def __init__(self, *args):
        self.args = args

    def build_fig(self):
        g = grid([[i for i in range(len(self.args))]])

        for object in self.args:
            g(object)

        g.build_fig()
        self._fig = g.fig


class combine(arrange):
    """
    Combine drawings together
    """
    def __init__(self, *args):
        self.args = args

    def build_fig(self):
        self._fig = make_subplots(rows=1, cols=1)

        for object in self.args:
            object._wraplotly_context = "go"
            for obj in object.__plot_fn__():
                self._fig.add_trace(obj, row=1, col=1)