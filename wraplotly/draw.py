import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from wraplotly.wraplotly import draw


class scatter(draw):
    """
    A class grouping plotly express' scatter and plotly graph_objects' Scatter.

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

        # In order to call line without a dataframe in arragements
        if df is not None and x is not None and y is None:
            y = x
            x = df
            df = None
        if df is not None and x is None and y is None:
            x = df
            df = None

        self.df = df
        self.x = x
        self.y = y

    def __plot_fn__(self):
        """
        Returns the plotly object representing the line
        """
        if self._wraplotly_context == "px":
            self.__px_to_go_bad_conversion_errors__()
            return px.scatter(data_frame=self.df, x=self.x, y=self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df is not None:
            return go.Scatter(x=self.df[self.x], y=self.df[self.y], mode="markers", **self.kwargs)
        elif self._wraplotly_context == "go":
            return go.Scatter(x=self.x, y=self.y, mode="markers", **self.kwargs)


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

        # In order to call line without a dataframe in arragements
        if df is not None and x is not None and y is None:
            y = x
            x = df
            df = None
        if df is not None and x is None and y is None:
            x = df
            df = None

        self.df = df
        self.x = x
        self.y = y

    def __plot_fn__(self):
        """
        Returns the plotly object representing the line
        """
        if self._wraplotly_context == "px":
            self.__px_to_go_bad_conversion_errors__()
            return px.line(data_frame=self.df, x=self.x, y=self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df is not None:
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
        """
        Returns the plotly object representing the colored line (arragement of different line traces)
        """
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


class bar(draw):
    """
    A class grouping plotly express' bar and plotly graph_objects' Bar.

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
        Returns the plotly object representing the bar
        """
        if self._wraplotly_context == "px":
            self.__px_to_go_bad_conversion_errors__()
            return px.bar(data_frame=self.df, x=self.x, y=self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df is not None:
            return go.Bar(x=self.df[self.x], y=self.df[self.y], **self.kwargs)
        elif self._wraplotly_context == "go":
            return go.Bar(x=self.x, y=self.y, **self.kwargs)


class box(draw):
    """
    A class grouping plotly express' box and plotly graph_objects' Box.

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
        Returns the plotly object representing the box plot
        """
        if self._wraplotly_context == "px":
            self.__px_to_go_bad_conversion_errors__()
            return px.box(data_frame=self.df, x=self.x, y=self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df is not None:
            return go.Box(x=self.df[self.x] if self.x is not None else None, 
                          y=self.df[self.y], **self.kwargs)
        elif self._wraplotly_context == "go":
            return go.Box(x=self.x, y=self.y, **self.kwargs)


class imshow(draw):
    type: str = "scatter"
    _actual_image = True

    def __init__(self, data=None, **kwargs):
        self.kwargs = kwargs
        self.data = data

    def __plot_fn__(self):
        """
        Returns the plotly object representing the box plot
        """
        if self._wraplotly_context == "px":
            self.__px_to_go_bad_conversion_errors__()
            return px.imshow(img=self.data, **self.kwargs)
        elif self._wraplotly_context == "go":
            if self._actual_image:
                return go.Image(z=self.data, **self.kwargs)
            return go.Heatmap(z=self.data, **self.kwargs)


# Heatmap makes more sense then imshow when using it for correlation matrices
# and so on
class heatmap(imshow):
    _actual_image = False


class confusion(draw):
    def __init__(self, data, labels, margin=dict(t=50, l=500, r=500), colorscale='Viridis', **kwargs):
        self.kwargs = kwargs
        self.data = data
        self.labels = labels
        self.margin = margin
        self.colorscale = colorscale

    def __plot_fn__(self):
        """
        Returns the plotly objects representing the confusion matrix
        """
        if self._wraplotly_context == "go":
            raise RuntimeError("The confusion matrix object does not support arragements.")

        x, y = self.labels, self.labels

        text = [[str(y) for y in x] for x in self.data]

        fig = ff.create_annotated_heatmap(z=self.data, x=x, y=y, annotation_text=text, 
                                               colorscale=self.colorscale)

        fig.update_layout(title_text='Confusion matrix')

        fig.add_annotation(dict(font=dict(color="black",size=14),
                                x=0.5,
                                y=-0.15,
                                showarrow=False,
                                text="Predicted value",
                                xref="paper",
                                yref="paper"))

        fig.add_annotation(dict(font=dict(color="black",size=14),
                                x=-0.35,
                                y=0.5,
                                showarrow=False,
                                text="Real value",
                                textangle=-90,
                                xref="paper",
                                yref="paper"))

        fig.update_layout(margin=self.margin)

        return fig