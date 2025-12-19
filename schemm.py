# schema.py

from pydantic import BaseModel, Field

class UserSignup(BaseModel):
    username: str
    password: str = Field(min_length=4, max_length=30)

class UserLogin(BaseModel):
    username: str
    password: str