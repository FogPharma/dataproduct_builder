"""
DataProduct Builder - A comprehensive data processing pipeline for peptide sequence analysis and general data manipulation.

This package provides utilities for:
- Column operations (renaming, dropping, concatenating amino acids, etc.)
- Row operations (filtering, sorting, sampling, validation, etc.)
- Frame operations (aggregation, pandas/numpy function application)
- Configuration-based pipeline execution
- Command-line interface for easy usage
"""

__version__ = "0.1.0"
__author__ = "FogPharma Data Science Team"
__email__ = "datascience@fogpharma.com"

# Import main modules for easy access
from . import column_ops
from . import row_ops
from . import frame_ops
from . import quality_checks
from . import config_executor

# Make key functions easily accessible
from .config_executor import run_from_config, create_example_config
from .column_ops import (
    rename_columns,
    drop_columns,
    concat_and_pad_aas,
    add_punctuation_staples_and_stitches,
    assign_class_labels,
    concatenate_stitches_and_staples,
    concatenate_stitches_and_staples2,
)
from .row_ops import (
    drop_duplicates,
    filter_rows,
    sort_rows,
    sample_rows,
    shuffle_rows,
    validate_rows,
    remove_empty_rows,
)
from .frame_ops import (
    aggregate_dataframe,
    aggregate_with_custom_functions,
    aggregate_with_column_functions,
    apply_pandas_function,
    apply_numpy_function,
)
from .quality_checks import (
    check_row_count,
    check_column_count,
    check_missing_values,
    check_data_types,
)

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    
    # Modules
    "column_ops",
    "row_ops", 
    "frame_ops",
    "quality_checks",
    "config_executor",
    
    # Config functions
    "run_from_config",
    "create_example_config",
    
    # Column operations
    "rename_columns",
    "drop_columns",
    "concat_and_pad_aas",
    "add_punctuation_staples_and_stitches",
    "assign_class_labels",
    "concatenate_stitches_and_staples",
    "concatenate_stitches_and_staples2",
    
    # Row operations
    "drop_duplicates",
    "filter_rows",
    "sort_rows",
    "sample_rows",
    "shuffle_rows",
    "validate_rows",
    "remove_empty_rows",
    
    # Frame operations
    "aggregate_dataframe",
    "aggregate_with_custom_functions",
    "aggregate_with_column_functions",
    "aggregate_peptide_data",
    "apply_pandas_function",
    "apply_numpy_function",
    
    # Quality checks
    "check_row_count",
    "check_column_count",
    "check_missing_values",
    "check_data_types",
]
