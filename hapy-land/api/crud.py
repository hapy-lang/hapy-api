from sqlalchemy.orm import Session

from . import models, schemas
from .utils import slugify

def get_user(db: Session, user_id: int):

    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):

    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str):

    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_examples(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Challenge).offset(skip).limit(limit).all()

def create_example(db: Session, item: schemas.BiteCreate, user_id: int, challenge_id: int):
    db_example = models.Solution(**item.dict(), owner_id=user_id, challenge_id=challenge_id)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example


def get_bites(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.BiteBase).offset(skip).limit(limit).all()

def get_bite_by_id(db: Session, bite_id: int):
    return db.query(models.BiteBase).filter(models.BiteBase.id == bite_id).first()

def get_bite_by_slug(db: Session, bite_slug: str):
    return db.query(models.BiteBase).filter(models.BiteBase.slug == bite_slug).first()

def create_bite(db: Session, item: schemas.BiteCreate, submitter_id: int, hapy_v: str):
    slug = slugify(item.dict()["title"])

    db_bite = models.BiteBase(**item.dict(), slug=slug, submitter_id=submitter_id, hapy_version=hapy_v)
    db.add(db_bite)
    db.commit()
    db.refresh(db_bite)
    return db_bite

def get_solutions(db: Session, skip: int = 0, limit: int = 100):

    return db.query(models.Solution).offset(skip).limit(limit).all()

def create_solution(db: Session, item: schemas.BiteCreate, challenge_id: int, submitter_id: int, hapy_v: str):
    slug = slugify(item.dict()["title"])
    db_solution = models.Solution(**item.dict(), slug=slug, challenge_id=challenge_id, submitter_id=submitter_id, hapy_version=hapy_v)
    db.add(db_solution)
    db.commit()
    db.refresh(db_solution)
    return db_solution

def get_challenges(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Challenge).offset(skip).limit(limit).all()

def get_challenge_by_id(db: Session, challenge_id: int):
    return db.query(models.Challenge).filter(models.Challenge.id == challenge_id).first()

def create_challenge(db: Session, item: schemas.ChallengeCreate):
    slug = slugify(item.dict()["title"])
    db_challenge = models.Challenge(**item.dict(), slug=slug)
    db.add(db_challenge)
    db.commit()
    db.refresh(db_challenge)
    return db_challenge


