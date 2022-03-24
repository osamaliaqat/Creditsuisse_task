from models import staging_pg_engine, user
from sqlalchemy.orm import Session


def get_user(email, password):
    session = Session(bind=staging_pg_engine, expire_on_commit=False)
    users = session.query(user).filter_by(email=email, password=password).first()
    return users