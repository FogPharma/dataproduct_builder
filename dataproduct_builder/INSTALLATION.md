# Installation Guide

This guide will help you install the `dataproduct-builder` package locally for development and testing.

## Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git (optional, for development)

## Installation Methods

### Method 1: Development Installation (Recommended)

This method installs the package in "editable" mode, so changes to the source code are immediately available.

```bash
# 1. Navigate to the package directory
cd /path/to/dataproduct_builder/dataproduct_builder

# 2. Install in development mode
pip install -e .

# 3. Verify installation
dataproduct-builder --help
```

### Method 2: Build and Install

This method builds the package and installs it normally.

```bash
# 1. Navigate to the package directory
cd /path/to/dataproduct_builder/dataproduct_builder

# 2. Build the package
python -m build

# 3. Install the built package
pip install dist/dataproduct_builder-0.1.0-py3-none-any.whl

# 4. Verify installation
dataproduct-builder --help
```

### Method 3: Install with Development Dependencies

For development work, install with additional tools:

```bash
# 1. Navigate to the package directory
cd /path/to/dataproduct_builder/dataproduct_builder

# 2. Install with development dependencies
pip install -e ".[dev]"

# 3. Verify installation
dataproduct-builder --help
```

## Verification

After installation, verify everything works:

```bash
# Test CLI
dataproduct-builder --help

# Test individual commands
dataproduct-builder list-operations
dataproduct-builder create-config

# Test Python import
python -c "import dataproduct_builder; print(dataproduct_builder.__version__)"
```

## Testing the Package

### 1. Create a Test Configuration

```bash
# Create example config
dataproduct-builder create-config --output test_config.json

# List available operations
dataproduct-builder list-operations
```

### 2. Test with Sample Data

Create a simple test CSV file:

```bash
# Create test data
cat > test_data.csv << EOF
id,sequence,activity
1,ACDEFGH,0.8
2,BCDEFGH,0.3
3,CDEFGHI,0.9
4,DEFGHIJ,0.2
EOF
```

Create a test configuration:

```json
{
  "input_path": "test_data.csv",
  "output_path": "test_output.csv",
  "steps": [
    {
      "operation": "filter_rows",
      "params": {
        "column": "activity",
        "operator": ">",
        "value": 0.5
      }
    },
    {
      "operation": "sort_rows",
      "params": {
        "by": "activity",
        "ascending": false
      }
    }
  ]
}
```

Run the test:

```bash
dataproduct-builder process test_config.json --verbose
```

### 3. Test Python API

```python
import pandas as pd
import dataproduct_builder as dpb

# Create test data
df = pd.DataFrame({
    'id': [1, 2, 3, 4],
    'sequence': ['ACDEFGH', 'BCDEFGH', 'CDEFGHI', 'DEFGHIJ'],
    'activity': [0.8, 0.3, 0.9, 0.2]
})

# Test individual functions
filtered_df = dpb.filter_rows(df, 'activity', '>', 0.5)
sorted_df = dpb.sort_rows(filtered_df, 'activity', ascending=False)

print("Filtered and sorted data:")
print(sorted_df)
```

## Troubleshooting

### Common Issues

1. **Command not found**: Make sure you're in the correct directory and have activated your Python environment.

2. **Import errors**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt  # if you have one
   # or
   pip install pandas numpy typer pyyaml openpyxl
   ```

3. **Permission errors**: Use `--user` flag for user installation:
   ```bash
   pip install -e . --user
   ```

4. **Version conflicts**: Use a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e .
   ```

### Uninstalling

To uninstall the package:

```bash
pip uninstall dataproduct-builder
```

## Development Setup

For active development:

```bash
# 1. Clone or navigate to the repository
cd /path/to/dataproduct_builder

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode with all dependencies
pip install -e ".[dev]"

# 4. Install pre-commit hooks (optional)
pre-commit install

# 5. Run tests
pytest

# 6. Format code
black src/
ruff check src/
```

## Package Structure

After installation, the package will be available as:

- **CLI**: `dataproduct-builder` command
- **Python**: `import dataproduct_builder`
- **Functions**: `dataproduct_builder.filter_rows()`, etc.

## Next Steps

1. **Read the documentation**: Check `CONFIG_USAGE.md` for detailed usage
2. **Try examples**: Use the provided example configurations
3. **Create your own**: Build custom processing pipelines
4. **Contribute**: Report issues or suggest improvements

## Support

If you encounter issues:

1. Check this installation guide
2. Verify your Python version (3.10+)
3. Ensure all dependencies are installed
4. Check the package documentation
5. Report issues on the project repository
