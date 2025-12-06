from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class UserData(BaseModel):
    phone: str

@router.post("/calc_expenses")
async def calc_top_expenses(data: UserData):
    return { "hello": "world",
             "data": data.phone }

