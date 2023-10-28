<p align="center">
  <a href="https://dataroots.io"><img alt="Maintained by dataroots" src="https://dataroots.io/maintained-rnd.svg" /></a>
  <a href="https://pypi.org/project/prefect-dbt-flow/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/prefect-dbt-flow" /></a>
  <a href="https://pypi.org/project/prefect-dbt-flow/"><img alt="PiPy" src="https://img.shields.io/pypi/v/prefect-dbt-flow" /></a>
  <a href="https://pepy.tech/project/prefect-dbt-flow"><img alt="Downloads" src="https://pepy.tech/badge/prefect-dbt-flow" /></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>
  <a href="https://codecov.io/gh/datarootsio/prefect-dbt-flow" >
    <img src="https://codecov.io/gh/datarootsio/prefect-dbt-flow/graph/badge.svg?token=NQ6RMX6670"/>
  </a>
</p>

# prefect-dbt-flow
prefect-dbt-flow is a Python library that enables Prefect to convert dbt workflows into independent tasks within a Prefect flow. This integration simplifies the orchestration and execution of dbt models and tests using Prefect, allowing you to build robust data pipelines and monitor your dbt projects efficiently.

dbt is an immensely popular tool for building and testing data transformation models, and Prefect is a versatile workflow management system. This integration brings together the best of both worlds, empowering data engineers and analysts to create robust data pipelines.

Key features:

 - *Simplified Orchestration*: Define and manage your dbt projects and models as Prefect tasks, creating a seamless pipeline for data transformation.
 - *Monitoring and Error Handling*: Gain deep insights into the execution of your dbt workflows and take immediate action in case of issues.
 - *Workflow Consistency*: Ensure your dbt workflows run consistently by managing them through Prefect. This consistency is crucial for maintaining data quality and reliability.
 - *Advanced Configuration*: Customize your dbt workflow by adjusting the dbt project, profile, and DAG options. You can also use Prefect features like scheduling, notifications, and task retries to monitor and manage your dbt flows effectively.

To get started, check out our [getting started guide](https://datarootsio.github.io/prefect-dbt-flow/latest/getting_started/).

**Active Development Notice:** *prefect-dbt-flow is actively under development and may not be ready for production use. We advise users to be aware of potential breaking changes as the library evolves. Please check the changelog for updates.*

## How to Install
You can install prefect-dbt-flow via pip:
```shell
pip install prefect-dbt-flow
```

*Note*: prefect-dbt-flow does not come with dbt as a dependency. You will need to install dbt or a dbt-adapter separately.

## Basic Usage
Here's an example of how to use prefect-dbt-flow to create a Prefect flow for your dbt project:

```python
from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtProfile, DbtProject

my_flow = dbt_flow(
    project=DbtProject(
        name="jaffle_shop",
        project_dir="path_to/jaffle_shop",
        profiles_dir="path_to/jaffle_shop",
    ),
    profile=DbtProfile(
        target="dev",
        overrides={
            "type": "duckdb",
            "path": "path_to/duckdb.db",
        },
    ),
)

if __name__ == "__main__":
    my_flow()
```

<img src="https://raw.githubusercontent.com/datarootsio/prefect-dbt-flow/main/docs/images/jaffle_shop_dag.png" alt="jaffle_shop_dag" width="100%">

For more information consult the [docs](https://datarootsio.github.io/prefect-dbt-flow/)

## Inspiration
prefect-dbt-flow draws inspiration from various projects in the data engineering and workflow orchestration space, including:
- [astronomer-cosmos](https://github.com/astronomer/astronomer-cosmos)
- [dbt + Dagster](https://docs.dagster.io/integrations/dbt)
- [prefect-dataplatform - Anna Geller](https://github.com/anna-geller/prefect-dataplatform)

# License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license. If you find this project helpful, please consider giving it a star on GitHub.
