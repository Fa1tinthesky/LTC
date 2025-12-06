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
        tr_mbs = tarif[5]
        tr_sms = tarif[4]
        tr_minutes = tarif[3]
        tr_price = tarif[2]
        tarif_name = tarif[1]

        w_mbs = 1
        w_min = 5
        w_sms = 10
        w_price = 2

        w_out = 1000

        value += abs(data.mbs - tr_mbs) * (1 if data.mbs <= tr_mbs else w_out) * w_mbs
        value += (
            abs(data.minutes - tr_minutes)
            * (1 if data.minutes <= tr_minutes else w_out)
            * w_min
        )
        value += abs(data.sms - tr_sms) * (1 if data.sms <= tr_sms else w_out) * w_sms
        value += (
            abs(data.min_sum - tr_price)
            * (1 if data.min_sum <= tr_price <= data.max_sum else w_out)
            * w_price
        )

        tarifs_sorted.append(
            {
                "name": tarif_name,
                "value": value,
                "mbs": tr_mbs,
                "sms": tr_sms,
                "minutes": tr_minutes,
                "price": tr_price,
            }
        )

    tarifs_sorted.sort(key=lambda x: x["value"])

    return {"data": tarifs_sorted}
