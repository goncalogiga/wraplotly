import numpy as np
from plotly.subplots import make_subplots
from wraplotly.wraplotly import arrange


class Grid(arrange):
    objects, object_cnt= {}, 0

    def __init__(self, layout: list, column_widths=None, row_heights=None, **kwargs):
        """
        Layout example: [[0], [1], [2]] or [[0, 0], [1, 2]]
        """
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
        self.specs = [[None for j in range(self.cols)] for i in range(self.rows)]

        for i, line in enumerate(self.layout):
            if len(set(line)) == 1:
                self.specs[i] = [{"colspan": self.rows}] + [None]*(self.rows - 1)

        for j, column in enumerate(self.layout.T):
            if len(set(column)) == 1:
                for i in range(self.rows): 
                    if i == 0:
                        self.specs[i][j] = {"rowspan": self.rows}
                    else:
                        self.specs[i][j] = None

    def __call__(self, obj):
        if self.object_cnt > self.nb_of_objs:
            raise RuntimeError(f"Too many objects added to Grid. Maximum calls available is {self.nb_of_objs}.")
            
        self.objects[self.object_cnt] = obj
        self.object_cnt += 1

    def build_fig(self):
        prefig = []
        used_objects_indexes = set()

        for i in range(self.rows):
            for j in range(self.cols):
                obj_idx = self.layout[i][j]

                if obj_idx in used_objects_indexes:
                    continue

                obj = self.objects[obj_idx]
                obj._wraplotly_context = "go"

                prefig.append((self.objects[obj_idx].__plot_fn__(), {"row": i+1, "col": j+1}))
                
                if self.specs and self.specs[i][j] is None:
                    self.specs[i][j] = {"type": self.objects[obj_idx].type}
                elif self.specs and self.specs[i][j]:
                    self.specs[i][j]["type"] = self.objects[obj_idx].type
                
                used_objects_indexes.add(obj_idx)

        self._fig = make_subplots(
            rows=self.rows, 
            cols=self.cols, 
            column_widths=self.column_widths, 
            row_heights=self.row_heights, 
            specs=self.specs
        )

        for data, kwargs in prefig:
            self._fig.add_trace(data, **kwargs)

    def show(self):
        self.build_fig()
        return self.fig.show()