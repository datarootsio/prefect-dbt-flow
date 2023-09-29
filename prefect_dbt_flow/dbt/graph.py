from typing import List, Optional

from prefect_dbt_flow.dbt import DbtProject, DbtNode


def parse_dbt_project(
    project: DbtProject, graph_operator: Optional[str] = None
) -> List[DbtNode]:
    dbt_graph = _parse_dbt_graph(project)

    if graph_operator:
        return _filter_dbt_nodes_by_operator(dbt_graph, graph_operator)

    return dbt_graph


def _parse_dbt_graph(project: DbtProject) -> List[DbtNode]:
    ...


def _filter_dbt_nodes_by_operator(
    dbt_nodes: List[DbtNode], graph_operator: str
) -> List[DbtNode]:
    ...
