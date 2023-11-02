"""Code for generate prefect DAG, includes dbt run and test functions"""
from typing import Dict, List, Optional

from prefect import Task, get_run_logger, task
from prefect.futures import PrefectFuture

from prefect_dbt_flow.dbt import (
    DbtDagOptions,
    DbtNode,
    DbtProfile,
    DbtProject,
    DbtResourceType,
    cli,
)
from prefect_dbt_flow.dbt.profile import override_profile

DBT_RUN_EMOJI = "🏃"
DBT_TEST_EMOJI = "🧪"
DBT_SEED_EMOJI = "🌱"
DBT_SNAPSHOT_EMOJI = "📸"


def _task_dbt_snapshot(
    project: DbtProject,
    profile: Optional[DbtProfile],
    dag_options: Optional[DbtDagOptions],
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
) -> Task:
    """
    Create a Prefect task for running a dbt snapshot. Uses dbt_snapshot from cli module

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        dag_options: A class to add dbt DAG configurations.
        dbt_node: A class that represents the dbt node (model) to run.
        task_kwargs: Additional task configuration.

    Returns:
        dbt_snapshot: Prefect task.
    """
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_SNAPSHOT_EMOJI} snapshot_{dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_snapshot():
        """
        Snapshots a dbt snapshot

        Returns:
            None
        """
        with override_profile(project, profile) as _project:
            if not dag_options or dag_options.install_deps:
                dbt_deps_output = cli.dbt_deps(_project, profile, dag_options)
                get_run_logger().info(dbt_deps_output)

            dbt_snapshot_output = cli.dbt_snapshot(
                _project, dbt_node.name, profile, dag_options
            )
            get_run_logger().info(dbt_snapshot_output)

    return dbt_snapshot


def _task_dbt_seed(
    project: DbtProject,
    profile: Optional[DbtProfile],
    dag_options: Optional[DbtDagOptions],
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
) -> Task:
    """
    Create a Prefect task for running a dbt seed. Uses dbt_seed from cli module

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        dag_options: A class to add dbt DAG configurations.
        dbt_node: A class that represents the dbt node (model) to run.
        task_kwargs: Additional task configuration.

    Returns:
        dbt_seed: Prefect task.
    """
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_SEED_EMOJI} seed_{dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_seed():
        """
        Seeds a dbt seed

        Returns:
            None
        """
        with override_profile(project, profile) as _project:
            if not dag_options or dag_options.install_deps:
                dbt_deps_output = cli.dbt_deps(_project, profile, dag_options)
                get_run_logger().info(dbt_deps_output)

            dbt_seed_output = cli.dbt_seed(
                _project, dbt_node.name, profile, dag_options
            )
            get_run_logger().info(dbt_seed_output)

    return dbt_seed


def _task_dbt_run(
    project: DbtProject,
    profile: Optional[DbtProfile],
    dag_options: Optional[DbtDagOptions],
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
) -> Task:
    """
    Create a Prefect task for running a dbt model. Uses dbt_run from cli module

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        dag_options: A class to add dbt DAG configurations.
        dbt_node: A class that represents the dbt node (model) to run.
        task_kwargs: Additional task configuration.

    Returns:
        dbt_run: A prefect task.
    """
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_RUN_EMOJI} {dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_run():
        """
        Run a dbt model.

        Returns:
            None
        """
        with override_profile(project, profile) as _project:
            if not dag_options or dag_options.install_deps:
                dbt_deps_output = cli.dbt_deps(_project, profile, dag_options)
                get_run_logger().info(dbt_deps_output)

            dbt_run_output = cli.dbt_run(_project, dbt_node.name, profile, dag_options)
            get_run_logger().info(dbt_run_output)

    return dbt_run


def _task_dbt_test(
    project: DbtProject,
    profile: Optional[DbtProfile],
    dag_options: Optional[DbtDagOptions],
    dbt_node: DbtNode,
    task_kwargs: Optional[Dict] = None,
) -> Task:
    """
    Create a Prefect task for testing a dbt model. Uses dbt_test from cli module

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        dag_options: A class to add dbt DAG configurations.
        dbt_node: A class that represents the dbt node (model) to run.
        task_kwargs: Additional task configuration.

    Returns:
        dbt_test: Prefect task.
    """
    all_task_kwargs = {
        **(task_kwargs or {}),
        "name": f"{DBT_TEST_EMOJI} test_{dbt_node.name}",
    }

    @task(**all_task_kwargs)
    def dbt_test():
        """
        Test a dbt model

        Returns:
            None
        """
        with override_profile(project, profile) as _project:
            if not dag_options or dag_options.install_deps:
                dbt_deps_output = cli.dbt_deps(_project, profile, dag_options)
                get_run_logger().info(dbt_deps_output)

            dbt_test_output = cli.dbt_test(
                _project, dbt_node.name, profile, dag_options
            )
            get_run_logger().info(dbt_test_output)

    return dbt_test


RESOURCE_TYPE_TO_TASK = {
    DbtResourceType.SEED: _task_dbt_seed,
    DbtResourceType.MODEL: _task_dbt_run,
    DbtResourceType.SNAPSHOT: _task_dbt_snapshot,
}


def generate_tasks_dag(
    project: DbtProject,
    profile: Optional[DbtProfile],
    dag_options: Optional[DbtDagOptions],
    dbt_graph: List[DbtNode],
    run_test_after_model: bool = False,
) -> None:
    """
    Generate a Prefect DAG for running and testing dbt models.

    Args:
        project: A class that represents a dbt project configuration.
        profile: A class that represents a dbt profile configuration.
        dag_options: A class to add dbt DAG configurations.
        dbt_graph: A list of dbt nodes (models) to include in the DAG.
        run_test_after_model: If True, run tests after running each model.

    Returns:
        None
    """

    # TODO: refactor this
    all_tasks = {
        dbt_node.unique_id: RESOURCE_TYPE_TO_TASK[dbt_node.resource_type](
            project=project,
            profile=profile,
            dag_options=dag_options,
            dbt_node=dbt_node,
        )
        for dbt_node in dbt_graph
    }

    submitted_tasks: Dict[str, PrefectFuture] = {}
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
                dag_options=dag_options,
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
