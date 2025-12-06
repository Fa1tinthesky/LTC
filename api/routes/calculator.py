from fastapi import APIRouter
from pydantic import BaseModel

from db.wrapper import wrapper

router = APIRouter()


class ReportCategory(BaseModel):
    phone: str
    details: str
    stars: int


@router.post("/calculator")
async def calculator(data: ReportCategory):
    return {"answer": wrapper("SELECT * FROM reports")}
