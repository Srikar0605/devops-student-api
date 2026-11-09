
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

#hiiiiiiiii
class Student(BaseModel):
    id: int = Field(gt=0)
    name: str
    maths: float = Field(ge=0, le=100)
    physics: float = Field(ge=0, le=100)
    chemistry: float = Field(ge=0, le=100)

class StudentUpdate(BaseModel):
    name: str | None = None
    maths: float | None = Field(default=None, ge=0, le=100)
    physics: float | None = Field(default=None, ge=0, le=100)
    chemistry: float | None = Field(default=None, ge=0, le=100)

students = {}

# POST - Create student
@app.post("/students")
def create_student(s: Student):
    if s.id in students:
        raise HTTPException(400, "Student already exists")
    students[s.id] = s
    return s

# GET - Read all students
@app.get("/students")
def get_students():
    return list(students.values())

# GET - Read one student
@app.get("/students/{sid}")
def get_student(sid: int):
    if sid not in students:
        raise HTTPException(404, "Student not found")
    return students[sid]

# PATCH - Update student
@app.patch("/students/{sid}")
def update_student(sid: int, s: StudentUpdate):
    if sid not in students:
        raise HTTPException(404, "Student not found")
    students[sid] = students[sid].model_copy(
        update=s.model_dump(exclude_unset=True)
    )
    return students[sid]

# DELETE - Delete student
@app.delete("/students/{sid}")
def delete_student(sid: int):
    if sid not in students:
        raise HTTPException(404, "Student not found")
    del students[sid]
    return {"message": "Student deleted"}
