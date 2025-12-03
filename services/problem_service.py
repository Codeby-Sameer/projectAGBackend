import os
import shutil
from uuid import uuid4
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.problem import ProblemReport
from schemas.problem import ProblemReportCreate
from core.config import settings
from fastapi import UploadFile, HTTPException


async def save_audio_file(upload_file: UploadFile) -> str:
    """
    Save uploaded audio file to uploads directory and return filename.
    """
    if upload_file is None:
        return None

    filename = upload_file.filename
    ext = os.path.splitext(filename)[1].lower()
    allowed_ext = {".mp3", ".wav", ".m4a", ".ogg", ".aac"}
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail="Unsupported audio format.")

    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    unique_name = f"{uuid4().hex}{ext}"
    dest_path = os.path.join(settings.UPLOAD_DIR, unique_name)

    # use async stream to write? UploadFile.file is a SpooledTemporaryFile - use shutil
    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return unique_name


async def create_problem(db: AsyncSession, payload: ProblemReportCreate, audio: Optional[UploadFile] = None) -> ProblemReport:
    audio_filename = None
    if audio:
        audio_filename = await save_audio_file(audio)
    new = ProblemReport(
        full_name=payload.clientName,
        primary_phone=payload.contactPhone,
        email=payload.contactEmail,
        existing_client_id=payload.existingClientId,
        business_vertical=payload.businessVertical,
        referring_source=payload.referringSource,
        problem_category=payload.problemCategory,
        priority_level=payload.urgencyLevel,
        audio_filename=audio_filename,
        written_summary=payload.problemSummary,
      )
    db.add(new)
    await db.commit()
    await db.refresh(new)
    return new


async def get_problem(db: AsyncSession, problem_id: int) -> ProblemReport:
    q = await db.execute(select(ProblemReport).where(ProblemReport.id == problem_id))
    result = q.scalars().first()
    return result


async def list_problems(db: AsyncSession, limit: int = 50, offset: int = 0):
    q = await db.execute(select(ProblemReport).order_by(ProblemReport.created_at.desc()).limit(limit).offset(offset))
    return q.scalars().all()
