import pandas
from wraplotly.draw import line
from wraplotly.base import make_grid


class grid(make_grid):
    """
    A grid is used to display multiple plotly objects by using the graph_objects
    equivalents to the plotly express objects and arranging them in a subplot.

    Usage:
    > g = grid([[0,0], [1,2]])
    >
    > g(wp.line([1,2,3]))
    > g(wp.line([4,5,6]))
    > g(wp.line([7,8,9]))
    > g

    Attributes
    ----------
    + grid: list
        A matrix of integers representing the looks of the grid

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    def __init__(self, grid, **kwargs):
        self.grid = grid
        self.objects = []
        self.object_cnt = 0
        self.kwargs = kwargs
        self.nb_of_objects = len(set(x for line in grid for x in line))

    def __call__(self, *objects):
        if self.object_cnt >= self.nb_of_objects:
            raise RuntimeError(f"Too many objects added to grid (maximum allowed is {self.nb_of_objects}).")

        self.object_cnt += 1
        self.objects.append([(obj, {}) for obj in objects])

    @property
    def fig(self):
        if self.object_cnt != self.nb_of_objects:
            raise RuntimeError(f"Not enough objects, expected {self.nb_of_objects} but got {self.object_cnt} instead.")
        super().__init__(self.grid, self.objects, **self.kwargs)
        return super().fig


class hstack(grid):
    """
    Stacks multiple plotly objects horizontaly by using the graph_objects
    equivalents to the plotly express objects and arranging them in a subplot.

    Usage:
    > hstack(
    >   wp.line([1,2,3]),
    >   wp.line([4,5,6])
    > )

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    def __init__(self, *objects, **kwargs):
        super().__init__([[i for i in range(len(objects))]], **kwargs)
        for obj in objects: self(obj)


class vstack(grid):
    """
    Stacks multiple plotly objects verticaly by using the graph_objects
    equivalents to the plotly express objects and arranging them in a subplot.

    Usage:
    > vstack(
    >   wp.line([1,2,3]),
    >   wp.line([4,5,6])
    > )

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    def __init__(self, *objects, **kwargs):
        super().__init__([[i] for i in range(len(objects))], **kwargs)
        for obj in objects: self(obj)


class combine(grid):
    """
    Combines multiple plotly objects by using the graph_objects equivalents to the 
    plotly express objects and arranging them in a subplot.

    Usage:
    > combine(
    >   wp.line([1,2,3]),
    >   wp.line([4,5,6])
    > )

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    def __init__(self, *objects, **kwargs):
        super().__init__([[0]], **kwargs)
        self(*objects)