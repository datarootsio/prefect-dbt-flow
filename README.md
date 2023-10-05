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
from pathlib import Path

from prefect.task_runners import SequentialTaskRunner

from prefect_dbt_flow.dbt import DbtProject, DbtProfile
from prefect_dbt_flow import dbt_flow

my_dbt_flow = dbt_flow(
    project=DbtProject(
        name="sample_project",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="prod",
    ),
    flow_kwargs={
        # Ensure only one process has access to the duckdb database file at the same time
        "task_runner": SequentialTaskRunner(),
    },
)

if __name__ == "__main__":
    my_dbt_flow()
```

## License
This project is licensed under the MIT License.