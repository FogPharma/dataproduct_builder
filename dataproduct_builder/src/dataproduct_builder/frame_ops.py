import pandas as pd
import numpy as np
from typing import Dict, List, Union

"""
frame_ops.py

This module provides utilities to manipulate both DataFrame rows and cols. 
These functions are intended to be used as part of a larger data product creation pipeline.
For columns manipulations see column_ops.py and row manipulations see row_ops_ops.py.
"""

def aggregate_dataframe(df: pd.DataFrame, groupby_cols: Union(str, List) agg_dict: Dict) -> pd.DataFrame:
    """
    Aggregates a DataFrame with custom aggregation functions and output column names.

    Parameters:
    - df: pd.DataFrame
    - groupby_cols: str or list of str, column(s) to group by
    - agg_dict: dict, structured like:
        {
            'original_col1': {
                'new_col_name1': 'agg_func',
                'new_col_name2': custom_func,
            },
            ...
        }

    Returns:
    - pd.DataFrame with custom-named aggregated columns
    """
    if isinstance(groupby_cols, str):
        groupby_cols = [groupby_cols]

    # Build the named aggregation dict
    named_aggs = {}
    for source_col, aggs in agg_dict.items():
        for new_col, func in aggs.items():
            named_aggs[new_col] = (source_col, func)

    aggregated_df = df.groupby(groupby_cols).agg(**named_aggs).reset_index()

    return aggregated_df



def apply_pandas_function(df, func_name, *args, **kwargs):
    """
    Applies any pandas DataFrame method to the given DataFrame.

    Parameters:
    - df: pd.DataFrame
    - func_name: str, name of the pandas DataFrame method (e.g., 'sort_values', 'fillna')
    - *args: positional arguments for the method
    - **kwargs: keyword arguments for the method

    Returns:
    - pd.DataFrame or result of the applied function
    """
    if not hasattr(df, func_name):
        raise AttributeError(f"'DataFrame' object has no method named '{func_name}'")

    func = getattr(df, func_name)
    return func(*args, **kwargs)




def apply_numpy_function(array, func_name, *args, **kwargs):
    """
    Applies a NumPy function to an array with optional arguments.

    Parameters:
    - array: np.ndarray or array-like
    - func_name: str, name of the NumPy function (e.g., 'mean', 'sum', 'argmax')
    - *args: positional arguments for the function
    - **kwargs: keyword arguments for the function

    Returns:
    - Result of the NumPy function
    """
    if not hasattr(np, func_name):
        raise AttributeError(f"'numpy' has no function named '{func_name}'")

    func = getattr(np, func_name)
    return func(array, *args, **kwargs)

