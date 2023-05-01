from pathlib import Path

import pytest

from src.db import DBManager
from src.models import Base


@pytest.fixture
def db() -> DBManager:
    db = DBManager()
    Base.metadata.drop_all(DBManager().engine)
    Base.metadata.create_all(db.engine)
    return db


@pytest.mark.parametrize(
    ("username, password, password2, expected"),
    [
        ("User", "Pass", "Pass", True),
        ("User", "Pass", "WrongPass", False),
    ],
)
def test_add_to_database(
    db: DBManager, username: str, password: str, password2: str, expected: bool
) -> None:
    db.add_user(username, password)
    assert db.validate_user(username, password2) == expected


def test_add_image(db: DBManager) -> None:
    db.add_image("Windows 10", "flagwindows_flag", Path().cwd() / "windows.png")
    db.add_image("Ubuntu", "flagubuntu_flag", Path().cwd() / "ubuntu.png")
    assert len(db.get_all_images()) == 2


def test_add_machine(db: DBManager) -> None:
    db.add_user("User", "Pass")
    db.add_image("Windows 10", "flagwindows_flag", Path().cwd() / "windows.png")
    db.add_image("Ubuntu", "flagubuntu_flag", Path().cwd() / "ubuntu.png")
    db.add_machine(1, 1, "container_id")
    db.add_machine(1, 2, "container_id2")
    assert len(db.get_user_machines(1)) == 2


def test_update_machine_status(db: DBManager) -> None:
    db.add_user("User", "Pass")
    db.add_image("Windows 10", "flagwindows_flag", Path().cwd() / "windows.png")
    db.add_machine(1, 1, "container_id")

    machine = db.get_user_machines(1)[0]
    assert machine.status == "down"

    db.update_machine_status(machine.id, "up")
    machine = db.get_user_machines(1)[0]
    assert machine.status == "up"

    db.update_machine_status(machine.id, "stop")
    machine = db.get_user_machines(1)[0]
    assert machine.status == "stop"


def test_validate_flag(db: DBManager) -> None:
    db.add_user("User", "Pass")
    db.add_image("Windows 10", "flagwindows_flag", Path().cwd() / "windows.png")

    assert db.validate_flag(1, "flagwindows_flag") == True
    assert db.validate_flag(1, "flagwindows_flag2") == False
