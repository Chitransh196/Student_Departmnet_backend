# schema.py

from pydantic import BaseModel, Field
from typing import Optional

class UserSignup(BaseModel):
    username: str
    password: str = Field(min_length=4, max_length=30)

class UserLogin(BaseModel):
    username: str
    password: str

class DepartmentCreate(BaseModel):
    name: str

class StudentsCreate(BaseModel):
    name: str
    dept_id: str

class StudentUpdate(BaseModel):
    name: str
    dept_id: int

class StudentDepartmentUpdate(BaseModel):
    student_name: Optional[str] = None
    dept_id: Optional[int] = None
    dept_name: Optional[str] = None
