# main.py
from modelss import User, Student, Department
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from St_Pd import engine
from schemm import UserSignup, DepartmentCreate, StudentsCreate, StudentDepartmentUpdate , UserLogin
from utils import hash_password, verify_password
from autht import create_access_token
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://st-dt-frontent-new.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



SessionLocal = sessionmaker(bind=engine)

@app.get("/")
def home():
    return "This is Home page of my website "

@app.get("/Student")
def get_students():
    session = SessionLocal()
    students = session.query(Student).all()
    result = []

    for s in students:
        result.append({
            "id": s.id,
            "name": s.name,
            "dept_id": s.dept_id
        })
    session.close()
    return result


@app.get("/departments")
def get_departments():
    session = SessionLocal()

    departments = session.query(Department).all()
    result = []

    for d in departments:
        result.append({
            "id": d.id,
            "name": d.name
        })

    session.close()
    return result



@app.post("/departments")
def post_department(dept: DepartmentCreate):
    session = SessionLocal()
    depart= Department(name=dept.name)
    session.add(depart)
    session.commit()
    session.close()
    return {"message": "Department added"}


    


@app.post("/students")
def post_Student(std: StudentsCreate):
    session = SessionLocal()
    std1=Student(name=std.name,
                 dept_id=std.dept_id)
    session.add(std1)
    session.commit()
    session.close()
    return {"message": "Student added successfully"}



@app.put("/students/{student_id}/update-all")
def update_student_and_department(
    student_id: int,
    data: StudentDepartmentUpdate
):
    session = SessionLocal()
    student = session.query(Student).filter(
        Student.id == student_id
    ).first()

    # student not found
    if not student:
        session.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    # update student name
    if data.student_name:
        student.name = data.student_name

    # update department
    if data.dept_id:
        department = session.query(Department).filter(
            Department.id == data.dept_id
        ).first()

        if not department:
            session.close()
            raise HTTPException(
                status_code=404,
                detail="Department not found"
            )

        student.dept_id = data.dept_id

    session.commit()
    session.close()
    return {"message": "Updated successfully"}





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




@app.post("/login")
def login(data: UserLogin):
    session = SessionLocal()

    user = session.query(User).filter(
        User.username == data.username
    ).first()

    if not user:
        session.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(data.password, user.hashed_password):
        session.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": user.username})

    session.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }





