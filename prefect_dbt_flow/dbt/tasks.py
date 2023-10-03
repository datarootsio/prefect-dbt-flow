from typing import List, Dict, Optional, Any

from prefect import task, get_run_logger

from prefect_dbt_flow.dbt import DbtNode, DbtProject, DbtProfile
from prefect_dbt_flow.dbt import cli


DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"


def _task_dbt_run(
    project: DbtProject,
    profile: DbtProfile,
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_RUN_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_run():
        dbt_run_output = cli.dbt_run(project, profile, dbt_node.name)
        get_run_logger().info(dbt_run_output)

    return dbt_run


def _task_dbt_test(
    project: DbtProject,
    profile: DbtProfile,
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
):
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} test_{dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_test():
        dbt_test_output = cli.dbt_test(project, profile, dbt_node.name)
        get_run_logger().info(dbt_test_output)

    return dbt_test


def generate_tasks_dag(
    project: DbtProject,
    profile: DbtProfile,
    dbt_graph: List[DbtNode],
    run_test_after_model: bool = False,
) -> None:
    # TODO: refactor this
    all_tasks = {
        dbt_node.unique_id: _task_dbt_run(
            project=project,
            profile=profile,
            dbt_node=dbt_node,
        )
        for dbt_node in dbt_graph
    }

    submitted_tasks: Dict[str, Any] = {}
    while node := _get_next_node(dbt_graph, list(submitted_tasks.keys())):
        run_task = all_tasks[node.unique_id]
        task_dependencies = [
            submitted_tasks[node_unique_id] for node_unique_id in node.depends_on
        ]

        run_task_future = run_task.submit(wait_for=task_dependencies)

        if run_test_after_model and node.has_tests:
            test_task = _task_dbt_test(
                project=project,
                profile=profile,
                dbt_node=node,
            )
            test_task_future = test_task.submit(wait_for=run_task_future)

            submitted_tasks[node.unique_id] = test_task_future
        else:
            submitted_tasks[node.unique_id] = run_task_future


def _get_next_node(
    dbt_graph: List[DbtNode], submitted_tasks: List[str]
) -> Optional[DbtNode]:
    for node in dbt_graph:
        if node.unique_id in submitted_tasks:
            continue

        node_dependencies = [node_unique_id for node_unique_id in node.depends_on]
        if set(node_dependencies) <= set(submitted_tasks):
            return node

    return None
