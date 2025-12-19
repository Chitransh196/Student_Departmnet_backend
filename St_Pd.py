# Student_Project.py

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql://postgres:Radheradhe1@localhost:5432/ST_DP_CLG"

engine = create_engine(
    DATABASE_URL,
    echo=True
)
Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
