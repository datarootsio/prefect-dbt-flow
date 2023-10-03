from typing import List, Dict, Optional

from prefect import task

from prefect_dbt_flow.dbt import DbtNode
from prefect_dbt_flow.utils import cmd

DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"


def _task_dbt_run(dbt_node: DbtNode, task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_RUN_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_run():
        cmd.run("dbt run ...")

    return dbt_run


def _task_dbt_test(dbt_node: DbtNode, task_kwargs: Optional[Dict] = None):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_test():
        cmd.run("dbt test ...")

    return dbt_test


def generate_tasks_dag(
    dbt_graph: List[DbtNode],
    run_test_after_model: bool = False,
):
    def tasks():
        for dbt_node in dbt_graph:
            ...

    return tasks
