import pandas
import warnings
import numpy as np


MIN_POINTS_BEFORE_RESAMPLING = 75000


def str_assertion(obj, name, header=""):
    if not isinstance(obj, str):
        raise TypeError(f"{header}: {name} should be of type 'str', got '{type(obj)}' instead.")


def itt_assertion(obj, name, header=""):
    try:
        len(obj)
    except:
        raise TypeError(f"{header}: {name} should be itterable (got faulty type '{type(obj)}'.).")


def ignored_warning(obj, name, header=""):
    if obj is not None:
        warnings.warn(f"{header}: {name} is ignored.")


def needs_resample(*args):
    nb_points = sum(len(arg) for arg in args if arg is not None and not isinstance(arg, str))
    return nb_points > MIN_POINTS_BEFORE_RESAMPLING


def count_nans_in_df_and_alert(df, *cols):
    for col in cols:
        if col is None:
            continue

        c = df[col].isna().sum()

        if c >= 1:
            warnings.warn(f"Column '{col}' of the passed dataframe contains {c} occurence(s) of NaN. This might result in faulty plots.")


def count_nans_and_alert(*args):
    for arg in args:
        if arg is None or isinstance(arg, str):
            continue

        if isinstance(arg, pandas.core.frame.DataFrame):
            l = arg.values.tolist()
            c = np.count_nonzero(np.isnan(np.array(l)))
            if c >= 1:
                warnings.warn(f"Argument '{arg}' contains {c} occurence(s) of NaN. This might result in faulty plots.")