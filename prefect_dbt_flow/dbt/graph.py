"""Code for parsing dbt project and generate a list of dbt nodes"""
import json
from typing import List, Optional

from prefect_dbt_flow.dbt import (
    DbtDagOptions,
    DbtNode,
    DbtProject,
    DbtResourceType,
    cli,
)


def parse_dbt_project(
    project: DbtProject, dag_options: Optional[DbtDagOptions] = None
) -> List[DbtNode]:
    """
    Parses a list of dbt nodes class objects from dbt ls cli command.

    Args:
        project: A class that represents a dbt project configuration.
        dag_options: A class to add dbt DAG configurations.

    Returns:
        dbt_graph: A list of dbt nodes, each node as a dataclass.
    """
    dbt_graph: List[DbtNode] = []
    models_with_tests: List[str] = []

    dbt_ls_output = cli.dbt_ls(project, dag_options)

    for line in dbt_ls_output.split("\n"):
        try:
            node_dict = json.loads(line.strip())

            if node_dict["resource_type"] == "model":
                dbt_graph.append(
                    DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"],
                        resource_type=DbtResourceType.MODEL,
                        depends_on=node_dict["depends_on"].get("nodes", []),
                    )
                )

            if node_dict["resource_type"] == "test":
                models_with_tests.extend(node_dict["depends_on"]["nodes"])

            if node_dict["resource_type"] == "seed":
                dbt_graph.append(
                    DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"],
                        resource_type=DbtResourceType.SEED,
                        depends_on=node_dict["depends_on"].get("nodes", []),
                    )
                )

            if node_dict["resource_type"] == "snapshot":
                dbt_graph.append(
                    DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"],
                        resource_type=DbtResourceType.SNAPSHOT,
                        depends_on=node_dict["depends_on"].get("nodes", []),
                    )
                )

        except json.decoder.JSONDecodeError:
            pass

    # Check if a node has tests
    for dbt_node in dbt_graph:
        if dbt_node.unique_id in models_with_tests:
            dbt_node.has_tests = True

    # Remove dependencies if not in Graph (needed in case of select/exclude)
    all_model_ids = [dbt_node.unique_id for dbt_node in dbt_graph]
    for dbt_node in dbt_graph:
        dbt_node.depends_on = [
            node_id for node_id in dbt_node.depends_on if node_id in all_model_ids
        ]

    return dbt_graph
