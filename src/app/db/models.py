from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Author(Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False)


class Blog(Base):
    __tablename__ = "blog"

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text)


class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    header = Column(String, nullable=False)
    text = Column(Text)
    author_id = Column(Integer, ForeignKey("author.id"), nullable=False)
    blog_id = Column(Integer, ForeignKey("blog.id"), nullable=False)


class SpaceType(Base):
    __tablename__ = "space_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class EventType(Base):
    __tablename__ = "event_type"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime, nullable=False)
    user_id = Column(Integer, nullable=False)
    space_type_id = Column(Integer, ForeignKey("space_type.id"), nullable=False)
    event_type_id = Column(Integer, ForeignKey("event_type.id"), nullable=False)
