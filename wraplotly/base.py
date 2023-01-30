"""
Mother classes of wraplotly.

The class draw is used for classes that directly plot graphs like line.

The class arrange is used for classes that arrange plots in a certain way,
such like Grid.
"""


class draw:
    _wraplotly_context: str = "px" # default is plotly express (easier to use)

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

    def __px_to_go_bad_conversion_errors__(self):
        if "name" in self.kwargs:
            raise ValueError("Key argument 'name' should not be used outside of arrange methods. Use 'title' instead.")

    def __plot_fn__(self):
        raise NameError("Draw object does not define a '__plot_fn__' internal method.")

    @property
    def fig(self):
        return self.__plot_fn__()

    def show(self):
        self.__plot_fn__().show()

    def __repr__(self):
        self.show(); return ''


class arrange:
    _fig = None

    def build_fig(self):
        raise NameError("Arrange object does not define a 'build_fig' method.")

    @property
    def fig(self):
        if self._fig is None:
            self.build_fig()
        return self._fig

    def show(self):
        self.build_fig(); return self._fig.show()

    def __repr__(self):
        self.show(); return ''