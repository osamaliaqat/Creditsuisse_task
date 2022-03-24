from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime


staging_pg_engine = create_engine("postgresql://user:password@host/database")
staging_pg_conn = staging_pg_engine.connect()
Base = declarative_base()


class user(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50))
    email = Column(String(50))
    password = Column(String(500))


class posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    post_description = Column(String(50))
    created_at = Column(DateTime)
