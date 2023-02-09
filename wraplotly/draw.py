import pandas
import warnings
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from wraplotly import base, utils, discrete_palette, continuous_palette


class scatter(base.plot2d):
    """
    A class grouping plotly express' scatter and plotly graph_objects' Scatter (with mode=markers).

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Scatter"

    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, colorscale=None, **kwargs):
        self.kwargs = kwargs
        self.colorscale = colorscale if colorscale else continuous_palette
        super().__init__(df, x, y, color, x_axis, y_axis, title)

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.scatter(data_frame=self.df, x=self.x, y=self.y, color=self.color, title=self.title, **self.kwargs)

    def __color__(self, color, name):
        if isinstance(color, list):
            return dict(marker=dict(color=color, colorbar=dict(title=name), colorscale=self.colorscale))
        return dict(marker=dict(color=color))

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        return go.Scatter(x=x, y=y, mode="markers", **self.__color_args__(color, name, show_name, row), **self.kwargs)


class line(base.plot2d):
    """
    A class grouping plotly express' line and plotly graph_objects' Scatter.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Line"

    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(df, x, y, color, x_axis, y_axis, title)

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.line(data_frame=self.df, x=self.x, y=self.y, color=self.color, title=self.title, **self.kwargs)

    def __color__(self, color, name):
        return dict(marker=dict(color=color))

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        if "mode" in self.kwargs:
            return go.Scatter(x=x, y=y, **self.__color_args__(color, name, show_name, row), **self.kwargs)
        else:
            return go.Scatter(x=x, y=y, mode="lines", **self.__color_args__(color, name, show_name, row), **self.kwargs)


class bar(base.plot2d):
    """
    A class grouping plotly express' bar and plotly graph_objects' Bar.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Bar"

    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(df, x, y, color, x_axis, y_axis, title)

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.bar(data_frame=self.df, x=self.x, y=self.y, color=self.color, title=self.title, **self.kwargs)

    def __color__(self, color, name):
        return dict(marker=dict(color=color))

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        return go.Bar(x=x, y=y, **self.__color_args__(color, name, show_name, row), **self.kwargs)


class box(base.plot2d):
    """
    A class grouping plotly express' box and plotly graph_objects' Box.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Box"

    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(df, x, y, color, x_axis, y_axis, title)

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.box(data_frame=self.df, x=self.x, y=self.y, color=self.color, title=self.title, **self.kwargs)

    def __color__(self, color, name):
        return dict(marker=dict(color=color))

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        return go.Box(x=x, y=y, **self.__color_args__(color, name, show_name, row), **self.kwargs)


class histogram(base.plot2d):
    """
    A class grouping plotly express' histogram and plotly graph_objects' Histogram.
    Note that this class is heavily modified and might bot behave like plotly express's histogram object at all

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Histogram"
    default_y_axis = "count"

    def set_barmode(self, y, color, barmode, join_bars):
        if barmode is not None:
            self.barmode = barmode
        elif join_bars:
            self.barmode = "relative"
        else:
            self.barmode = "group" if y is not None or color is not None else "relative"

    def set_histfunc(self, df, x, y, histfunc):
        self.set_y_as_color = False

        if histfunc:
            self.histfunc = histfunc
            return
        
        if y is None:
            self.histfunc = "count"
        elif df is not None and isinstance(df, pandas.core.frame.DataFrame) and isinstance(y, str):
            if pandas.api.types.is_numeric_dtype(df[x]) or pandas.api.types.is_numeric_dtype(df[y]):
                self.histfunc = "sum"
            else:
                self.set_y_as_color = True if x is not None else False
                self.histfunc = "count"
        else:
            self.histfunc = "count"

    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, orientation=None, histfunc=None, join_bars=False, barmode=None, **kwargs):
        self.kwargs = kwargs
        self.orientation = orientation
        self.set_barmode(y, color, barmode, join_bars)
        self.set_histfunc(df, x, y, histfunc)

        # If the y column contains categorical values only, set it as color
        if color is None and self.set_y_as_color:
            color = y
        
        user_defined_y_axis = y_axis is not None
        y_axis = f"{self.histfunc} of {y}" if isinstance(y, str) and not user_defined_y_axis else None     
        super().__init__(df, x, y, color, x_axis, y_axis, title)

        if self.histfunc == "count":
            if isinstance(df, pandas.core.frame.DataFrame):
                x_cnt = len(set(self.df[self.x])) if self.x is not None else None
                y_cnt = len(set(self.df[self.y])) if self.y is not None else None
            else:
                x_cnt = len(set(self.x)) if self.x is not None else None
                y_cnt = len(set(self.y)) if self.y is not None else None

            if x_cnt and y_cnt and x_cnt > y_cnt:
                self.x_axis = f"{self.histfunc} of {x}" if x is not None and isinstance(x, str) and x_axis is None else None
                self.y_axis = y if y is not None and isinstance(y, str) and not user_defined_y_axis else None
                self.orientation = 'h'

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.histogram(data_frame=self.df, x=self.x, y=self.y, color=self.color, barmode=self.barmode, histfunc=self.histfunc, title=self.title, orientation=self.orientation, **self.kwargs)

    def __color__(self, color, name):
        return dict(marker=dict(color=color))

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        return go.Histogram(x=x, y=y, orientation=self.orientation, histfunc=self.histfunc, **self.__color_args__(color, name, show_name, row), **self.kwargs)


class density_heatmap(base.plot2d):
    """
    A class grouping plotly express' density_heatmap and plotly graph_objects' Histogram2d.

    Attributes
    ----------
    + df : pandas.DataFrame
        A DataFrame containing some columns we wish to display on a line chart.
    + x : str|list
        Either a string specifying which column of self.df should be used as x-axis or a list that
        will be used as the x-axis data.
    + y : str|list
        Either a string specifying which column of self.df should be used as y-axis or a list that
        will be used as the y-axis data.

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Density Map"
    args_type = "df x y"

    def __init__(self, df=None, x=None, y=None, x_axis=None, y_axis=None, title=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(df, x, y, None, x_axis, y_axis, title)

    def __px__(self):
        self.set_color_discrete_sequence()
        return px.density_heatmap(data_frame=self.df, x=self.x, y=self.y, title=self.title, **self.kwargs)

    def __go__(self, x, y, color=None, name=None, show_name=None, row=None):
        return go.Histogram2d(x=x, y=y, **self.kwargs)


class imshow(base.draw):
    name = "Image"

    def __init__(self, data=None, **kwargs):
        self.data = data
        self.kwargs = kwargs

    def __px__(self):
        return px.imshow(img=self.data, **self.kwargs)

    def __go__(self):
        return go.Image(z=self.data, **self.kwargs)        


# Heatmap makes more sense then imshow when using it for correlation matrices
class heatmap(base.draw):
    """
    A class behaving similarly to sns.heatmap

    Attributes
    ----------
    + data : pandas.DataFrame
        A DataFrame or array that will be displayed in the heatmap
    + colorscales: A dictionary 

    Methods
    -------
    + fig (proprety):
        Returns the plotly object associated with the object heriting from plot2d
    + show:
        Shows the figure
    """
    name = "Heatmap"
    colorscales = {
        "correlation": "Inferno",
        "confusion": "Electric",
        "default": None
    }


    def __init__(self, data=None, range_color=None, title=None, colorscales=None, labels=None, xlabels=None, ylabels=None, **kwargs):
        utils.itt_assertion(data, "name")
        if (xlabels or ylabels or labels) and isinstance(data, pandas.core.frame.DataFrame):
            warnings.warn("You should not specify labels when using a dataframe explicitly.")
            xlabels, ylabels, labels = None, None, None
            self.data = data
        elif xlabels:
            self.data = pandas.DataFrame(data, columns=xlabels)
        elif ylabels:
            if isinstance(data, pandas.core.frame.DataFrame):
                self.data = data.set_index(pandas.Index(ylabels)) 
            else:
                self.data = pandas.DataFrame(data, index=ylabels)
        elif xlabels is None and ylabels is None and labels:
            self.data = pandas.DataFrame(data, columns=labels, index=labels)
        else:
            self.data = data

        self.title = title
        self.kwargs = kwargs
        self.range_color = range_color
        self.color_continuous_scale = self.colorscales["default"]
        self.colorscales = colorscales if colorscales else self.colorscales

        # Infer correlation
        if -1 <= np.array(data).min() and np.array(data).max() <= 1:
            self.range_color = [-1,1] if range_color is None else range_color
            self.title = "Correlation Matrix" if title is None else title
            self.color_continuous_scale = self.colorscales["correlation"]

        # Infer confusion
        if 0 <= np.array(data).min() and all(int(x) == x for x in np.array(data).flatten()):
            self.title = "Confusion Matrix" if title is None else title
            if "text_auto" not in self.kwargs: kwargs["text_auto"] = True
            self.color_continuous_scale = self.colorscales["confusion"]

        self.kwargs = kwargs

    def __px__(self):
        return px.imshow(
            img=self.data,
            title=self.title,
            range_color=self.range_color,
            color_continuous_scale=self.color_continuous_scale,
            **self.kwargs
        )

    def __go__(self):
        raise RuntimeError("heatmap does not support arrangements, use imshow instead.")


# === custom functions not comming from plotly directly ===


class distplot(base.draw):
    def __init__(self, hist_data=None, columns=None, title=None, **kwargs):
        columns = columns if isinstance(columns, list) else [columns]

        if hist_data is not None and isinstance(hist_data, pandas.core.frame.DataFrame):
            columns = columns if columns else hist_data.select_dtypes(include=np.number).columns
            hist_data = [hist_data[c].values for c in columns]

        self.kwargs = kwargs
        self.columns = columns
        self.hist_data = hist_data
        self.title = title if title is not None else "Distribution Plot"

    def __go__(self, *args, **kwargs):
        raise RuntimeError("Wraplotly custom object 'distplot' cannot be arranged.")
        
    @property
    def fig(self):
        self.set_color_discrete_sequence(nb_of_colors=len(self.columns), color_key="colors")
        fig = ff.create_distplot(self.hist_data, group_labels=self.columns, **self.kwargs)
        fig.update_layout(title=self.title)
        return fig


class colored_line(base.plot2d):
    def __init__(self, df=None, x=None, y=None, color=None, x_axis=None, y_axis=None, title=None, **kwargs):
        self.kwargs = kwargs
        super().__init__(df, x, y, color, x_axis, y_axis, title)

    def __go__(self, *args, **kwargs):
        raise RuntimeError("Wraplotly custom object 'colored_line' cannot be arranged.")

    @property
    def fig(self):
        """
        Returns the plotly object representing the colored line (arragement of different line traces)
        """
        if self.df is None:
            x, y, color = self.x, self.y, self.color
        else:
            x, y, color = self.df[self.x], self.df[self.y], self.df[self.color]

        figures, colors_in_legend = [], set()

        color_palette = {
            c: '#%02x%02x%02x' % (int(r*255), int(g*255), int(b*255))\
            for c, (r, g, b) in zip(set(color), sns.color_palette(discrete_palette, n_colors=len(set(color))))
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
                    x=x[tn:tn+2],
                    y=y[tn:tn+2],
                    line_color=color_palette[color[tn]],
                    name=name,
                    showlegend=showlegend,
                    **self.kwargs
                )
            )

        return go.Figure(figures, layout={"title": self.title})


class pairplot(base.draw):
    def __init__(self, df=None, color=None, title=None, width=800, height=800, **kwargs):
        self.df = df
        self.color = color
        self.title = title
        self.width = width
        self.height = height
        self.kwargs = kwargs
    
    def __go__(self, *args, **kwargs):
        raise RuntimeError("Wraplotly custom object 'pairplot' cannot be arranged.")

    @property
    def fig(self):
        self.set_color_discrete_sequence(nb_of_colors=len(set(self.df[self.color])), color_key="colormap")
        fig = ff.create_scatterplotmatrix(self.df, diag='box', index=self.color, height=self.height, width=self.width, **self.kwargs)
        fig.update_layout(title=self.title)
        return fig