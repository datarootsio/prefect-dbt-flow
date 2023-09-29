from typing import Optional, Any

from prefect import flow, Flow

from prefect_dbt_flow.dbt import DbtProject, DbtProfile
from prefect_dbt_flow.dbt import graph, tasks


def dbt_flow(
    project: DbtProject,
    profile: Optional[DbtProfile] = None,
    graph_operator: Optional[str] = None,
    run_test_after_model: bool = False,
    flow_kwargs: Optional[dict] = None,
) -> Flow[[], Any]:
    all_flow_kwargs = {
        "name": project.name,
        **(flow_kwargs or {}),
    }

    dbt_graph = graph.parse_dbt_project(project, graph_operator)

    @flow(**all_flow_kwargs)
    def dbt_flow():
        tasks.generate_tasks_dag(dbt_graph, run_test_after_model)

    return dbt_flow
