from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Text,
)
from sqlalchemy.orm import relationship

from .database import Base


# DB Models
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False, unique=True)
    timestamp = Column(TIMESTAMP, nullable=False)
    password = Column(String(25), nullable=False)
    email = Column(Text, nullable=False)

    # Relationships
    solutions = relationship("BiteBase", back_populates="uploaded_by")

    def __repr__(self) -> str:
        return f"<class User>id: {self.id}, username: {self.username}, timestamp: {self.timestamp} "


class UserLogin(Base):
    __tablename__ = "login"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("user.id"))
    user_agent = Column(Text)
    mac_address = Column(Text)
    ip_address = Column(Text)
    timestamp = Column(TIMESTAMP, nullable=False)


class BiteBase(Base):
    __tablename__ = "bite"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text(), nullable=False)
    upload_timestamp = Column(TIMESTAMP)
    submitter_id = Column(Integer, ForeignKey("user.id"))
    # relationship
    uploaded_by = relationship("User", back_populates="solutions")


class Answer(BiteBase):
    challenge_id = Column(Integer, ForeignKey("challenge.id"))
    challenge = relationship("Challenge", back_populates="submitted_answers")


class Challenge(Base):
    __tablename__ = "challenge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    upload_timestamp = Column(TIMESTAMP)
    submitted_answers = relationship("Answer", back_populates="challenge")
