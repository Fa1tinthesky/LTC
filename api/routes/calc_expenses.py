from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db.wrapper import wrapper

router = APIRouter()

class UserData(BaseModel):
    phone: str

@router.post("/calc_expenses")
async def calc_top_expenses(data: UserData):
    timestamps = []
    data = wrapper("SELECT * FROM your_table_name WHERE phone_number IS NOT NULL AND phone_number != '';")
    # by phone get data

    return { "sorted_by_time": data }
    """
            phone TEXT,
            megabytes_used BIGINT NOT NULL,
            minutes_used INTEGER NOT NULL,
            sms_used INTEGER NOT NULL,
            tarif TEXT NOT NULL,
            date TIMESTAMP NOT NULL
    """
