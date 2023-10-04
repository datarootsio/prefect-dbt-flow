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
    all_flow_kwargs = {
        "name": project.name,
        **(flow_kwargs or {}),
    }

    dbt_graph = graph.parse_dbt_project(project, dag_options)

    @flow(**all_flow_kwargs)
    def dbt_flow():
        tasks.generate_tasks_dag(
            project,
            profile,
            dbt_graph,
            dag_options.run_test_after_model if dag_options else False,
        )

    return dbt_flow
