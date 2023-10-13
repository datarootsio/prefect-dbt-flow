import os
from pathlib import Path

import pytest

import duckdb
from duckdb import DuckDBPyConnection

from prefect.task_runners import SequentialTaskRunner

from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtProfile, DbtProject


SAMPLE_PROJECT_PATH = Path(__file__).parent.parent / "examples" / "sample_project"
JAFFLE_SHOP_PATH = Path(__file__).parent.parent / "examples" / "jaffle_shop_duckdb"


@pytest.fixture
def duckdb_db_file(monkeypatch, tmp_path: Path):
    duckdb_db_file = tmp_path / "dbt_test.duckdb"
    monkeypatch.setenv("DUCKDB_DB_FILE", str(duckdb_db_file))

    yield duckdb_db_file


def test_flow_sample_project(duckdb_db_file: Path):
    dbt_project_path = SAMPLE_PROJECT_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="sample_project",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": SequentialTaskRunner(),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4
        assert ddb.sql("SELECT * FROM my_model_d ORDER BY id").fetchall() == [
            (1,),
            (2,),
            (3,),
            (4,),
        ]


def test_flow_jaffle_shop(duckdb_db_file: Path):
    dbt_project_path = JAFFLE_SHOP_PATH

    my_dbt_flow = dbt_flow(
        project=DbtProject(
            name="jaffle_shop",
            project_dir=dbt_project_path,
            profiles_dir=dbt_project_path,
        ),
        profile=DbtProfile(
            target="test",
        ),
        flow_kwargs={
            # Ensure only one process has access to the duckdb db
            # file at the same time
            "task_runner": SequentialTaskRunner(),
        },
    )

    my_dbt_flow()

    with duckdb.connect(str(duckdb_db_file)) as ddb:
        assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 8
