"""Functions to create a prefect flow for a dbt project."""
from typing import Optional

from prefect import Flow, flow

from prefect_dbt_flow.dbt import DbtDagOptions, DbtProfile, DbtProject, graph, tasks


def dbt_flow(
    project: DbtProject,
    profile: Optional[DbtProfile] = None,
    dag_options: Optional[DbtDagOptions] = None,
    flow_kwargs: Optional[dict] = None,
) -> Flow:
    """
    Create a PrefectFlow for executing a dbt project.

    Args:
        project: A Class that represents a dbt project configuration.
        profile: A Class that represents a dbt profile configuration.
        dag_options: A Class to add dbt DAG configurations.
        flow_kwargs: A dict of prefect @flow arguments

    Returns:
        dbt_flow: A Prefec Flow.
    """
    all_flow_kwargs = {
        "name": project.name,
        **(flow_kwargs or {}),
    }

    dbt_graph = graph.parse_dbt_project(project, profile, dag_options)

    @flow(**all_flow_kwargs)
    def dbt_flow():
        """
        Function that configurates and runs a Prefect flow.

        Returns:
            A prefect flow
        """
        tasks.generate_tasks_dag(
            project,
            profile,
            dag_options,
            dbt_graph,
            dag_options.run_test_after_model if dag_options else False,
        )

    return dbt_flow
