import json
from prefect import get_run_logger
from typing import Dict

from utils import DbtNode, DbtConfig, cmd, logging_config

logger = logging_config.logger


def parse_dbt_nodes_info(dbt_config: DbtConfig) -> Dict[str, DbtNode]:
    """
    Function to parse dbt nodes from the output of the `dbt ls` command.
    Returns a dictionary mapping unique IDs to DbtNode instances.
    """
    dbt_ls_command = [
        dbt_config.dbt_exe,
        "ls",
        "--project-dir",
        dbt_config.dbt_project_dir,
        "--output",
        "json",
        "--profiles-dir",
        dbt_config.dbt_profiles_dir,
    ]
    
    cmd_out = cmd._run_cmd(dbt_ls_command)
    # logger.debug(f"parse_dbt_nodes_info__{cmd_out = }")
    dbt_nodes_info = {} #instead of a dict, use a list ?
    for raw_dbt_node_data in cmd_out.split("\n"):
        if "{" in raw_dbt_node_data:
            try:
                node_dict = json.loads(raw_dbt_node_data.strip())
                if node_dict["resource_type"] == "model" or node_dict["resource_type"] == "test":
                    dbt_node = DbtNode(
                        name=node_dict["name"],
                        unique_id=node_dict["unique_id"], #model.prefect_dbt.my_first_dbt_model
                        resource_type=node_dict["resource_type"],
                        depends_on=node_dict["depends_on"].get("nodes", []),
                        # file_path=dbt_config.dbt_project_dir / node_dict["original_file_path"],
                        # tags=node_dict["tags"],
                        # config=node_dict["config"],
                    )
                    dbt_nodes_info[dbt_node.unique_id] = dbt_node
            except json.decoder.JSONDecodeError:
                get_run_logger().debug(f"Skipping line: {raw_dbt_node_data}")
                print("error")
    #dbt_nodes_info = { unique_id : DbtNode }
    return dbt_nodes_info.values() #list of DbtNodes