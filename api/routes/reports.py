from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ReportCategory(BaseModel):
    phone: str
    details: str
    stars: int


@router.post("/report_write")
async def write_report(data: ReportCategory):
    return {}
