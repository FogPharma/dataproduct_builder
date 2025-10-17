# Configuration-Based Data Processing

The `dataproduct_builder` package now supports JSON and YAML configuration files for defining data processing pipelines. This allows you to create reusable, version-controlled data processing workflows.

## Quick Start

### 1. Create a Configuration File

```bash
# Generate an example configuration
dataproduct-builder create-config --output my_config.json
```

### 2. Edit the Configuration

Modify the generated configuration file to match your data and requirements:

```json
{
  "input_path": "data/my_data.csv",
  "output_path": "data/processed_data.csv",
  "steps": [
    {
      "operation": "drop_duplicates",
      "params": {
        "subset": ["id"],
        "keep": "first"
      }
    },
    {
      "operation": "filter_rows",
      "params": {
        "column": "score",
        "operator": ">",
        "value": 0.5
      }
    }
  ]
}
```

### 3. Run the Pipeline

```bash
# Process data using configuration
dataproduct-builder process my_config.json

# Or specify output file
dataproduct-builder process my_config.json --output results.csv
```

## Configuration Format

### Basic Structure

```json
{
  "input_path": "path/to/input.csv",
  "output_path": "path/to/output.csv",  // Optional
  "steps": [
    {
      "operation": "operation_name",
      "params": {
        "param1": "value1",
        "param2": "value2"
      }
    }
  ]
}
```

### Supported File Formats

- **Input**: CSV, Excel (.xlsx, .xls), JSON
- **Output**: CSV, Excel (.xlsx, .xls), JSON
- **Configuration**: JSON, YAML (.yaml, .yml)

## Available Operations

### Column Operations
- `rename_columns` - Rename DataFrame columns
- `drop_columns` - Remove specified columns
- `concat_and_pad_aas` - Concatenate amino acid columns
- `add_punctuation_staples_and_stitches` - Add punctuation to peptide sequences
- `assign_class_labels` - Create classification labels
- `concatenate_stitches_and_staples` - Process peptide staples and stitches

### Row Operations
- `drop_duplicates` - Remove duplicate rows
- `filter_rows` - Filter rows based on conditions
- `sort_rows` - Sort DataFrame by columns
- `sample_rows` - Randomly sample rows
- `shuffle_rows` - Shuffle row order
- `validate_rows` - Apply multiple validation conditions
- `remove_empty_rows` - Remove rows with missing values

### Frame Operations
- `aggregate_dataframe` - Group and aggregate data
- `apply_pandas_function` - Apply any pandas method
- `apply_numpy_function` - Apply any numpy function

### Quality Checks
- `check_row_count` - Validate row count

## CLI Commands

### List Available Operations
```bash
dataproduct-builder list-operations
```

### Create Example Configuration
```bash
dataproduct-builder create-config
dataproduct-builder create-config --output custom_config.json
```

### Process Data
```bash
dataproduct-builder process config.json
dataproduct-builder process config.yaml --output results.csv --verbose
```

## Example Configurations

### Peptide Sequence Processing
See `example_peptide_config.json` for a complete peptide data processing pipeline including:
- Duplicate removal
- Activity filtering
- Amino acid concatenation
- Sequence punctuation
- Classification labeling
- Sampling and sorting

### Simple Data Processing
See `example_simple_config.json` for basic data operations:
- Duplicate removal
- Score filtering
- Sorting
- Random sampling

## Error Handling

The system includes comprehensive error handling:
- Configuration validation
- File format checking
- Operation parameter validation
- Step-by-step error reporting
- Detailed logging

## Logging

Enable verbose logging for debugging:
```bash
dataproduct-builder process config.json --verbose
```

## Python API

You can also use the configuration system programmatically:

```python
from dataproduct_builder.config_executor import run_from_config

# Process data from configuration
df = run_from_config("config.json")

# Save to specific output
df = run_from_config("config.json", output_path="results.csv")
```

## Tips

1. **Start Simple**: Begin with basic operations and gradually add complexity
2. **Test Incrementally**: Test each step individually before combining
3. **Use Examples**: Copy and modify the provided example configurations
4. **Validate Early**: The system validates configurations before execution
5. **Log Everything**: Use `--verbose` flag for detailed execution logs
