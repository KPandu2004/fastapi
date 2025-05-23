# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
#
# from fastapi import FastAPI, Depends, HTTPException
# from pydantic import BaseModel
# app = FastAPI()
#
# students = []
#
# class Student(BaseModel):
#     name: str
#     age: int
#     grade: int
# @app.get("/")
# def read_root():
#     return {"Message": "Welcome to FastAPI!"}
#
# @app.get("/students")
# def get_students():
#     return students
# @app.head("/students")
# def head_students():
#     return {"X-Total students": len(students)}
#
# @app.options("/students")
# def options_students():
#     return {
#         "allowed_methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
#     }
# @app.post("/students")
# def create_student(student: Student):
#     students.append(student.dict())
#     return {"message": "Student added","data" : Student}
#
# @app.put("/students/{student_id}")
# def get_student(student_id: int):
#     if 0 <= student_id < len(students):
#         return students[student_id]
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.put("/students/{student_id}")
# def update_student(student_id: int, student: Student):
#     if 0 <= student_id < len(students):
#         students[student_id] = student.dict()
#         return {"Message": "Student updated","data" : students}
#     raise HTTPException(status_code=404, detail="Student not found")
#
#
# @app.patch("/students/{student_id}")
# def partial_update_student(student_id: int,student: Student):
#     if 0 <= student_id < len(students):
#         current_data = students[student_id]
#         update_data = student.dict(exclude_unset=True)
#         current_data.update(update_data)
#         student[student_id] = current_data
#         return {"Message": "Student partially updated","data" : current_data}
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.delete("/students/{student_id}")
# def delete_student(student_id: int):
#     if 0 <= student_id < len(students):
#         removed = students.pop(student_id)
#         return {"Message": "Student removed","data" : removed}
#     raise HTTPException(status_code=404, detail="Student not found")
#
# @app.get("/search")
# def search_students(name:str = None):
#     if name:
#         results =  [s for s in students if s["name"].lower() == name.lower()]
#         return { "results":results}
#     return { "message": "no name found" }
#
# def common_dependency():
#     return {"note": "common dependency injected"}
#
# @app.get(":/check")
# def check(dep=Depends(common_dependency)):
#     return dep


from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse

app = FastAPI()

students = []


# Pydantic model for full data (POST)
class Student(BaseModel):
    name: str
    age: int
    grade: str


# Pydantic model for partial data (PATCH)
class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None


# Custom exception class
class StudentNotFound(Exception):
    def __init__(self, student_id: int):
        self.student_id = student_id


# Custom exception handler
@app.exception_handler(StudentNotFound)
def student_not_found_handler(request: Request, exc: StudentNotFound):
    return JSONResponse(


        status_code=404,
        content={"message": f"Student with ID {exc.student_id} not found."},
    )


# POST - Add a new student
@app.post("/students", status_code=status.HTTP_201_CREATED)
def create_student(student: Student):
    students.append(student.model_dump())
    return {
        "message": "Student added successfully",
        "data": student
    }


# PATCH - Update existing student partially
@app.patch("/students/{student_id}")
def partial_update_student(student_id: int, student: UpdateStudent):
    if student_id < 0 or student_id >= len(students):
        raise StudentNotFound(student_id)

    updated_data = student.model_dump(exclude_unset=True)
    students[student_id].update(updated_data)

    return {
        "message": "Student updated successfully",
        "data": students[student_id]
    }


# GET - Retrieve all students (optional utility)
@app.get("/students")
def get_all_students():
    return {
        "message": "List of all students",
        "data": students
    }

