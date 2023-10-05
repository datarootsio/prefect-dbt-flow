"""Functions to create a prefect flow for a dbt project."""
from typing import Optional, Any

from prefect import flow

from prefect_dbt_flow.dbt import (
    DbtProject,
    DbtProfile,
    DbtDagOptions,
    graph,
    tasks,
)


def dbt_flow(
    project: DbtProject,
    profile: Optional[DbtProfile] = None,
    dag_options: Optional[DbtDagOptions] = None,
    flow_kwargs: Optional[dict] = None,
) -> Any:
    """
    Create a PrefectFlow for executing a dbt project.

    Examples:
        ```
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
        ```

    Args:
        project (dataclass): A Class that represents a dbt project configuration.
        profile (dataclass): A Class that represents a dbt profile configuration.
        dag_options (dataclass): A Class to add dbt DAG configurations.
        flow_kwargs (dict): A dict of prefect @flow arguments

    Returns:
        dbt_flow: A Prefec Flow.
    """
    all_flow_kwargs = {
        "name": project.name,
        **(flow_kwargs or {}),
    }

    dbt_graph = graph.parse_dbt_project(project, dag_options)

    @flow(**all_flow_kwargs)
    def dbt_flow():
        """
        Function that configurates and runs a Prefect flow using the parameters from dbt_flow.

        Returns:
            A prefect flow
        """
        tasks.generate_tasks_dag(
            project,
            profile,
            dbt_graph,
            dag_options.run_test_after_model if dag_options else False,
        )

    return dbt_flow
