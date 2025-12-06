from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class ReportCategory(BaseModel):
    phone: str
    details: str
    stars: int

@router.get("/report_write")
async def write_report(data: ReportCategory):
    return {}