import yaml
import pandas as pd
from dataproduct_builder import column_ops, quality_checks

OPERATION_MAP = {
    'rename_columns': column_ops.rename_columns,
    'check_row_count': quality_checks.check_row_count,
}

def run_from_config():
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    df = pd.read_csv(config["input_path"])
    for step in config["steps"]:
        func = OPERATION_MAP[step["operation"]]
        params = step.get("params", {})
        result = func(df, **params)
        if isinstance(result, str):  # result is a validation message
            print(result)
        else:
            df = result
