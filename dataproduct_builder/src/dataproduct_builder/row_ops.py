import pandas as pd
import numpy as np
from typing import Dict, List, Union, Any, Optional
import random


"""
row_ops.py

This module provides utilities to manipulate DataFrame rows. These functions are intended to be used
as part of a larger data product creation pipeline. For columns manipulations see column_ops.py and cross
row-column manipulations see grid_ops.py.
"""

def drop_duplicates(df: pd.DataFrame, subset: Union[str, List[str]], keep: Union[str, None] = 'first') -> pd.DataFrame:
    """
    Drop duplicates from a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        subset (Union[str, List[str]]): Column name(s) to consider for identifying duplicates.
        keep (Union[str, None]): Which duplicates to keep. Options: 'first', 'last', False.
        
    Returns:
        pd.DataFrame: DataFrame with duplicates removed.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 1, 2], 'B': [3, 3, 4]})
        >>> result = drop_duplicates(df, subset='A')
        >>> print(result)
           A  B
        0  1  3
        2  2  4
    """
    return df.drop_duplicates(subset=subset, keep=keep)


def filter_rows(df: pd.DataFrame, column: str, operator: str, value: Any) -> pd.DataFrame:
    """
    Filter rows from a DataFrame based on a column condition (safe alternative to eval).
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        column (str): Column name to filter on.
        operator (str): Comparison operator ('==', '!=', '>', '<', '>=', '<=', 'in', 'not_in').
        value (Any): Value to compare against.
        
    Returns:
        pd.DataFrame: Filtered DataFrame.
        
    Raises:
        ValueError: If column doesn't exist or operator is not supported.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> result = filter_rows(df, 'A', '>', 1)
        >>> print(result)
           A  B
        1  2  5
        2  3  6
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame")
    
    valid_operators = ['==', '!=', '>', '<', '>=', '<=', 'in', 'not_in']
    if operator not in valid_operators:
        raise ValueError(f"Operator '{operator}' not supported. Use one of: {valid_operators}")
    
    if operator == '==':
        return df[df[column] == value]
    elif operator == '!=':
        return df[df[column] != value]
    elif operator == '>':
        return df[df[column] > value]
    elif operator == '<':
        return df[df[column] < value]
    elif operator == '>=':
        return df[df[column] >= value]
    elif operator == '<=':
        return df[df[column] <= value]
    elif operator == 'in':
        return df[df[column].isin(value)]
    elif operator == 'not_in':
        return df[~df[column].isin(value)]


def sort_rows(df: pd.DataFrame, by: Union[str, List[str]], ascending: Union[bool, List[bool]] = True) -> pd.DataFrame:
    """
    Sort DataFrame rows by one or more columns.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        by (Union[str, List[str]]): Column name(s) to sort by.
        ascending (Union[bool, List[bool]]): Sort order(s).
        
    Returns:
        pd.DataFrame: Sorted DataFrame.
        
    Example:
        >>> df = pd.DataFrame({'A': [3, 1, 2], 'B': [6, 4, 5]})
        >>> result = sort_rows(df, by='A')
        >>> print(result)
           A  B
        1  1  4
        2  2  5
        0  3  6
    """
    return df.sort_values(by=by, ascending=ascending)


def sample_rows(df: pd.DataFrame, n: Optional[int] = None, frac: Optional[float] = None, 
                random_state: Optional[int] = None, replace: bool = False) -> pd.DataFrame:
    """
    Randomly sample rows from a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        n (Optional[int]): Number of rows to sample.
        frac (Optional[float]): Fraction of rows to sample (0.0 to 1.0).
        random_state (Optional[int]): Random seed for reproducibility.
        replace (bool): Whether to sample with replacement.
        
    Returns:
        pd.DataFrame: Sampled DataFrame.
        
    Raises:
        ValueError: If neither n nor frac is specified, or both are specified.
        
    Example:
        >>> df = pd.DataFrame({'A': range(10), 'B': range(10, 20)})
        >>> result = sample_rows(df, n=3, random_state=42)
        >>> print(result)
           A   B
        6  6  16
        3  3  13
        7  7  17
    """
    if n is None and frac is None:
        raise ValueError("Either 'n' or 'frac' must be specified")
    if n is not None and frac is not None:
        raise ValueError("Cannot specify both 'n' and 'frac'")
    
    return df.sample(n=n, frac=frac, random_state=random_state, replace=replace)


def shuffle_rows(df: pd.DataFrame, random_state: Optional[int] = None) -> pd.DataFrame:
    """
    Shuffle the rows of a DataFrame.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        random_state (Optional[int]): Random seed for reproducibility.
        
    Returns:
        pd.DataFrame: DataFrame with shuffled rows.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> result = shuffle_rows(df, random_state=42)
        >>> print(result)
           A  B
        2  3  6
        0  1  4
        1  2  5
    """
    return df.sample(frac=1.0, random_state=random_state).reset_index(drop=True)


def validate_rows(df: pd.DataFrame, conditions: Dict[str, Any]) -> pd.DataFrame:
    """
    Filter rows that meet all specified validation conditions.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        conditions (Dict[str, Any]): Dictionary mapping column names to validation values.
                                   Use tuples for operators: ('column', 'operator', value).
        
    Returns:
        pd.DataFrame: DataFrame with rows that pass all validations.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
        >>> conditions = {'A': ('A', '>', 1), 'B': ('B', '<', 6)}
        >>> result = validate_rows(df, conditions)
        >>> print(result)
           A  B
        1  2  5
    """
    mask = pd.Series([True] * len(df), index=df.index)
    
    for col, condition in conditions.items():
        if isinstance(condition, tuple) and len(condition) == 3:
            col_name, operator, value = condition
            if col_name not in df.columns:
                raise ValueError(f"Column '{col_name}' not found in DataFrame")
            
            if operator == '==':
                mask &= (df[col_name] == value)
            elif operator == '!=':
                mask &= (df[col_name] != value)
            elif operator == '>':
                mask &= (df[col_name] > value)
            elif operator == '<':
                mask &= (df[col_name] < value)
            elif operator == '>=':
                mask &= (df[col_name] >= value)
            elif operator == '<=':
                mask &= (df[col_name] <= value)
            elif operator == 'in':
                mask &= df[col_name].isin(value)
            elif operator == 'not_in':
                mask &= ~df[col_name].isin(value)
            else:
                raise ValueError(f"Unsupported operator: {operator}")
        else:
            # Simple equality check
            if col not in df.columns:
                raise ValueError(f"Column '{col}' not found in DataFrame")
            mask &= (df[col] == condition)
    
    return df[mask]


def remove_empty_rows(df: pd.DataFrame, subset: Optional[Union[str, List[str]]] = None) -> pd.DataFrame:
    """
    Remove rows with missing values (NaN, None, empty strings).
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        subset (Optional[Union[str, List[str]]]): Columns to check for missing values.
                                                If None, checks all columns.
        
    Returns:
        pd.DataFrame: DataFrame with empty rows removed.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, None, 3], 'B': [4, '', 6]})
        >>> result = remove_empty_rows(df)
        >>> print(result)
           A  B
        0  1  4
        2  3  6
    """
    if subset is None:
        return df.dropna()
    else:
        return df.dropna(subset=subset)




##todo: 
## def filter_on_fingerprint_similarity_dist_to_self() ## operation to augment a needed subset with dissimilary data from a less desierable subset of the dataframe (especially useful when prioritizing internal vs external data) 
## def all sorts of external data selection and cleaning menthods such as: 
###### removing external data with inequalities within  thresholds determined by internal data for relevan assay, 
###### removing inequality data where not helpful (ineuqality data is often found in external data sources including patents) 
###### 