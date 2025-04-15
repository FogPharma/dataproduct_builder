"""Write dataframe schemas here. Refere to pandera.readthedocs.io for more information."""

from pandera import Check, Column, DataFrameSchema, Index

# Sourced from the pandera documentation.
example_schema = DataFrameSchema(
    {
        "column1": Column(int),
        "column2": Column(float, Check(lambda s: s < -1.2)),
        # you can provide a list of validators
        "column3": Column(
            str,
            [
                Check(lambda s: s.str.startswith("value")),
                Check(lambda s: s.str.split("_", expand=True).shape[1] == 2),
            ],
        ),
    },
    index=Index(int),
    strict=True,
    coerce=True,
)

# example_schema.validate(df)
