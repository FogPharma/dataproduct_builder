import pandas as pd
import numpy as np
from typing import Dict, List, Union

"""
column_ops.py

This module provides utilities to manipulate DataFrame columns. These functions are intended to be used
as part of a larger data product creation pipeline. For row manipulations see row_ops.py and cros row-column
manipulations see grid_ops.py.
"""

# staple lists
S_STAPLES=['S4','S5','S6','S7','S8','S9','PyrS','PyrS1','PyrS2','PyrS3','PyrS4','PyrS5','SgN','SdN','SeN','PL3']
R_STAPLES=['R4','R5','R6','R7','R8','R9','PyrR','PyrR1','PyrR2','PyrR3','PyrR4','PyrR5','RgN','RdN','ReN','PD3']
A_STAPLES=['Az','Az1','Az2','Az3','SPip','SPip1','SPip2','SPip3']
STITCHES=['B4','B5','B6','B7','B8','B9']
EXTRA_STAPLES=['PD3Lac']
WAHL_STAPLES=['%Cys','%dCys','Cys','dCys', 'aMeC', '%aMeC']


def rename_columns(df: pd.DataFrame, col_mapping: Dict[str, str]) -> pd.DataFrame:
    """
    Rename columns in a DataFrame based on a provided mapping.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        col_mapping (dict): Dictionary mapping current column names to new names.

    Returns:
        pd.DataFrame: A new DataFrame with columns renamed.
    """
    return df.rename(columns=col_mapping)


def drop_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Drop specified columns from the DataFrame.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        columns (List[str]): List of column names to drop.

    Returns:
        pd.DataFrame: DataFrame without the specified columns.
    """
    return df.drop(columns=columns)


# Function to concatenate specific columns in each row
def concat_and_pad_aas(df: pd.DataFrame, cols_to_concat: List[str], output_col: str,  pad: bool,) -> pd.DataFrame:
    """
    For a list of AAs column names concatenate their contents with '-' and 
    replace NaN or empty cells with 'blank'.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        cols_to_concat (List[str]): List of column names to concatenate. e.g. ['Ncap', 'AA1', 'AA2', 'AA3', 'AA4', 'AA5', 'AA6', 'AA7', 'AA8', 'AA9',
        'AA10', 'AA11', 'AA12', 'AA13', 'AA14', 'AA15', 'AA16', 'AA17', 'AA18', 'AA19', 'Ccap']
        output_col (str): Name of the sequence column.
        pad (bool): Whether to pad the sequence with 'BLANK' if an AA col is blank for a sequence.

    Returns:
        pd.DataFrame: DataFrame with concatenated and padded sequence.
    """
    if pad:
        df[output_col] = df[cols_to_concat].fillna('BLANK').agg('-'.join, axis=1)
    else:
        df[output_col] = df[cols_to_concat].fillna('').agg('-'.join, axis=1).str.replace(r'-+', '-', regex=True)

    return df



def add_punctuation_staples_and_stitches(df: pd.DataFrame, col_name:str, output_col:str  ) -> pd.DataFrame:
    """
    Fix the staples and stitches in the DataFrame with the correct punctuation marks
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        col_name str: name of the sequence column.
        output_col str: name of the output column.
    Returns:
        pd.DataFrame: DataFrame with fixed staples and stitches.
    """ 
    # Create a copy of the DataFrame to avoid modifying the original
    dftemp = df.copy()

    stitch_staple_residues = S_STAPLES + R_STAPLES + A_STAPLES + EXTRA_STAPLES + WAHL_STAPLES

    ## get staples and add $ for normal staple residues and $$ for stitch residues if they dont aleady have a $
    for staple in stitch_staple_residues:
        dftemp[output_col]=dftemp[col_name].str.replace('-'+staple+'-','-$'+staple+'-')
    for stitch in STITCHES:
        dftemp[output_col]=dftemp[col_name].str.replace('-'+stitch+'-','-$$'+stitch+'-')
    
    return dftemp



def assign_class_labels(df: pd.DataFrame, input_col:str, threshold: Union[int, float, List[Union[int, float]]], output_col:str ) -> pd.DataFrame:
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
        df[output_col] = (df[input_col] > threshold).astype(int)
    
    elif isinstance(threshold, List[Union[int, float]]): ## multiclass classification
        sorted_thresholds = sorted(threshold)
        bins = [-np.inf] + sorted_thresholds + [np.inf]
        df[output_col] = pd.cut(df[input_col], bins=bins, labels=False, include_lowest=True)
    else:
        raise TypeError("Threshold must be a number or a list of numbers.")

    return df


def concatenate_stitches_and_staples(df: pd.DataFrame, input_col:str, output_col:str ) -> pd.DataFrame:  #TODO: this function is not working as expected
    """
    Concatenate the staples and stitches in the DataFrame to the same residue. This is useful for plsSAR analysis
    This function assumes that the staple and stitch residues are already marked with $ and $$ respectively.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        input_col str: name of the sequence column.
        output_col str: name of the output column.
    Returns:
        pd.DataFrame: DataFrame with concatenated staples and stitches.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    dftemp = df.copy()    

    def concatenate_staples_and_stitches_helper(input_str:str) -> str: 
        # fix punctuation in the staple lists 
        stitch_staple_residues =  ['$'+i for i in S_STAPLES + R_STAPLES + A_STAPLES + EXTRA_STAPLES] + ['$$' for i in STITCHES]
        wahl_staples = ['$'+i for i in WAHL_STAPLES]
        stitch_resiudes = ['$$' for i in STITCHES]
        lactam_residues = ['*']



        # Split the input string by "-"
        elements = input_str.split("-")

        # Identify staple/stitch and wahl residues and positions
        staple_residues = []
        staple_positions = []
        wahl_res_comp = []
        wahl_position_comp = []
        lactam_positions = []
        lactam_residues = []

        for position, residue in enumerate(elements):
            if any(tag in residue for tag in stitch_staple_residues):
                staple_residues.append(residue)
                staple_positions.append(position)
            if residue in wahl_staples:
                wahl_res_comp.append(residue)
                wahl_position_comp.append(position)
            if any(tag in residue for tag in lactam_residues):
                lactam_residues.append(residue)
                lactam_positions.append(position)

        # Group stitch/staple residues and handle "B5" condition
        i = 0
        while i < len(staple_residues) - 1:
            elements[staple_positions[i]] = f"{staple_residues[i]}{staple_residues[i+1]}"
            elements[staple_positions[i+1]] = "STAP"

            if staple_residues[i+1] in stitch_resiudes:
                if i + 2 < len(staple_residues):
                    elements[staple_positions[i+1]] = f"{elements[staple_positions[i]]}{staple_residues[i+2]}"
                    elements[staple_positions[i]] = "STAP"
                    elements[staple_positions[i+2]] = "STAP"
                    i += 2
                else:
                    i += 1
            else:
                i += 1

        # Group WAHL residues 7 positions apart
        i = 0
        while i < len(wahl_res_comp) - 1:
            if wahl_position_comp[i+1] - wahl_position_comp[i] == 7:
                elements[wahl_position_comp[i]] = f"{wahl_res_comp[i]}{wahl_res_comp[i+1]}"
                elements[wahl_position_comp[i+1]] = "WAHL"
                i += 1
            i += 1

        ## group lactams together
        while i < len(lactam_positions) - 1:
            elements[lactam_positions[i]] = f"{lactam_residues[i]}{lactam_residues[i+1]}"
            elements[lactam_positions[i+1]] = "LACT"
            i += 1
            
        # Join and return the final result
        return "-".join(elements)
    

    # Apply the function to the specified column
    dftemp[output_col] = dftemp[input_col].apply(concatenate_staples_and_stitches_helper)

    return dftemp


def concatenate_stitches_and_staples2(df: pd.DataFrame, input_col: str, output_col: str) -> pd.DataFrame:
    """
    Concatenate the staples and stitches in the DataFrame to the same residue. This is useful for plsSAR analysis.
    Works with both plain residue names and residues marked with $ (staple) or $$ (stitch) prefixes.
    
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        input_col (str): Name of the sequence column.
        output_col (str): Name of the output column.
    
    Returns:
        pd.DataFrame: DataFrame with concatenated staples and stitches.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    dftemp = df.copy()
    
    def concatenate_staples_and_stitches_helper2(input_str: str) -> str:
        
        # Define residue lists
        STITCH_STAPLE_RESIDUES =  S_STAPLES + R_STAPLES + A_STAPLES + EXTRA_STAPLES + STITCHES
        WAHL_RESIDUES =  WAHL_STAPLES
        STITCH_RESIDUES =  STITCHES
        LACTAMS = ["*"]
        
        # Helper function to strip $ and $$ prefixes
        def strip_prefix(residue):
            if residue.startswith("$$"):
                return residue[2:]
            elif residue.startswith("$"):
                return residue[1:]
            return residue
        
        # Helper function to check if residue contains any target string (works with or without prefix)
        def contains_target(residue, targets):
            stripped = strip_prefix(residue)
            return any(target in stripped for target in targets)
        
        # Helper function to check if residue ends with any target (works with or without prefix)
        def ends_with_target(residue, targets):
            stripped = strip_prefix(residue)
            return any(stripped.endswith(target) for target in targets)
        
        # Split the input string by "-"
        elements = input_str.split("-")
        
        # Identify staple/stitch and wahl residues and positions
        staple_residues = []
        staple_positions = []
        wahl_res_comp = []
        wahl_position_comp = []
        lactam_positions = []
        lactam_residues = []
        
        for position, residue in enumerate(elements):
            if contains_target(residue, STITCH_STAPLE_RESIDUES):
                staple_residues.append(residue)
                staple_positions.append(position)
            if ends_with_target(residue, WAHL_RESIDUES):
                wahl_res_comp.append(residue)
                wahl_position_comp.append(position)
            if contains_target(residue, LACTAMS):
                lactam_residues.append(residue)
                lactam_positions.append(position)
        
        # Group stitch/staple residues and handle stitch condition
        i = 0
        while i < len(staple_residues) - 1:
            elements[staple_positions[i]] = f"{staple_residues[i]}{staple_residues[i+1]}"
            elements[staple_positions[i+1]] = "STAP"
            
            if ends_with_target(staple_residues[i+1], STITCH_RESIDUES):
                if i + 2 < len(staple_residues):
                    elements[staple_positions[i+1]] = f"{elements[staple_positions[i]]}{staple_residues[i+2]}"
                    elements[staple_positions[i]] = "STAP"
                    elements[staple_positions[i+2]] = "STAP"
                    i += 2
                else:
                    i += 1
            else:
                i += 1
        
        # Group WAHL residues 7 positions apart
        i = 0
        while i < len(wahl_res_comp) - 1:
            if wahl_position_comp[i+1] - wahl_position_comp[i] == 7:
                elements[wahl_position_comp[i]] = f"{wahl_res_comp[i]}{wahl_res_comp[i+1]}"
                elements[wahl_position_comp[i+1]] = "WAHL"
                i += 1
            i += 1
        
        # Group lactams together
        i = 0
        while i < len(lactam_positions) - 1:
            elements[lactam_positions[i]] = f"{lactam_residues[i]}{lactam_residues[i+1]}"
            elements[lactam_positions[i+1]] = "LACT"
            i += 1
        
        # Join and return the final result
        return "-".join(elements)
    
    # Apply the function to the specified column
    dftemp[output_col] = dftemp[input_col].apply(concatenate_staples_and_stitches_helper2)
    
    return dftemp


def convert_to_pxc50_values(df: pd.DataFrame, input_col:str, unit:str = 'uM', output_col:str = 'pxc50_value') -> pd.DataFrame:
    """
    Convert the values in the input column to pxc50 values.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        input_col str: name of the column to convert.
        unit str: unit of the input column. Default is 'nM'. can also handle uM, M, and pM 
        output_col str: name of the output column.
    Returns:
        pd.DataFrame: DataFrame with converted values.
    """
    if unit == 'uM':
        df[output_col] = 6-np.log10(df[input_col])
    elif unit == 'M':
        df[output_col] = -np.log10(df[input_col])
    elif unit == 'pM':
        df[output_col] = 12-np.log10(df[input_col])
    elif unit == 'nM':
        df[output_col] = 9-np.log10(df[input_col])
    else:
        raise ValueError(f"Invalid unit: {unit}, must be one of: uM, M, pM, nM")
    return df

