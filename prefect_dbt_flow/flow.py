"""Functions to create a prefect flow for a dbt project."""
from typing import Optional, Any

from prefect import flow, Flow

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
) -> Flow[[], Any]:
    """
    Create a PrefectFlow for executing a dbt project.

    :param project: Class that represents a dbt project configuration.
    :param profile: Class that represents a dbt profile configuration.
    :param dag_options: Class to add dbt DAG configurations.
    :param flow_kwargs:
    :return: Prefec Flow.
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

        :return: prefect flow
        """
        tasks.generate_tasks_dag(
            project,
            profile,
            dbt_graph,
            dag_options.run_test_after_model if dag_options else False,
        )

    return dbt_flow
