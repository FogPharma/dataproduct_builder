import pandas as pd
from typing import Union, Optional


def check_row_count(df: pd.DataFrame, expected_count: Optional[int] = None, 
                   min_count: Optional[int] = None, max_count: Optional[int] = None) -> str:
    """
    Check if DataFrame has the expected number of rows.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        expected_count (Optional[int]): Exact expected row count.
        min_count (Optional[int]): Minimum acceptable row count.
        max_count (Optional[int]): Maximum acceptable row count.
        
    Returns:
        str: Validation message indicating pass/fail status.
        
    Example:
        >>> df = pd.DataFrame({'A': [1, 2, 3]})
        >>> result = check_row_count(df, expected_count=3)
        >>> print(result)
        "✅ Row count validation passed: 3 rows (expected: 3)"
    """
    actual_count = len(df)
    
    if expected_count is not None:
        if actual_count == expected_count:
            return f"✅ Row count validation passed: {actual_count} rows (expected: {expected_count})"
        else:
            return f"❌ Row count validation failed: {actual_count} rows (expected: {expected_count})"
    
    if min_count is not None and actual_count < min_count:
        return f"❌ Row count validation failed: {actual_count} rows (minimum: {min_count})"
    
    if max_count is not None and actual_count > max_count:
        return f"❌ Row count validation failed: {actual_count} rows (maximum: {max_count})"
    
    # If we get here, all checks passed
    return f"✅ Row count validation passed: {actual_count} rows"


def check_column_count(df: pd.DataFrame, expected_count: Optional[int] = None,
                      min_count: Optional[int] = None, max_count: Optional[int] = None) -> str:
    """
    Check if DataFrame has the expected number of columns.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        expected_count (Optional[int]): Exact expected column count.
        min_count (Optional[int]): Minimum acceptable column count.
        max_count (Optional[int]): Maximum acceptable column count.
        
    Returns:
        str: Validation message indicating pass/fail status.
    """
    actual_count = len(df.columns)
    
    if expected_count is not None:
        if actual_count == expected_count:
            return f"✅ Column count validation passed: {actual_count} columns (expected: {expected_count})"
        else:
            return f"❌ Column count validation failed: {actual_count} columns (expected: {expected_count})"
    
    if min_count is not None and actual_count < min_count:
        return f"❌ Column count validation failed: {actual_count} columns (minimum: {min_count})"
    
    if max_count is not None and actual_count > max_count:
        return f"❌ Column count validation failed: {actual_count} columns (maximum: {max_count})"
    
    return f"✅ Column count validation passed: {actual_count} columns"


def check_missing_values(df: pd.DataFrame, threshold: float = 0.1) -> str:
    """
    Check if DataFrame has excessive missing values.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        threshold (float): Maximum acceptable proportion of missing values (0.0 to 1.0).
        
    Returns:
        str: Validation message indicating pass/fail status.
    """
    total_cells = df.size
    missing_cells = df.isnull().sum().sum()
    missing_proportion = missing_cells / total_cells if total_cells > 0 else 0
    
    if missing_proportion <= threshold:
        return f"✅ Missing values validation passed: {missing_proportion:.2%} missing (threshold: {threshold:.2%})"
    else:
        return f"❌ Missing values validation failed: {missing_proportion:.2%} missing (threshold: {threshold:.2%})"


def check_data_types(df: pd.DataFrame, expected_types: dict) -> str:
    """
    Check if DataFrame columns have expected data types.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to check.
        expected_types (dict): Dictionary mapping column names to expected dtypes.
        
    Returns:
        str: Validation message indicating pass/fail status.
    """
    failed_checks = []
    
    for column, expected_dtype in expected_types.items():
        if column not in df.columns:
            failed_checks.append(f"Column '{column}' not found")
        elif df[column].dtype != expected_dtype:
            failed_checks.append(f"Column '{column}': expected {expected_dtype}, got {df[column].dtype}")
    
    if not failed_checks:
        return f"✅ Data types validation passed: {len(expected_types)} columns checked"
    else:
        return f"❌ Data types validation failed: {'; '.join(failed_checks)}"
