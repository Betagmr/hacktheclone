from typing import List
from sqlalchemy.orm import backref, relationship, sessionmaker, Session, DeclarativeBase
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from pathlib import Path

class Base(DeclarativeBase): 
    pass

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String(30))
    password = Column(String(30))

    machines = relationship("Machine", backref="user", cascade="all, delete-orphan")

    def __repr__(self):
        return self.username
    
class Machine(Base):
    __tablename__ = "machine"
    id = Column(Integer, primary_key=True)
    root = Column(String(50))
    status = Column(String(10))
    user_id = Column(Integer, ForeignKey("user.id"))
    image_id = Column(Integer, ForeignKey("image.id"))

    def __str__(self):
        return self.root
    

class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    machines = relationship("Machine", backref="image", cascade="all, delete-orphan")


class DBManager():

    def __init__(self):
        self.db_path = Path().cwd() / 'database.db'
        self.engine = create_engine(rf"sqlite:///{self.db_path}", echo=True)


    def get_user(self, user_id: int) -> User:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        

    def create_user(self, username: str, password: str) -> User:
        with Session(self.engine) as session:
            user = User(username=username, password=password)
            session.add(user)
            session.commit()
            session.expunge(user)
            return user


    def delete_machine(self, machine_id: int) -> None | Machine:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(machine.id == machine_id).first()
            if machine:
                session.delete(machine)
                session.commit()
                return machine
            
            return None



    def add_machine(self, user_id: int, root: str, image_id: int) -> None | Machine:
        with Session(self.engine) as session:
            user = session.query(User).filter(User.id == user_id).first()
            image = session.query(Image).filter(Image.id == image_id).first()
            
            if user and image:
                machine = Machine(user_id = user_id, root=root, status="Sin iniciar", image_id=image_id)
                user.machines.append(machine)
                image.machines.append(machine)
                session.commit()
                return machine
            
            return None


    def update_status(self, machine_id: int, status: str) -> None | Machine:
        with Session(self.engine) as session:
            machine = session.query(Machine).filter(machine.id == machine_id).first()
            if machine:
                machine.status = status
                session.commit()
                return machine
            
            return None
        

