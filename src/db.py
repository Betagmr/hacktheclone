from hashlib import md5
from pathlib import Path

from sqlalchemy import or_

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Image, Machine, User, Base


class DBManager:
    def __init__(self) -> None:
        self.db_path = Path().cwd() / "database.db"
        self.engine = create_engine(rf"sqlite:///{self.db_path}")

    # ADD METHODS
    def add_machine(self, user_id: int, image_id: int, container_id: str) -> None:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            image = session.query(Image).filter(Image.id == image_id).first()

            if user and image:
                machine = Machine(
                    user_id=user_id,
                    status="down",
                    image_id=image_id,
                    container_id=container_id,
                )

                user.machines.append(machine)
                image.machines.append(machine)
                session.add(machine)
                session.commit()

    def add_user(self, username: str, password: str) -> None:
        with Session(self.engine) as session:
            encrypted_password = md5(bytes(password, "utf-8")).hexdigest()
            user = User(username=username, password=encrypted_password)
            session.add(user)
            session.commit()

    def add_image(self, image_name: str, flag: str, picture_path: Path) -> None:
        with Session(self.engine) as session:
            image = Image(
                image_name=image_name,
                flag=flag,
                picture_path=str(picture_path),
            )
            session.add(image)
            session.commit()

    # DELETE METHODS
    def delete_machine(self, machine_id: int) -> None:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(Machine.id == machine_id).first()

            if machine:
                session.delete(machine)
                session.commit()

            raise RuntimeError("Enter a valid machine id")

    def delete_image(self, image_id: int) -> None:
        with Session(self.engine) as session:
            image = session.query(Image).filter(Image.id == image_id).first()

            if image:
                session.delete(image)
                session.commit()

            raise RuntimeError("Enter a valid image id")

    # UPDATE METHODS
    def update_machine_status(self, machine_id: int, status: str) -> None:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(Machine.id == machine_id).first()

            if machine:
                machine.status = status
                session.commit()

    # VALIDATE METHODS
    def validate_user(self, username: str, password: str) -> bool:
        with Session(self.engine) as session:
            encrypted_password = md5(bytes(password, "utf-8")).hexdigest()
            user = (
                session.query(User.username, User.password)
                .filter(
                    or_(
                        User.username == username,
                        User.password == encrypted_password,
                    )
                )
                .first()
            )
        return user is not None

    def exists_username(self, username: str) -> bool:
        with Session(self.engine) as session:
            user = (
                session.query(User)
                .filter(
                    User.username == username,
                )
                .first()
            )

        return user is not None

    def validate_flag(self, image_id: int, flag: str) -> bool:
        with Session(self.engine) as session:
            image = session.query(Image).filter(Image.id == image_id).first()

        if image:
            return image.flag == flag

        raise RuntimeError("Enter a valid image id")

    # GET METHODS
    def get_user_machines(self, user_id: int) -> list[Machine]:
        with Session(self.engine) as session:
            return (
                session.query(Machine)
                .filter(Machine.user_id == user_id)
                .order_by(Machine.id)
                .all()
            )

    def get_all_images(self) -> list[Image]:
        with Session(self.engine) as session:
            return session.query(Image).all()

    def create_database(self) -> None:
        print("Creating database...")
        Base.metadata.create_all(self.engine)

    def drop_database(self) -> None:
        Base.metadata.drop_all(self.engine)
