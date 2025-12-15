from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from db.wrapper import wrapper

router = APIRouter()


def filter_by_phone_number(phone_number, data):
    if phone_number == "":
        return data

    return [x for x in data if x[0] == phone_number]


def maximum_traffic_used_month(data):
    expenses = {}
    megabytes_used = 0
    minutes_used = 0
    sms_used = 0

    for x in data:
        if int(x[0]) > int(megabytes_used):
            megabytes_used = x[1]
        if int(x[1]) > int(minutes_used):
            minutes_used = x[2]
        if int(x[2]) > int(sms_used):
            sms_used = x[3]

    expenses["megabytes_used"] = megabytes_used
    expenses["minutes_used"] = minutes_used
    expenses["sms_used"] = sms_used

    print(expenses)
    expenses_sorted = dict(sorted(expenses.items(), key=lambda x: x[1], reverse=True))
    return expenses_sorted


class UserData(BaseModel):
    phone: str


@router.post("/calc_expenses")
async def calc_top_expenses(data: UserData):
    phone_number = data.phone
    print(data.phone)

    # payments_monthly_expenses table (fixed name & types)
    data = wrapper(f"SELECT * FROM payments_monthly_expenses WHERE phone IS NOT NULL")
    tarif_data = wrapper("SELECT * FROM tarifs")

    data = filter_by_phone_number(phone_number, data)
    data.sort(key=lambda x: x[-1])

    expenses_sorted = []

    return {"sorted_by_time": data, "sorted_by_usage": maximum_traffic_used_month(data)}
    """
            phone TEXT,
            megabytes_used BIGINT NOT NULL,
            minutes_used INTEGER NOT NULL,
            sms_used INTEGER NOT NULL,
            tarif TEXT NOT NULL,
            date TIMESTAMP NOT NULL
    """

    # tarifs table (use numeric/integer types)
    """tarifs(
        tarif TEXT PRIMARY KEY,
        tar_name TEXT NOT NULL,
        tar_price NUMERIC NOT NULL,
        tar_minutes INTEGER NOT NULL,
        tar_sms INTEGER NOT NULL,
        tar_megabytes BIGINT NOT NULL
    )"""
