from pathlib import Path

import docker
from docker import DockerClient
from docker.models.containers import Container
from docker.models.images import Image


class MachineController:
    def __init__(self) -> None:
        self.client: DockerClient = docker.from_env()
        self.running_machine: Container = None

    @property
    def image_list(self) -> list[Image]:
        return self.client.images.list()

    @property
    def container_list(self) -> list[Container]:
        return self.client.containers.list(all=True)

    def build_image(self, machine_path: Path) -> Image:
        folder_name = machine_path.name
        tag = f"hacktheclone_{folder_name}"

        return self.client.images.build(path=str(machine_path), tag=tag)[0]

    def run_machine(self, image: Image) -> Container:
        if not self.running_machine:
            self.running_machine = self.client.containers.run(image=image, detach=True)
            return self.running_machine

        raise RuntimeError("Machine already running - Stop it first")

    def reset_running_machine(self) -> Container:
        if self.running_machine:
            image = self.running_machine.image
            self.running_machine.stop()
            self.running_machine.remove()

            return self.run_machine(image)

        raise RuntimeError("No machine running - Start one first")

    def stop_running_machine(self) -> Container:
        if self.running_machine:
            machine = self.running_machine
            machine.stop()
            self.running_machine = None

            return machine

        raise RuntimeError("No machine running - Start one first")

    def start_stoped_machine(self, machine: Container) -> Container:
        if not self.running_machine:
            self.running_machine = machine
            self.running_machine.start()

            return self.running_machine

        raise RuntimeError("Machine already running - Stop it first")

    def delete_stoped_machine(self, machine: Container) -> Container:
        return machine.remove()
