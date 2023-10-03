from prefect import flow, Flow
from typing import Optional, Any
from utils import graph, tasks, DbtConfig, logging_config

logger = logging_config.logger


def dbt_flow( #What do we want as default values?
    dbt_project_name: str,
    dbt_project_dir: str,
    dbt_profiles_dir: str,
    dbt_target: str,
    dbt_exe: Optional[str],
    dbt_run_test_after_model: Optional[bool],
    dbt_print_stauts: Optional[bool],
    flow_kwargs: Optional[dict],
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
    logger.debug(f"dbt_flow__{all_flow_kwargs = }")


    @flow(**all_flow_kwargs)
    def run_dbt_flow():
        dbt_config=DbtConfig(
            dbt_project_name=dbt_project_name,
            dbt_project_dir=dbt_project_dir,
            dbt_profiles_dir=dbt_profiles_dir,
            dbt_target=dbt_target,
            dbt_exe=dbt_exe,
            dbt_run_test_after_model=dbt_run_test_after_model,
            dbt_print_stauts=dbt_print_stauts,
        )
        # logger.debug(f"run_dbt_flow__{dbt_config = }")

        dbt_graph = graph.parse_dbt_nodes_info(dbt_config)
        # logger.debug(f"run_dbt_flow__{dbt_graph = }")
        #Return a list of DbtNodes

        pool_futures = {}
        if dbt_run_test_after_model:
            for dbt_node in dbt_graph:
                upstream_futures = [pool_futures[dependency] for dependency in dbt_node.depends_on] #on the first run, should be [], the second should be a list of prefectFutures
                dbt_task = tasks._task_dbt_test( #returns prefect.tasks.Task
                    dbt_node=dbt_node, 
                    dbt_config=dbt_config,
                    name=dbt_node.name, #the name has to be the same as wait for?...
                    wait_for= upstream_futures,
                ) #here, upstrean futures is str, a prefect future is needed... dbt_task_0, dbt_task_2...
                # state_dbt_task = dbt_task.wait() #Wait for the run to finish and return the final state
                pool_futures[dbt_node.unique_id] = dbt_task #saves the future as {"dbt_node.name" : dtb_task=prefectfuture}
                logger.debug(f"run_dbt_flow__{dbt_node.name = } {dbt_task = }")
        else:
            pass
        logger.debug(f"run_dbt_flow__{pool_futures.values() = }")
        return pool_futures
    
    run = run_dbt_flow()
    logger.debug(f"run_dbt_flow__{run = }")
    return run