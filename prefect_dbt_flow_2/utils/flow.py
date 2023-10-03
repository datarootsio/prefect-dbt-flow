from prefect import flow, Flow
from typing import Optional, Any
import shutil
from prefect_dbt_flow_2.utils import graph, tasks, DbtConfig



def dbt_flow( #What do we want as default values?
    dbt_project_name: str,
    dbt_project_dir: str,
    dbt_profiles_dir: str,
    dbt_target: str,
    dbt_exe: str,
    dbt_run_test_after_model: bool,
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

        dbt_graph = graph.parse_dbt_nodes_info(dbt_config)
        #Return a list of DbtNodes

        pool_futures = {}
        if dbt_run_test_after_model:
            for dbt_node in dbt_graph:
                upstream_futures = [pool_futures[dependency] for dependency in dbt_node.depends_on] #on the first run, should be [], the second should be a list of prefectFutures
                dbt_task = tasks._task_dbt_test.with_options( #will this create a future? what if the list is not in order?
                    name=dbt_node.name, #the name has to be the same as wait for?...
                    dbt_node=dbt_node, 
                    dbt_config=dbt_config,
                    wait_for=upstream_futures) #here, upstrean futures is str, a prefect future is needed... dbt_task_0, dbt_task_2...
                state_dbt_task = dbt_task.wait() #Wait for the run to finish and return the final state
                pool_futures[dbt_node.name] = dbt_task #saves the future as {"dbt_node.name" : dtb_task=prefectfuture}
        else:
            for dbt_node in dbt_graph:
                upstream_futures = [pool_futures[dependency] for dependency in dbt_node.depends_on]
                dbt_task = tasks._task_dbt_run.with_options(
                    name=dbt_node.name,
                    dbt_node=dbt_node,
                    dbt_config=dbt_config,
                    wait_for=upstream_futures)
                state_dbt_task = dbt_task.wait()
                pool_futures[dbt_node.name] = state_dbt_task
        
        return pool_futures

    return run_dbt_flow