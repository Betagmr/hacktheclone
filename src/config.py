from pathlib import Path
from enum import Enum

class Page(int, Enum):
    LOGIN = 1
    REGISTER = 2
    APP = 3

MACHINE_FOLDER = Path().cwd() / "containers"

