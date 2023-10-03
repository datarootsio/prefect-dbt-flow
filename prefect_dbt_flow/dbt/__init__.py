from typing import List, Literal
from dataclasses import dataclass


@dataclass
class DbtProject:
    name: str
    project_dir: str
    profiles_dir: str


@dataclass
class DbtProfile:
    target: str


@dataclass
class DbtNode:
    name: str
    node_type: Literal["model", "test"]
    depends_on: List["DbtNode"]
