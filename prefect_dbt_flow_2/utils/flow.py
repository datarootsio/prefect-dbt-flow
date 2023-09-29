from prefect import flow, Flow
from typing import Optional, Any
from prefect_dbt_flow_2.utils import graph, tasks, DbtConfig


def dbt_flow( #What do we want as default values?
    dbt_project_name: str,
    dbt_project_dir: str,
    dbt_profiles_dir: str,
    dbt_target: str = "dev",
    dbt_run_test_after_model: bool = True,
    dbt_print_stauts:bool = False,
    flow_kwargs: Optional[dict] = None,
)-> Flow[[], Any]:
    """
    Create a Prefect flow for running dbt tasks.

    Args:
        dbt_project_name (str): The name of the dbt project.
        dbt_project_dir (str): The directory where the dbt project is located.
        dbt_profiles_dir (str): The directory containing dbt profiles.
        flow_kwargs (dict, optional): Additional kwargs for the Prefect flow.
        ...

    Returns:
        prefect.Flow: The Prefect flow for running dbt tasks.
    """
    all_flow_kwargs = {
        "name": dbt_project_name,
        **(flow_kwargs or {}),
    }
    
    

    @flow(**all_flow_kwargs)
    def run_dbt_flow():  #Why not inside of the flow?
        dbt_config=DbtConfig(
            dbt_project_name=dbt_project_name,
            dbt_project_dir=dbt_project_dir,
            dbt_profiles_dir=dbt_profiles_dir,
            dbt_target=dbt_target,
            dbt_run_test_after_model=dbt_run_test_after_model,
            dbt_print_stauts=dbt_print_stauts,
        )

        # dbt_graph = graph.parse_dbt_nodes_info(dbt_config) #Why not inside of the flow?

        # tasks.geneate_tasks_dag(
        #     dbt_graph=dbt_graph,
        #     dbt_config=dbt_config,
        #     )

    return run_dbt_flow