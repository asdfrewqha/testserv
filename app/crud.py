from models import User
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError


def createUser(
        db,
        id: str,
        name: str,
        email: str,
        pwd_hash: str,
        token: str):
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return None
        user = User(
            id=id,
            name=name,
            email=email,
            password_hash=pwd_hash,
            token=token)
        db.add(user)
        db.commit()  # Commit the transaction
        db.refresh(user)
        return user

    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise


def get(db: Session, query, filter_q, filter):
    try:
        return db.query(query).filter(filter_q == filter).first()
    except ProgrammingError:
        return None


def read(
    db: Session,
    query,
    filter_q,
    filter,
    limit: int = 0,
    offset: int = 10,
    sort: str = None,
):
    if not sort:
        sort = "id"
    return (
        db.query(query)
        .filter(filter_q == filter)
        .order_by(sort)
        .offset(offset)
        .limit(limit)
        .all()
    )

def updtoken(db: Session, query, id: str, obj: str):
    upd = db.query(query).filter(query.id == id).first()
    upd.token = obj
    db.commit()
