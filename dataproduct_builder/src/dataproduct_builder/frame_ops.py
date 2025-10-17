import pandas as pd
import numpy as np
from typing import Dict, List, Union

"""
frame_ops.py

This module provides utilities to manipulate both DataFrame rows and cols. 
These functions are intended to be used as part of a larger data product creation pipeline.
For columns manipulations see column_ops.py and row manipulations see row_ops_ops.py.
"""

def aggregate_dataframe(df: pd.DataFrame, groupby_cols: Union[str, List], agg_dict: Dict) -> pd.DataFrame:
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


def aggregate_with_custom_functions(df: pd.DataFrame, groupby_cols: Union[str, List], 
                                  agg_dict: Dict, custom_functions: Dict = None) -> pd.DataFrame:
    """
    Aggregates a DataFrame with support for custom functions via string references.
    
    Parameters:
    - df: pd.DataFrame
    - groupby_cols: str or list of str, column(s) to group by
    - agg_dict: dict, structured like:
        {
            'original_col1': {
                'new_col_name1': 'agg_func_or_custom_name',
                'new_col_name2': 'median',
            },
            ...
        }
    - custom_functions: dict, mapping custom function names to actual functions:
        {
            'set_join': lambda x: ', '.join(sorted(str(v) for v in set(x) if pd.notna(v))),
            'custom_median': lambda x: x.median(),
        }

    Returns:
    - pd.DataFrame with custom-named aggregated columns
    
    Example:
        >>> custom_funcs = {
        ...     'set_join': lambda x: ', '.join(sorted(str(v) for v in set(x) if pd.notna(v)))
        ... }
        >>> agg_dict = {
        ...     'ID': {'ID_aggregated': 'set_join'},
        ...     'Score': {'Score_median': 'median'}
        ... }
        >>> result = aggregate_with_custom_functions(df, 'Parent ID', agg_dict, custom_funcs)
    """
    if isinstance(groupby_cols, str):
        groupby_cols = [groupby_cols]
    
    if custom_functions is None:
        custom_functions = {}
    
    # Build the named aggregation dict
    named_aggs = {}
    for source_col, aggs in agg_dict.items():
        for new_col, func_name in aggs.items():
            # Check if it's a custom function
            if func_name in custom_functions:
                func = custom_functions[func_name]
            else:
                # Use pandas built-in function
                func = func_name
            
            named_aggs[new_col] = (source_col, func)

    aggregated_df = df.groupby(groupby_cols).agg(**named_aggs).reset_index()

    return aggregated_df


def aggregate_with_column_functions(df: pd.DataFrame, groupby_cols: Union[str, List], 
                                  column_functions: Dict, add_count_column: bool = False,
                                  count_column_name: str = "row_count") -> pd.DataFrame:
    """
    Aggregates a DataFrame where each column can have its own aggregation function.
    
    This function allows you to specify aggregation functions for each column directly
    in the configuration, making it much more flexible than predefined functions.
    
    Parameters:
    - df: pd.DataFrame
    - groupby_cols: str or list of str, column(s) to group by
    - column_functions: dict, mapping column names to aggregation functions:
        {
            'ID': 'set_join',
            'Score': 'median',
            'Name': 'first',
            'Category': 'set_join',
            ...
        }
    - add_count_column: bool, whether to add a column showing count of aggregated rows
    - count_column_name: str, name of the count column (default: "row_count")
    
    Returns:
    - pd.DataFrame with aggregated data
    
    Example:
        >>> column_funcs = {
        ...     'ID': 'set_join',
        ...     'IC50': 'median',
        ...     'Sequence': 'first'
        ... }
        >>> result = aggregate_with_column_functions(df, 'Parent ID', column_funcs, add_count_column=True)
    """
    if isinstance(groupby_cols, str):
        groupby_cols = [groupby_cols]
    
    # Define built-in custom functions
    def set_join(x):
        """Join unique non-null values with commas."""
        return ', '.join(sorted(str(v) for v in set(x) if pd.notna(v)))
    
    # Map function names to actual functions
    function_map = {
        'set_join': set_join,
        'median': 'median',
        'mean': 'mean',
        'sum': 'sum',
        'count': 'count',
        'first': 'first',
        'last': 'last',
        'min': 'min',
        'max': 'max',
        'std': 'std',
        'var': 'var',
    }
    
    # Build aggregation dictionary
    agg_dict = {}
    for col, func_name in column_functions.items():
        if col in df.columns:
            if func_name in function_map:
                agg_dict[col] = function_map[func_name]
            else:
                # Use the function name directly (pandas built-in)
                agg_dict[col] = func_name
    
    
    # Perform aggregation
    result = df.groupby(groupby_cols, dropna=False).agg(agg_dict).reset_index()
    
    # Add count column if requested
    if add_count_column:
        # Count the number of rows in each group
        count_series = df.groupby(groupby_cols, dropna=False).size()
        result[count_column_name] = result[groupby_cols[0]].map(count_series)

    
    return result



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

