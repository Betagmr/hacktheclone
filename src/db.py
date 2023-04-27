from hashlib import md5
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.models import Image, Machine, User


class DBManager:
    def __init__(self) -> None:
        self.db_path = Path().cwd() / "database.db"
        self.engine = create_engine(rf"sqlite:///{self.db_path}")

    def validate_user(self, username: str, password: str) -> bool:
        with Session(self.engine) as session:
            encrypted_password = md5(bytes(password, "utf-8")).hexdigest()
            user = (
                session.query(User)
                .filter(
                    User.username == username,
                    User.password == encrypted_password,
                )
                .first()
            )

            return user is not None

    def create_user(self, username: str, password: str) -> None:
        with Session(self.engine) as session:
            encrypted_password = md5(bytes(password, "utf-8")).hexdigest()
            user = User(username=username, password=encrypted_password)
            session.add(user)
            session.commit()

    def delete_machine(self, machine_id: int) -> None:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(Machine.id == machine_id).first()

            if machine:
                session.delete(machine)
                session.commit()

    def add_machine(self, user_id: int, root: str, image_id: int) -> None:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            image = session.query(Image).filter(Image.id == image_id).first()

            if user and image:
                machine = Machine(
                    user_id=user_id,
                    root=root,
                    status="Sin iniciar",
                    image_id=image_id,
                )
                user.machines.append(machine)
                image.machines.append(machine)
                session.commit()

    def update_status(self, machine_id: int, status: str) -> None:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(Machine.id == machine_id).first()

            if machine:
                machine.status = status
                session.commit()
