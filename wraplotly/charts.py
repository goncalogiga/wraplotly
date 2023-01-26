import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from wraplotly.wraplotly import draw


class line(draw):
    """
    A class grouping plotly express' line and plotly graph_objects' Scatter.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing come columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.
    + type: str
        The type of the graph object.

    Methods
    -------
    + plot()
        Plots the line by calling the 'hidden' function __plot_fn__. It is also possible to plot the line
        by simply having it in the last line of a jupyter's notebook cell, since the __repr__ method is implemented.
        Both plot() and __repr__() come from the mother class draw.
    """
    type: str = "scatter"

    def __init__(self, df=None, x=None, y=None, **kwargs):
        self.kwargs = kwargs
        self.df = df
        self.x = x
        self.y = y

    def __plot_fn__(self):
        """
        Returns the plotly object representing the line
        """
        if self._wraplotly_context == "px":
            return px.line(self.df, self.x, self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df:
            return go.Scatter(x=self.df[self.x], y=self.df[self.y], **self.kwargs)
        elif self._wraplotly_context == "go":
            return go.Scatter(x=self.x, y=self.y, **self.kwargs)


class colored_line(draw):
    """
    A class that can be used to color a *single* line in Plotly. This is especially usefull to
    vizualize time series data or time series predictions.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing come columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.
    + palette: str
        Name of palette or None to return current palette. 
    + type: str
        The type of the graph object.

    Methods
    -------
    + plot()
        Plots the line by calling the 'hidden' function __plot_fn__. It is also possible to plot the line
        by simply having it in the last line of a jupyter's notebook cell, since the __repr__ method is implemented.
        Both plot() and __repr__() come from the mother class draw.
    """
    def __init__(self, df=None, x=None, y=None, color=None, palette=None, **kwargs):
        self.kwargs = kwargs
        self.df = df
        self.x = x
        self.y = y
        self.color = color
        self.palette = palette

    def __plot_fn__(self):
        if self.df is None:
            x, y, color = self.x, self.y, self.color
        else:
            x, y, color = self.df[self.x], self.df[self.y], self.df[self.color]

        figures, colors_in_legend = [], set()

        colors = [
            (int(r*255), int(g*255), int(b*255))\
            for r, g, b in sns.color_palette(self.palette, len(set(color)))
        ]

        color_palette = {
            c: '#%02x%02x%02x' % (colors[i][0], colors[i][1], colors[i][2])\
            for i, c in enumerate(set(color))
        }

        for tn in range(len(x)):
            name = str(color[tn])

            if color[tn] not in colors_in_legend:
                showlegend = True
                colors_in_legend.add(color[tn])
            else:
                showlegend = False
            
            figures.append(
                go.Scatter(
                    x=x[tn : tn + 2],
                    y=y[tn : tn + 2],
                    line_color=color_palette[color[tn]],
                    name=name,
                    showlegend=showlegend,
                    **self.kwargs
                )
            )

        return go.Figure(figures)