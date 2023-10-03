from typing import List, Literal, Optional
from dataclasses import dataclass
import shutil

@dataclass
class DbtConfig:
    dbt_project_name: str
    dbt_project_dir: str
    dbt_profiles_dir: str
    dbt_target: str  #dev, prod, and others, better to leave it open ???
    dbt_exe: str = shutil.which("dbt")
    dbt_run_test_after_model: Optional[bool] = True
    dbt_print_stauts: Optional[bool] = False

@dataclass
class DbtNode:
    """Class representing a dbt node"""
    name: str
    unique_id: str
    resource_type: Literal["model", "test"] #keep dbt naming convention
    depends_on: List["DbtNode"] #what if the node depends on a macro?

@dataclass
class PrefectTask:
    name: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    retries: Optional[int] = None
    retry_delay_seconds: Optional[int] = None
    log_prints: Optional[bool] = None
    persist_result: Optional[bool] = None
    # wait_for: Optional[List[prefectFuture]] = None