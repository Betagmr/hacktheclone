from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    username: Mapped[str] = mapped_column(String(30))
    password: Mapped[str] = mapped_column(String(30))
    machines = relationship("Machine", backref="user", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"USER - Username={self.username}"


class Machine(Base):
    __tablename__ = "machine"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True)
    flag: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(10))
    user_id: Mapped[int] = mapped_column(Integer(), ForeignKey("user.id"))
    image_id: Mapped[int] = mapped_column(Integer(), ForeignKey("image.id"))

    def __str__(self) -> str:
        return f"MAHINE - {self.flag}"


class Image(Base):
    __tablename__ = "image"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    image_name: Mapped[str] = mapped_column(String(30))
    machines = relationship("Machine", backref="image", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"IMAGE - {self.image_name}"
