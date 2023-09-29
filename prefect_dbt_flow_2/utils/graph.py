import json
from prefect import get_run_logger
from typing import Dict

from prefect_dbt_flow_2.utils.cmd import _run_cmd
from prefect_dbt_flow_2.utils import DbtNode

def parse_dbt_nodes_info() -> Dict[str, DbtNode]:
    """
    Function to parse dbt nodes from the output of the `dbt ls` command.
    Returns a dictionary mapping unique IDs to DbtNode instances.
    """
    dbt_ls_command = [
        DBT_EXE,
        "ls",
        "--project-dir",
        str(DBT_PROJECT_DIR.absolute()),
        "--output",
        "json",
        "--profiles-dir",
        str(DBT_PROJECT_DIR.absolute()),
    ]
    # print(f"\n---debug_parse_dbt_nodes_info__dbt_ls_command:\n{dbt_ls_command}")
    cmd_out = _run_cmd(dbt_ls_command)
    # print(f"\n---debug_parse_dbt_nodes_info:\n{cmd_out}")
    dbt_nodes_info = {}
    for raw_dbt_node_data in cmd_out.split("\n"):
        if "{" in raw_dbt_node_data:
            try:
                node_dict = json.loads(raw_dbt_node_data.strip())
                if node_dict["resource_type"] == "model" or node_dict["resource_type"] == "test":
                    dbt_node = DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"],
                        resource_type=node_dict["resource_type"],
                        depends_on=node_dict["depends_on"].get("nodes", []),
                        file_path=DBT_PROJECT_DIR / node_dict["original_file_path"],
                        tags=node_dict["tags"],
                        config=node_dict["config"],
                    )
                    dbt_nodes_info[dbt_node.unique_id] = dbt_node
            except json.decoder.JSONDecodeError:
                get_run_logger().debug(f"Skipping line: {raw_dbt_node_data}")
                print("error")

    return dbt_nodes_info