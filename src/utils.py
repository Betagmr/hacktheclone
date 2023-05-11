from pathlib import Path
from dataclasses import dataclass

@dataclass
class MachineInfo():
    container_name: str
    flag: str
    image: Path
        

def get_machines_info() -> list[MachineInfo]:
    machines = []

    folder_path = Path().cwd() / 'containers'
    for machine_folder in folder_path.iterdir():
        container = machine_folder.name
        container_path = folder_path / container
        
        image = container_path / 'images.jpeg'

        flag_path = container_path / 'root.txt'
        with open(flag_path, "r") as file:
            flag = file.readlines()[0].replace('\n', '')

        machine = MachineInfo(container, flag, image)
        machines.append(machine)

    return machines
