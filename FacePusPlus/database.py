from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from config import DB_URL

SQLALCHEMY_DATABASE_URL = DB_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

Base = declarative_base()


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    image = Column(String, nullable=False)
    faces = Column(JSON, nullable=True)