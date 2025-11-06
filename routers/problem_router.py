from fastapi import APIRouter, Form, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.problem import Problem
import shutil, os

router = APIRouter()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ✅ CREATE Problem
@router.post("/")
async def create_problem(
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    client_id: str | None = Form(None),
    business_vertical: str = Form(...),
    referring_source: str = Form(...),
    problem_category: str = Form(...),
    priority_level: str = Form(...),
    problem_summary: str | None = Form(None),
    audio_file: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):

    filename = None
    if audio_file:
        filename = f"{full_name.replace(' ', '_')}_{audio_file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

    problem = Problem(
        full_name=full_name,
        phone=phone,
        email=email,
        client_id=client_id,
        business_vertical=business_vertical,
        referring_source=referring_source,
        problem_category=problem_category,
        priority_level=priority_level,
        problem_summary=problem_summary,
        audio_filename=filename
    )

    db.add(problem)
    db.commit()
    db.refresh(problem)

    return {"message": "✅ Problem submitted successfully!", "problem_id": problem.id}


# ✅ GET ALL Problems
@router.get("/")
def get_all_problems(db: Session = Depends(get_db)):
    problems = db.query(Problem).all()
    return problems


# ✅ GET Problem by ID
@router.get("/{problem_id}")
def get_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem


# ✅ UPDATE Problem by ID
@router.put("/{problem_id}")
async def update_problem(
    problem_id: int,
    full_name: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    client_id: str | None = Form(None),
    business_vertical: str = Form(...),
    referring_source: str = Form(...),
    problem_category: str = Form(...),
    priority_level: str = Form(...),
    problem_summary: str | None = Form(None),
    audio_file: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    # Update fields
    problem.full_name = full_name
    problem.phone = phone
    problem.email = email
    problem.client_id = client_id
    problem.business_vertical = business_vertical
    problem.referring_source = referring_source
    problem.problem_category = problem_category
    problem.priority_level = priority_level
    problem.problem_summary = problem_summary

    if audio_file:
        filename = f"{full_name.replace(' ', '_')}_{audio_file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(audio_file.file, buffer)

        problem.audio_filename = filename

    db.commit()
    db.refresh(problem)

    return {"message": "✅ Problem updated successfully!"}


# ✅ DELETE Problem by ID
@router.delete("/{problem_id}")
def delete_problem(problem_id: int, db: Session = Depends(get_db)):
    problem = db.query(Problem).filter(Problem.id == problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    db.delete(problem)
    db.commit()

    return {"message": "🗑️ Problem deleted successfully!"}
