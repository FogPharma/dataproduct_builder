import typer
from pathlib import Path
from typing import Optional
from dataproduct_builder.config_executor import run_from_config, create_example_config

app = typer.Typer(help="DataProduct Builder - Peptide sequence data processing pipeline")


@app.command()
def process(
    config: str = typer.Argument(..., help="Path to configuration file (JSON or YAML)"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Output file path"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """
    Process data using a configuration file.
    
    This command executes a data processing pipeline defined in a JSON or YAML configuration file.
    The configuration specifies input data, processing steps, and parameters.
    
    Example:
        dataproduct-builder process config.json
        dataproduct-builder process config.yaml --output results.csv
    """
    try:
        if verbose:
            import logging
            logging.getLogger().setLevel(logging.DEBUG)
        
        typer.echo(f"Processing data with configuration: {config}")
        result_df = run_from_config(config, output_path=output)
        
        typer.echo(f"✅ Processing completed successfully!")
        typer.echo(f"📊 Final DataFrame shape: {result_df.shape}")
        
        if output:
            typer.echo(f"💾 Results saved to: {output}")
        else:
            typer.echo("💡 Use --output to save results to a file")
            
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def create_config(
    output: str = typer.Option("example_config.json", "--output", "-o", help="Output configuration file path")
):
    """
    Create an example configuration file.
    
    This command generates a sample JSON configuration file that demonstrates
    how to use various data processing operations.
    
    Example:
        dataproduct-builder create-config
        dataproduct-builder create-config --output my_config.json
    """
    try:
        create_example_config(output)
        typer.echo(f"✅ Example configuration created: {output}")
        typer.echo("📝 Edit the configuration file to match your data and requirements")
        typer.echo("🚀 Then run: dataproduct-builder process <config_file>")
        
    except Exception as e:
        typer.echo(f"❌ Error: {str(e)}", err=True)
        raise typer.Exit(1)


@app.command()
def list_operations():
    """
    List all available data processing operations.
    
    This command shows all the operations that can be used in configuration files.
    """
    from dataproduct_builder.config_executor import OPERATION_MAP
    
    typer.echo("📋 Available Operations:")
    typer.echo("=" * 50)
    
    # Group operations by module
    column_ops = [op for op in OPERATION_MAP.keys() if op in [
        'rename_columns', 'drop_columns', 'concat_and_pad_aas', 
        'add_punctuation_staples_and_stitches', 'assign_class_labels', 
        'concatenate_stitches_and_staples'
    ]]
    
    row_ops = [op for op in OPERATION_MAP.keys() if op in [
        'drop_duplicates', 'filter_rows', 'sort_rows', 'sample_rows',
        'shuffle_rows', 'validate_rows', 'remove_empty_rows'
    ]]
    
    frame_ops = [op for op in OPERATION_MAP.keys() if op in [
        'aggregate_dataframe', 'aggregate_with_custom_functions', 'aggregate_with_column_functions', 
        'aggregate_peptide_data', 'apply_pandas_function', 'apply_numpy_function'
    ]]
    
    quality_ops = [op for op in OPERATION_MAP.keys() if op in [
        'check_row_count', 'check_column_count', 'check_missing_values', 'check_data_types'
    ]]
    
    typer.echo("🔧 Column Operations:")
    for op in column_ops:
        typer.echo(f"  • {op}")
    
    typer.echo("\n📊 Row Operations:")
    for op in row_ops:
        typer.echo(f"  • {op}")
    
    typer.echo("\n🔄 Frame Operations:")
    for op in frame_ops:
        typer.echo(f"  • {op}")
    
    typer.echo("\n✅ Quality Checks:")
    for op in quality_ops:
        typer.echo(f"  • {op}")
    
    typer.echo(f"\n📖 Total operations: {len(OPERATION_MAP)}")
    typer.echo("💡 Use 'create-config' to see example usage")


if __name__ == "__main__":
    app()
