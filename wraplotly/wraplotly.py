"""
Mother classes of wraplotly.

The class draw is used for classes that directly plot graphs like line.

The class arrange is used for classes that arrange plots in a certain way,
such like Grid.
"""


class draw:
    _wraplotly_context: str = "px" # default is plotly express (easier to use)

    def __plot_fn__(self):
        raise NameError("Draw object does not define a '__plot_fn__' internal method.")

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
            raise RuntimeError("Figure (fig) is not yet built. Please run the method build_fig() before accessing the 'fig' object.")
        return self._fig

    def show(self):
        self.build_fig(); return self._fig.show()

    def __repr__(self):
        self.show(); return ''