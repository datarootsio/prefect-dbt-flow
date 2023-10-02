from typing import List, Literal
from dataclasses import dataclass
import os
from shutil import which


@dataclass
class DbtConfig:
    dbt_project_name: str
    dbt_project_dir: str
    dbt_profiles_dir: str
    dbt_target: str  #dev, prod, and others, better to leave it open ???
    dbt_exe: str
    dbt_run_test_after_model: bool
    dbt_print_stauts:bool

@dataclass
class DbtNode:
    """Class representing a dbt node"""
    name: str
    resource_type: Literal["model", "test"] #keep dbt naming convention
    depends_on: List["DbtNode"] #what if the node depends on a macro?
