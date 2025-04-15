## Why do we need this Github repo?
In general, every project has multiple codes, notebooks, scripts and plots, which are generated while working on the project's goals. Having a Git repo template to follow for a Python project helps i. standarize the file structure across the projects and users and ii. wrap all the relevant Python scripts into a Python package for easy distribution. Note that this distribution could be to different users or different compute environments for the same user.

The tutorial given here for building a Python Package is different than the typical tutorials seen on web, which uses an intermediate step of publishing it to public `pypi` server. We can't follow those tutorials for propreity code. The workflow given here avoids publishing to any public server.


## How to use this?

We use [cookiecutter](https://github.com/cookiecutter/cookiecutter) package to implement a customizable package. It has an automated pipeline to create package folder along with its corresponding metadata defined in `cookiecutter.json`

Please follow the instructions given below:

``` 
conda env create --file environment.yml
conda activate cookiecutter_env
git clone git@github.com:FogPharma/fog-cdd-pytemplate.git
pipx run cookiecutter fog-cdd-pytemplate
```

More specific details about the Python package are given in [{{ cookiecutter.repo_name }}/Readme.md](https://github.com/FogPharma/fog-cdd-pytemplate/tree/main/%7B%7B%20cookiecutter.repo_name%20%7D%7D#readme)

## Features

- Data Science friendly folder structure
- Github actions template : automated CI/CD
- `toml` file for tracking package dependencies
- pytest template for creating unit and integration test
- Ruff and Black linting
- pre-commit hook
