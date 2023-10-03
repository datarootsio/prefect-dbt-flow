from typing import List, Optional
import json

from prefect_dbt_flow.dbt import cli
from prefect_dbt_flow.dbt import DbtProject, DbtNode


def parse_dbt_project(
    project: DbtProject, graph_operator: Optional[str] = None
) -> List[DbtNode]:
    dbt_graph = _parse_dbt_graph(project)

    if graph_operator:
        return _filter_dbt_nodes_by_operator(dbt_graph, graph_operator)

    return dbt_graph


def _parse_dbt_graph(project: DbtProject) -> List[DbtNode]:
    dbt_graph: List[DbtNode] = []
    models_with_tests: List[str] = []

    dbt_ls_output = cli.dbt_ls(project)

    for line in dbt_ls_output.split("\n"):
        try:
            node_dict = json.loads(line.strip())

            if node_dict["resource_type"] == "model":
                dbt_graph.append(
                    DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"],
                        resource_type=node_dict["resource_type"],
                        depends_on=node_dict["depends_on"].get("nodes", []),
                    )
                )
            if node_dict["resource_type"] == "test":
                models_with_tests.extend(node_dict["depends_on"]["nodes"])

        except json.decoder.JSONDecodeError:
            pass

    for dbt_node in dbt_graph:
        if dbt_node.unique_id in models_with_tests:
            dbt_node.has_tests = True

    print(dbt_graph)

    return dbt_graph


def _filter_dbt_nodes_by_operator(
    dbt_nodes: List[DbtNode], graph_operator: str
) -> List[DbtNode]:
    # TODO: implement this
    return dbt_nodes
