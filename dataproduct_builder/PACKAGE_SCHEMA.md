# DataProduct Builder Package Schema

## Package Architecture Overview

```
dataproduct_builder/
├── 📦 Package Structure
│   ├── src/dataproduct_builder/
│   │   ├── __init__.py (Package Interface)
│   │   ├── cli.py (Command Line Interface)
│   │   ├── config_executor.py (Pipeline Orchestrator)
│   │   ├── column_ops.py (Column Operations)
│   │   ├── row_ops.py (Row Operations)
│   │   ├── frame_ops.py (DataFrame Operations)
│   │   └── quality_checks.py (Data Validation)
│   ├── pyproject.toml (Package Configuration)
│   ├── requirements.txt (Dependencies)
│   └── example_*.json (Configuration Examples)
```

## Module Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                    dataproduct_builder                          │
│                         Package                                 │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    __init__.py                                  │
│              (Package Interface & Exports)                      │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│     cli.py          │ │ config_executor │ │   Core Modules      │
│ (Command Line)      │ │   (Orchestrator)│ │                     │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
                                │                       │
                                ▼                       ▼
                    ┌─────────────────────┐   ┌─────────────────────┐
                    │   OPERATION_MAP     │   │  Function Modules   │
                    │  (47 Operations)    │   │                     │
                    └─────────────────────┘   └─────────────────────┘
                                │                       │
                                ▼                       ▼
                ┌─────────────────────────────────────────────────┐
                │              Core Modules                       │
                └─────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   column_ops.py     │ │   row_ops.py    │ │   frame_ops.py      │
│  (7 Functions)      │ │  (7 Functions)  │ │  (5 Functions)      │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ quality_checks.py   │
                    │  (4 Functions)      │
                    └─────────────────────┘
```

## Function Categories & Operations

### Column Operations (column_ops.py)
```
┌─────────────────────────────────────────────────────────────────┐
│                    Column Operations                            │
├─────────────────────────────────────────────────────────────────┤
│ • rename_columns()           - Rename DataFrame columns         │
│ • drop_columns()             - Remove specified columns         │
│ • concat_and_pad_aas()       - Concatenate amino acid columns   │
│ • add_punctuation_staples_   - Add punctuation to sequences     │
│   and_stitches()                                                │
│ • assign_class_labels()      - Create classification labels     │
│ • concatenate_stitches_      - Process peptide staples/stitches │
│   and_staples()                                                 │
│ • concatenate_stitches_      - Alternative peptide processing   │
│   and_staples2()                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Row Operations (row_ops.py)
```
┌─────────────────────────────────────────────────────────────────┐
│                      Row Operations                             │
├─────────────────────────────────────────────────────────────────┤
│ • drop_duplicates()          - Remove duplicate rows            │
│ • filter_rows()              - Filter rows by conditions        │
│ • sort_rows()                - Sort DataFrame rows              │
│ • sample_rows()              - Random sample of rows            │
│ • shuffle_rows()             - Randomly shuffle rows            │
│ • validate_rows()            - Validate row data                │
│ • remove_empty_rows()        - Remove rows with missing data    │
└─────────────────────────────────────────────────────────────────┘
```

### Frame Operations (frame_ops.py)
```
┌─────────────────────────────────────────────────────────────────┐
│                    DataFrame Operations                         │
├─────────────────────────────────────────────────────────────────┤
│ • aggregate_dataframe()      - Basic DataFrame aggregation      │
│ • aggregate_with_custom_     - Aggregation with custom functions│
│   functions()                                                   │
│ • aggregate_with_column_     - Column-specific aggregation      │
│   functions()                                                   │
│ • aggregate_peptide_data()   - Specialized peptide aggregation  │
│ • apply_pandas_function()    - Apply pandas methods             │
│ • apply_numpy_function()     - Apply numpy functions            │
└─────────────────────────────────────────────────────────────────┘
```

### Quality Checks (quality_checks.py)
```
┌─────────────────────────────────────────────────────────────────┐
│                    Data Quality Checks                          │
├─────────────────────────────────────────────────────────────────┤
│ • check_row_count()          - Validate row count               │
│ • check_column_count()       - Validate column count            │
│ • check_missing_values()     - Check for missing data           │
│ • check_data_types()         - Validate data types              │
└─────────────────────────────────────────────────────────────────┘
```

## Configuration System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                Configuration-Driven Pipeline                    │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    JSON/YAML Config                             │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ {                                                       │   │
│  │   "input_path": "data.csv",                            │   │
│  │   "output_path": "output.csv",                         │   │
│  │   "steps": [                                           │   │
│  │     {                                                  │   │
│  │       "operation": "filter_rows",                      │   │
│  │       "params": { "column": "score", "operator": ">" } │   │
│  │     }                                                  │   │
│  │   ]                                                    │   │
│  │ }                                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                config_executor.py                               │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ • load_config()         - Load JSON/YAML configs        │   │
│  │ • validate_config()     - Validate configuration        │   │
│  │ • execute_step()        - Execute individual steps      │   │
│  │ • run_from_config()     - Run complete pipeline         │   │
│  │ • OPERATION_MAP         - Maps 47 operations            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Function Execution                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ 1. Load Data (CSV/Excel/JSON)                          │   │
│  │ 2. Execute Steps Sequentially                          │   │
│  │ 3. Apply Operations via OPERATION_MAP                  │   │
│  │ 4. Save Results (CSV/Excel/JSON)                       │   │
│  │ 5. Log Progress & Errors                               │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## CLI Interface

```
┌─────────────────────────────────────────────────────────────────┐
│                    Command Line Interface                       │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    dataproduct-builder                          │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │ Commands:                                              │   │
│  │ • process <config>     - Run pipeline from config      │   │
│  │ • create-config        - Generate example config       │   │
│  │ • list-operations      - Show available operations     │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        Data Flow                                │
└─────────────────────────────────────────────────────────────────┘
                                │
                ┌───────────────┼───────────────┐
                ▼               ▼               ▼
┌─────────────────────┐ ┌─────────────────┐ ┌─────────────────────┐
│   Input Data        │ │   Processing    │ │   Output Data       │
│ • CSV Files         │ │ • Column Ops    │ │ • Processed CSV     │
│ • Excel Files       │ │ • Row Ops       │ │ • Excel Files       │
│ • JSON Files        │ │ • Frame Ops     │ │ • JSON Files        │
│                     │ │ • Quality Checks│ │ • Logs & Reports    │
└─────────────────────┘ └─────────────────┘ └─────────────────────┘
```

## Key Features

### 🎯 **Core Capabilities**
- **47 Operations** across 4 modules
- **Configuration-driven** pipelines (JSON/YAML)
- **CLI Interface** with 3 main commands
- **Multiple file formats** (CSV, Excel, JSON)
- **Specialized peptide processing** (staples, stitches, sequences)

### 🔧 **Technical Features**
- **Modular architecture** with clear separation
- **Type hints** throughout codebase
- **Error handling** and logging
- **Editable installation** support
- **Professional packaging** with pyproject.toml

### 📊 **Domain Expertise**
- **Peptide sequence analysis** with specialized functions
- **Amino acid processing** (concatenation, padding)
- **Staple/stitch handling** for peptide chemistry
- **Aggregation functions** for biological data
- **Data quality validation** for research data

## Usage Patterns

### 1. **Direct Function Calls**
```python
import dataproduct_builder as dpb
result = dpb.rename_columns(df, {"old": "new"})
```

### 2. **Configuration Pipeline**
```python
result = dpb.run_from_config("my_pipeline.json")
```

### 3. **CLI Usage**
```bash
dataproduct-builder process my_config.json --output results.csv
```

This schema represents a well-architected, production-ready package for data processing with specialized capabilities for peptide analysis.
