![dataroots.png](https://dataroots.io/assets/logo/logo-rainbow.png)
[![maintained by dataroots](https://img.shields.io/badge/maintained%20by-dataroots-%2300b189)](https://dataroots.io)

# prefect-dbt-flow
Welcome to the prefect-dbt-flow integration repository! This project aims to provide a seamless integration for simplifying the execution of dbt workflows using Prefect.

## Requirements
Before you get started, make sure you have the following prerequisites installed on your system:

- python
- prefect
- dbt

## Installation
``` bash
pip install prefect-dbt-flow
```

## Usage

### Create a flow

``` python
import prefect_dbt_flow as dbtFlow

my_flow = dbtFlow.dbt_flow(
    project=dbtFlow.DbtProject(
        name="my_flow",
        project_dir="path_to/dbt_project",
        profiles_dir="path_to/dbt_profiles",
    ),
    profile=dbtFlow.DbtProfile(
        target="dev",
    ),
    dag_options=dbtFlow.DbtDagOptions(
        run_test_after_model=True,
    ),
)

if __name__ == "__main__":
    my_flow()
```

## License
This project is licensed under the MIT License.