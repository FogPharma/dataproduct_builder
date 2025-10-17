import json
import yaml
import pandas as pd
from typing import Dict, Any, Union, List
from pathlib import Path
import logging

# Import all modules
from dataproduct_builder import column_ops, row_ops, frame_ops, quality_checks

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comprehensive operation map for all functions
OPERATION_MAP = {
    # Column operations
    'rename_columns': column_ops.rename_columns,
    'drop_columns': column_ops.drop_columns,
    'concat_and_pad_aas': column_ops.concat_and_pad_aas,
    'add_punctuation_staples_and_stitches': column_ops.add_punctuation_staples_and_stitches,
    'assign_class_labels': column_ops.assign_class_labels,
    'concatenate_stitches_and_staples': column_ops.concatenate_stitches_and_staples,
    'concatenate_stitches_and_staples2': column_ops.concatenate_stitches_and_staples2,
    
    # Row operations
    'drop_duplicates': row_ops.drop_duplicates,
    'filter_rows': row_ops.filter_rows,
    'sort_rows': row_ops.sort_rows,
    'sample_rows': row_ops.sample_rows,
    'shuffle_rows': row_ops.shuffle_rows,
    'validate_rows': row_ops.validate_rows,
    'remove_empty_rows': row_ops.remove_empty_rows,
    
    # Frame operations
    'aggregate_dataframe': frame_ops.aggregate_dataframe,
    'aggregate_with_custom_functions': frame_ops.aggregate_with_custom_functions,
    'aggregate_with_column_functions': frame_ops.aggregate_with_column_functions,
    'apply_pandas_function': frame_ops.apply_pandas_function,
    'apply_numpy_function': frame_ops.apply_numpy_function,
    
    # Quality checks
    'check_row_count': quality_checks.check_row_count,
    'check_column_count': quality_checks.check_column_count,
    'check_missing_values': quality_checks.check_missing_values,
    'check_data_types': quality_checks.check_data_types,
}


def load_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load configuration from JSON or YAML file.
    
    Parameters:
        config_path (Union[str, Path]): Path to configuration file
        
    Returns:
        Dict[str, Any]: Configuration dictionary
        
    Raises:
        FileNotFoundError: If config file doesn't exist
        ValueError: If file format is not supported
    """
    config_path = Path(config_path)
    
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    
    with open(config_path, 'r') as f:
        if config_path.suffix.lower() == '.json':
            config = json.load(f)
        elif config_path.suffix.lower() in ['.yaml', '.yml']:
            config = yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {config_path.suffix}")
    
    return config


def validate_config(config: Dict[str, Any]) -> None:
    """
    Validate configuration structure and required fields.
    
    Parameters:
        config (Dict[str, Any]): Configuration dictionary
        
    Raises:
        ValueError: If configuration is invalid
    """
    required_fields = ['input_path', 'steps']
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    if not isinstance(config['steps'], list):
        raise ValueError("'steps' must be a list")
    
    for i, step in enumerate(config['steps']):
        if 'operation' not in step:
            raise ValueError(f"Step {i}: Missing 'operation' field")
        
        operation = step['operation']
        if operation not in OPERATION_MAP:
            available_ops = list(OPERATION_MAP.keys())
            raise ValueError(f"Step {i}: Unknown operation '{operation}'. Available: {available_ops}")


def execute_step(df: pd.DataFrame, step: Dict[str, Any], step_index: int) -> pd.DataFrame:
    """
    Execute a single configuration step.
    
    Parameters:
        df (pd.DataFrame): Input DataFrame
        step (Dict[str, Any]): Step configuration
        step_index (int): Step index for error reporting
        
    Returns:
        pd.DataFrame: Result DataFrame
        
    Raises:
        Exception: If step execution fails
    """
    operation = step['operation']
    params = step.get('params', {})
    
    try:
        logger.info(f"Executing step {step_index + 1}: {operation}")
        logger.debug(f"Parameters: {params}")
        
        func = OPERATION_MAP[operation]
        result = func(df, **params)
        
        if isinstance(result, str):
            # Quality check result (validation message)
            logger.info(f"Validation result: {result}")
            return df
        else:
            # DataFrame operation result
            logger.info(f"Step completed. DataFrame shape: {result.shape}")
            return result
            
    except Exception as e:
        logger.error(f"Error in step {step_index + 1} ({operation}): {str(e)}")
        raise


def run_from_config(config_path: Union[str, Path], output_path: Union[str, Path] = None) -> pd.DataFrame:
    """
    Execute a data processing pipeline from configuration file.
    
    Parameters:
        config_path (Union[str, Path]): Path to configuration file (JSON or YAML)
        output_path (Union[str, Path], optional): Path to save output DataFrame
        
    Returns:
        pd.DataFrame: Final processed DataFrame
        
    Example:
        >>> df = run_from_config("config.json")
        >>> df = run_from_config("config.yaml", output_path="output.csv")
    """
    # Load and validate configuration
    config = load_config(config_path)
    validate_config(config)
    
    logger.info(f"Starting pipeline execution from {config_path}")
    logger.info(f"Input file: {config['input_path']}")
    logger.info(f"Number of steps: {len(config['steps'])}")
    
    # Load input data
    input_path = Path(config['input_path'])
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")
    
    if input_path.suffix.lower() == '.csv':
        df = pd.read_csv(input_path)
    elif input_path.suffix.lower() in ['.xlsx', '.xls']:
        df = pd.read_excel(input_path)
    elif input_path.suffix.lower() == '.json':
        df = pd.read_json(input_path)
    else:
        raise ValueError(f"Unsupported input file format: {input_path.suffix}")
    
    logger.info(f"Loaded DataFrame with shape: {df.shape}")
    
    # Execute pipeline steps
    for i, step in enumerate(config['steps']):
        df = execute_step(df, step, i)
    
    # Save output if specified
    if output_path:
        output_path = Path(output_path)
        logger.info(f"Saving output to: {output_path}")
        
        if output_path.suffix.lower() == '.csv':
            df.to_csv(output_path, index=False)
        elif output_path.suffix.lower() in ['.xlsx', '.xls']:
            df.to_excel(output_path, index=False)
        elif output_path.suffix.lower() == '.json':
            df.to_json(output_path, orient='records', indent=2)
        else:
            raise ValueError(f"Unsupported output file format: {output_path.suffix}")
    
    logger.info("Pipeline execution completed successfully")
    return df


def create_example_config(output_path: Union[str, Path] = "example_config.json") -> None:
    """
    Create an example configuration file with common operations.
    
    Parameters:
        output_path (Union[str, Path]): Path to save example configuration
    """
    example_config = {
        "input_path": "data/input.csv",
        "output_path": "data/output.csv",
        "steps": [
            {
                "operation": "drop_duplicates",
                "params": {
                    "subset": ["sequence_id"],
                    "keep": "first"
                }
            },
            {
                "operation": "filter_rows",
                "params": {
                    "column": "activity",
                    "operator": ">",
                    "value": 0.5
                }
            },
            {
                "operation": "concat_and_pad_aas",
                "params": {
                    "cols_to_concat": ["Ncap", "AA1", "AA2", "AA3", "AA4", "AA5", "Ccap"],
                    "output_col": "sequence"
                }
            },
            {
                "operation": "add_punctuation_staples_and_stitches",
                "params": {
                    "col_name": "sequence",
                    "output_col": "sequence_with_punctuation"
                }
            },
            {
                "operation": "assign_class_labels",
                "params": {
                    "input_col": "activity",
                    "threshold": 0.7,
                    "output_col": "activity_class"
                }
            },
            {
                "operation": "sort_rows",
                "params": {
                    "by": "activity",
                    "ascending": False
                }
            },
            {
                "operation": "sample_rows",
                "params": {
                    "n": 1000,
                    "random_state": 42
                }
            }
        ]
    }
    
    with open(output_path, 'w') as f:
        json.dump(example_config, f, indent=2)
    
    logger.info(f"Example configuration saved to: {output_path}")


if __name__ == "__main__":
    # Create example config if run directly
    create_example_config()
