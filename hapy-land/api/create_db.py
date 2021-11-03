from .database import Base, engine
from sqlalchemy_utils import create_database, database_exists


from .models import *


def create_db(Base=Base, engine=engine):
    if not database_exists(engine.url):
        create_database(engine.url)

    Base.metadata.create_all(engine)
