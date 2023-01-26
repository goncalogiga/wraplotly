import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wraplotly.wraplotly import draw


class line(draw):
    type = "scatter"
    
    def __init__(self, df: pd.DataFrame=None, x: str=None, y: str=None, **kwargs):
        self.kwargs = kwargs
        self.df = df
        self.x = x
        self.y = y

    def __plot_fn__(self):
        if self._wraplotly_context == "px":
            return px.line(self.df, self.x, self.y, **self.kwargs)
        elif self._wraplotly_context == "go" and self.df:
            return go.Scatter(x=self.df[self.x], y=self.df[self.y], **self.kwargs)
        elif self._wraplotly_context == "go":
            return go.Scatter(x=self.x, y=self.y, **self.kwargs)