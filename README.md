<p align="center">
  <a href="https://datarootsio.github.io/prefect-dbt-flow"><img alt="logo" src="https://dataroots.io/assets/logo/logo-rainbow.png"></a>
</p>
<p align="center">
  <a href="https://dataroots.io"><img alt="Maintained by dataroots" src="https://dataroots.io/maintained-rnd.svg" /></a>
  <a href="https://pypi.org/project/prefect-dbt-flow/"><img alt="Python versions" src="https://img.shields.io/pypi/pyversions/prefect-dbt-flow" /></a>
  <a href="https://pypi.org/project/prefect-dbt-flow/"><img alt="PiPy" src="https://img.shields.io/pypi/v/prefect-dbt-flow" /></a>
  <a href="https://pepy.tech/project/prefect-dbt-flow"><img alt="Downloads" src="https://pepy.tech/badge/prefect-dbt-flow" /></a>
  <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg" /></a>
  <a href="http://mypy-lang.org/"><img alt="Mypy checked" src="https://img.shields.io/badge/mypy-checked-1f5082.svg" /></a>
</p>

# prefect-dbt-flow
Prefect-dbt-flow is a Python library that enables Prefect to convert dbt workflows into independent tasks within a Prefect flow. This integration simplifies the orchestration and execution of dbt models and tests using Prefect, allowing you to build robust data pipelines and monitor your dbt projects efficiently.

**Active Development Notice:** Prefect-dbt-flow is actively under development and may not be ready for production use. We advise users to be aware of potential breaking changes as the library evolves. Please check the changelog for updates.

## Table of Contents
- [Introduction](#introduction)
- [Why Use Prefect-dbt-flow?](#why-use-prefect-dbt-flow)
- [How to Install](#how-to-install)
- [Basic Usage](#basic-usage)
- [Inspiration](#inspiration)
- [License](#license)

## Introduction
Prefect-dbt-flow is a tool designed to streamline the integration of dbt workflows into Prefect. dbt is an immensely popular tool for building and testing data transformation models, and Prefect is a versatile workflow management system. This integration brings together the best of both worlds, empowering data engineers and analysts to create robust data pipelines.

## Why Use Prefect-dbt-flow?
### Simplified Orchestration
With Prefect-dbt-flow, you can orchestrate your dbt workflows with ease. Define and manage your dbt projects and models as Prefect tasks, creating a seamless pipeline for data transformation.

[Simplified Orchestration]()

### Monitoring and Error Handling
Prefect provides extensive monitoring capabilities and error handling. Now, you can gain deep insights into the execution of your dbt workflows and take immediate action in case of issues.

[Monitoring and Error Handling]()

### Workflow Consistency
Ensure your dbt workflows run consistently by managing them through Prefect. This consistency is crucial for maintaining data quality and reliability.

[Workflow Consistency]()

## How to Install
You can install Prefect-dbt-flow via pip:
```shell
pip install prefect-dbt-flow
```
## Basic Usage
Here's an example of how to use Prefect-dbt-flow to create a Prefect flow for your dbt project:
```python
from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtProfile, DbtProject, DbtDagOptions

my_flow = dbt_flow(
        project=DbtProject(
            name="my_flow",
            project_dir="path_to/dbt_project",
            profiles_dir="path_to/dbt_profiles",
        ),
        profile=DbtProfile(
            target="dev",
        ),
        dag_options=DbtDagOptions(
            run_test_after_model=True,
        ),
    )

if __name__ == "__main__":
    my_flow()
```
For more information consult the [Getting started guide](GETTING_STARTED.md)

## Inspiration
Prefect-dbt-flow draws inspiration from various projects in the data engineering and workflow orchestration space, including:
- [cosmos by astronomer](https://github.com/astronomer/astronomer-cosmos)
- [anna-geller => prefect-dataplatform](https://github.com/anna-geller/prefect-dataplatform)
- [dbt + Dagster](https://docs.dagster.io/integrations/dbt)

# License
This project is licensed under the MIT License. You are free to use, modify, and distribute this software as per the terms of the license. If you find this project helpful, please consider giving it a star on GitHub.