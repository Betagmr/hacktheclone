from typing import List
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey

Base = declarative_base()
engine = create_engine("sqlite://", echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username: Column(String(30))
    password: Column(String(30))

    machines = relationship("Machine", backref="user", cascade="all, delete-orphan")

    def __str__(self):
        return self.username
    
class Machine(Base):
    __tablename__ = "machines"
    id = Column(Integer, primary_key=True)
    root = Column(String(50))
    status = Column(String(10))
    user_id = Column(Integer, ForeignKey("user.id"))
    image_id = Column(Integer, ForeignKey("image.id"))

    def __str__(self):
        return self.root
    

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True)
    machines = relationship("Machine", backref="image", cascade="all, delete-orphan")


def get_user(user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    session.close()
    return user


def create_user(username, password):
    session = Session()
    user = User(username=username, password=password)
    session.add(user)
    session.commit()
    session.close()
    return user


def delete_machine(machine_id):
    session = Session()
    machine = session.query(Machine).filter(machine.id == machine_id).first()
    if machine:
        session.delete(machine)
        session.commit()
    session.close()


def add_machine(user_id, root, image_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    image = session.query(Image).filter(Image.id == image_id).first()
    if user and image:
        machine = Machine(user_id = user_id, root=root, status="Sin iniciar", image_id=image_id)
        user.machines.append(machine)
        image.machines.append(machine)
        session.commit()
    session.close


def update_status(machine_id, status):
    session = Session()
    machine = session.query(Machine).filter(machine.id == machine_id).first()
    if machine:
        machine.status = status
        session.commit()
    session.close()


if __name__ == '__main__':
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)