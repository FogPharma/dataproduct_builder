import pandas as pd
import numpy as np
from typing import Dict, List, Union


"""
row_ops.py

This module provides utilities to manipulate DataFrame rows. These functions are intended to be used
as part of a larger data product creation pipeline. For columns manipulations see column_ops.py and cross
row-column manipulations see grid_ops.py.
"""


def assign_class_labels(df: pd.DataFrame, input_col:str, threshold: Union[str, Dic]), output_col:str ) -> pd.DataFrame:
    """
    Assigns class labels to a DataFrame based on a single threshold or a list of thresholds.

    Parameters:
    - df: pd.DataFrame
    - input_col: str, column name to apply the threshold(s)
    - threshold: float or list of floats
        - If float: assigns binary labels (0 or 1)
        - If list: assigns multiclass labels (0, 1, 2, ...) based on bins
    - output_col: str, name of the column to store the class labels

    Returns:
    - df: pd.DataFrame with new column output_col containing class labels
    """

    if isinstance(threshold, (int, float)):  # Binary classification
        df[label_col] = (df[col] > threshold).astype(int)

    elif isinstance(threshold, (list, tuple, np.ndarray)):
        sorted_thresholds = sorted(threshold)
        bins = [-np.inf] + sorted_thresholds + [np.inf]
        df[label_col] = pd.cut(df[col], bins=bins, labels=False, include_lowest=True)

    else:
        raise TypeError("Threshold must be a number or a list of numbers.")

    return df


