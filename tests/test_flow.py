import os
from pathlib import Path

import duckdb

from prefect.task_runners import SequentialTaskRunner

from prefect_dbt_flow.dbt import DbtProject, DbtProfile
from prefect_dbt_flow import dbt_flow


def test_flow_basic(tmp_path: Path):
    duckdb_db_file = str(tmp_path / "dbt_test.duckdb")
    dbt_project_path = Path(__file__).parent.parent / "examples" / "sample_project"

    os.environ["DUCKDB_DB_FILE"] = duckdb_db_file

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
            # Ensure only one process has access to the duckdb database file at the same time
            "task_runner": SequentialTaskRunner(),
        },
    )

    my_dbt_flow()

    ddb = duckdb.connect(duckdb_db_file)

    assert len(ddb.sql("SHOW ALL TABLES").fetchall()) == 4
    assert ddb.sql("SELECT * FROM my_model_d ORDER BY id").fetchall() == [
        (1,),
        (2,),
        (3,),
        (4,),
    ]
