# main.py

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from St_Pd import engine
from modelss import User
from schemm import UserSignup
from utils import hash_password

app = FastAPI()

SessionLocal = sessionmaker(bind=engine)

@app.post("/signup")
def signup(data: UserSignup):
    session = SessionLocal()

    existing_user = session.query(User).filter(User.username == data.username).first()

    if existing_user:
        session.close()
        raise HTTPException(status_code=400, detail="User exists")

    new_user = User(
        username=data.username, hashed_password=hash_password(data.password)
    )

    session.add(new_user)
    session.commit()
    session.close()

    return {"message": "User registered successfully"}
