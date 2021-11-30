from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    TIMESTAMP,
    Text,
    event,
)
from sqlalchemy.orm import relationship

from .database import Base
from .utils import slugify


# DB Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)
    password = Column(String(25), nullable=False)
    email = Column(Text, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    # Relationships
    bites = relationship("BiteBase", back_populates="uploaded_by")

    def __repr__(self) -> str:
        return f"<User id: {self.id}, username: {self.username}, created: {self.created_at}>"


class UserLogin(Base):
    __tablename__ = "logins"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("users.id"))
    user_agent = Column(Text)
    mac_address = Column(Text)
    ip_address = Column(Text)
    timestamp = Column(TIMESTAMP, nullable=False)


class BiteBase(Base):
    __tablename__ = "bites"
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(Text(), nullable=False)
    # short title of the snippet
    title = Column(String(255), nullable=False)
    slug = Column(String(255))
    # Markdown Enabled description!
    description = Column(Text())
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())
    submitter_id = Column(Integer, ForeignKey("users.id"))
    hapy_version = Column(Text())
    # relationship
    uploaded_by = relationship("User", back_populates="bites")
    downloads = Column(Integer, default=0)
    stars = Column(Integer, default=0)
    # the version of the code/solution
    version = Column(Integer, default=1)
    # whether it's a solution or pure bite
    type = Column(String(20), nullable=False, default="bite")

    __mapper_args__ = {"polymorphic_on": type, "polymorphic_identity": "bite"}

    def __repr__(self) -> str:
        return f"<Bite ({self.type}) id: {self.id}, title: {self.title}, owner: @{self.uploaded_by.username}, created: {self.created_at}>"


class Solution(BiteBase):
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    challenge = relationship("Challenge", back_populates="solutions")

    __mapper_args__ = {"polymorphic_identity": "solution"}


# from: https://docs.sqlalchemy.org/en/14/orm/inheritance.html


class Challenge(Base):
    __tablename__ = "challenges"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    slug = Column(String(255))
    description = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.now())
    updated_at = Column(TIMESTAMP, default=datetime.now())
    solutions = relationship("Solution", back_populates="challenge")

    def __repr__(self) -> str:
        return f"<Challenge id: {self.id}, title: '{self.title}', solutions: {len(self.solutions)}>"


# event.listen(Challenge.title, 'set', Challenge.generate_slug, retval=False)


@event.listens_for(Challenge.title, "set")
# @event.listens_for(BiteBase.title, 'set')
def generate_slug(target, value, oldvalue, initiator):
    print("generating slug", value)
    if value and (not target.slug or value != oldvalue):
        target.slug = slugify(value)
        print("slug", target.slug)
