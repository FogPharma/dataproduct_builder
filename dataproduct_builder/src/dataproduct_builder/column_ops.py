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
def concat_and_pad_aas(df: pd.DataFrame, cols_to_concat: List[str], output_col: str) -> pd.DataFrame:
    """
    For a list of AAs column names concatenate their contents with '-' and 
    replace NaN or empty cells with 'blank'.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        cols_to_concat (List[str]): List of column names to drop. e.g. ['Ncap', 'AA1', 'AA2', 'AA3', 'AA4', 'AA5', 'AA6', 'AA7', 'AA8', 'AA9',
        'AA10', 'AA11', 'AA12', 'AA13', 'AA14', 'AA15', 'AA16', 'AA17', 'AA18', 'AA19', 'Ccap']
        output_col (str): Name of the sequence column.

    Returns:
        pd.DataFrame: DataFrame with concatenated and padded sequence.
    """
    def concat_aas(row: pd.Series, cols_to_concat: List[str]) -> str:
        """
        Concatenate amino acid columns for a single row.

        Parameters:
            row (pd.Series): A single row of the DataFrame.
            cols_to_concat (List[str]): List of column names to concatenate.

        Returns:
            str: Concatenated string of amino acids.
        """
        # Replace NaN or empty cells with 'blank' and join with '-'
        return '-'.join([str(row[col]) if pd.notnull(row[col]) and row[col] != '' else 'blank' for col in cols_to_concat])
    
    # Apply the concatenation function to each row
    df[output_col] = df.apply(lambda row: concat_aas(row, cols_to_concat), axis=1)

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

    non_stitch_staple_residues = S_STAPLES + R_STAPLES + A_STAPLES + EXTRA_STAPLES + WAHL_STAPLES

    ## get staples and add $ for normal staple residues and $$ for stitch residues if they dont aleady have a $
    for staple in non_stitch_staple_residues:
        dftemp[output_col]=dftemp[col_name].str.replace('-'+staple+'-','-$'+staple+'-')
    for stitch in STITCHES:
        dftemp[output_col]=dftemp[col_name].str.replace('-'+stitch+'-','-$$'+stitch+'-')
    
    return dftemp



    

def concatenate_stitches_and_staples(df: pd.DataFrame, col_name:str, output_col:str ) -> pd.DataFrame:
    """
    Concatenate the staples and stitches in the DataFrame to the same residue. This is useful for plsSAR analysis
    This function assumes that the staple and stitch residues are already marked with $ and $$ respectively.
    Parameters:
        df (pd.DataFrame): The input DataFrame.
        col_name str: name of the sequence column.
        output_col str: name of the output column.
    Returns:
        pd.DataFrame: DataFrame with concatenated staples and stitches.
    """
    # Create a copy of the DataFrame to avoid modifying the original
    dftemp = df.copy()    

    def concatenate_staples_and_stitches(input_string:str) -> str:
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
                    elements[staple_positions[i+1]] = f"{elements[positions[i]]}{staple_residues[i+2]}"
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
    dftemp[output_col] = dftemp[col_name].apply(concatenate_staples_and_stitches)

    return dftemp





