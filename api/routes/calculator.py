from fastapi import APIRouter
from pydantic import BaseModel

from db.wrapper import wrapper

router = APIRouter()


class CalculatorModel(BaseModel):
    mbs: int
    minutes: int
    sms: int
    min_sum: int
    max_sum: int


@router.post("/calculator")
async def calculator(data: CalculatorModel):
    tarif_data = wrapper("SELECT * FROM tarifs")
    """
    tarif TEXT PRIMARY KEY, 0
    tar_name TEXT NOT NULL, 1
    tar_price NUMERIC NOT NULL, 2
    tar_minutes INTEGER NOT NULL, 3
    tar_sms INTEGER NOT NULL, 4
    tar_megabytes BIGINT NOT NULL, 5
    """

    tarifs_sorted = []

    for tarif in tarif_data:
        value = 0
        mbs = tarif[5]
        sms = tarif[4]

        value += abs(data.mbs - mbs) * (0.5 if data.mbs > mbs else 1)

    tarifs_sorted.sort(key=lambda x: x[1])

    return {"answer": tarifs_sorted}
