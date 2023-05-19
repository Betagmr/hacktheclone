from dataclasses import dataclass
from pathlib import Path

from config import MACHINE_FOLDER


@dataclass
class MachineInfo:
    container_name: str
    container_path: Path
    flag: str
    image: Path

    @property
    def display_name(self) -> str:
        return self.container_name.replace("_", " ").title()

    @property
    def tag(self) -> str:
        return f"hacktheclone_{self.container_name}"


def get_machines_info() -> list[MachineInfo]:
    machines = []

    for machine_folder in MACHINE_FOLDER.iterdir():
        container = machine_folder.name
        container_path = MACHINE_FOLDER / container

        image = container_path / "image.png"
        image = image if image.exists() else None

        flag_path = container_path / "root.txt"
        with open(flag_path, "r") as file:
            flag = file.readlines()[0].replace("\n", "")

        machine = MachineInfo(container, container_path, flag, image)
        machines.append(machine)

    return machines
