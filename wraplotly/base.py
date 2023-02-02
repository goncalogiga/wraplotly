"""
Mother classes of wraplotly.

The class draw is used for classes that directly plot graphs like line.

The class arrange is used for classes that arrange plots in a certain way,
such like Grid.
"""
import pandas
import warnings
import numpy as np
import plotly.graph_objects as go
from plotly_resampler import register_plotly_resampler


""" === some helper function """
def count_nans_in_df_and_alert(df, x):
    c = df[x].isna().sum()

    if c >= 1:
        warnings.warn(f"Column '{x}' of the passed dataframe contains {c} occurence(s) of NaN. This might result in faulty plots.")

def count_nans_and_alert(l, arg):
    if isinstance(l, str):
        return 
    if isinstance(l, pandas.core.frame.DataFrame):
        l = l.values.tolist()
    
    c = np.count_nonzero(np.isnan(np.array(l)))
    if c >= 1:
        warnings.warn(f"Argument '{arg}' contains {c} occurence(s) of NaN. This might result in faulty plots.")


class draw:
    _min_points_before_resampling = 75000
    _wraplotly_context: str = "px"
    _resample = False
    x_name, y_name = "", ""

    def __register_axis_names__(self, x, y):
        if x and isinstance(x, str):
            self.x_name = x
        if y and isinstance(y, str):
            self.y_name = y

    def __resampler__(self):
        self._points = 0

        if self.df is not None:
            self._points += max(self.df.shape)
        if self.x is not None and not isinstance(self.x, str):
            self._points += len(self.x)
        if self.y is not None and not isinstance(self.y, str):
            self._points += len(self.y)

        self._resample = self._points > self._min_points_before_resampling

    def __prepare_2d_plot_args__(self, df, x, y):
        # In order to call line without a dataframe in arragements
        if df is not None and x is not None and y is None:
            y = x
            x = df
            df = None
        if df is not None and x is None and y is None:
            y = df
            df = None
        return df, x, y

    def __check_for_nans__(self):
        if self.df is not None:
            if self.x is not None:
                count_nans_in_df_and_alert(self.df, self.x)
            if self.y is not None:
                count_nans_in_df_and_alert(self.df, self.y)
        else:
            if self.x is not None:
                count_nans_and_alert(self.x, 'x')
            if self.y is not None:
                count_nans_and_alert(self.y, 'y')

    def __px_to_go_bad_conversion_errors__(self):
        if "name" in self.kwargs:
            raise ValueError("Key argument 'name' should not be used outside of arrange methods. Use 'title' instead.")

    @property
    def fig(self):
        return self.__plot_fn__()

    def show(self):
        if self._resample:
            register_plotly_resampler(mode='auto')
            warnings.warn(f"Data was too large (~{self._points} entries) and had to be downsampled using plotly-resampler.")
            self._wraplotly_context = "go"
            self._fig = go.Figure()
            for obj in self.__plot_fn__():
                self._fig.add_trace(obj)
            self._fig.show()
        else:
            self.__plot_fn__().show()

    def __repr__(self):
        self.show(); return ''


class arrange:
    _fig = None

    def build_fig(self):
        raise NameError("Arrange object does not define a 'build_fig' method.")

    def __plot_fn__(self):
        self.build_fig(); return self._fig

    @property
    def fig(self):
        if self._fig is None:
            self.build_fig()
        return self._fig

    def show(self):
        self.build_fig(); return self._fig.show()

    def __repr__(self):
        self.show(); return ''