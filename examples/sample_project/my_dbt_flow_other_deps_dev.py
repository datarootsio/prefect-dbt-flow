from pathlib import Path

from prefect import task, flow
from prefect.task_runners import SequentialTaskRunner

from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtProfile, DbtProject

my_dbt_flow = dbt_flow(
    project=DbtProject(
        name="sample_project",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="dev",
    ),
    flow_kwargs={
        # Ensure only one process has access to the duckdb db
        # file at the same time
        "task_runner": SequentialTaskRunner(),
    },
)


@flow
def upstream_flow():
    @task
    def upstream_flow_task():
        print("upstream flow")

    upstream_flow_task()


@flow
def downstream_flow():
    @task
    def downstream_flow_task():
        print("downstream flow")

    downstream_flow_task()


@task
def upstream_task():
    print("upstream task")


@task
def downstream_task():
    print("downstream task")


@flow(log_prints=True)
def main_flow():
    uf_future = upstream_flow(return_state=True)
    ut_future = upstream_task(return_state=True)

    dbt_future = my_dbt_flow(wait_for=[uf_future, ut_future])

    downstream_flow(wait_for=[dbt_future])
    downstream_task(wait_for=[dbt_future])


if __name__ == "__main__":
    main_flow()
