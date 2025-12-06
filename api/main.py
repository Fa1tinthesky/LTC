from fastapi import FastAPI

from api.routes import calc_expenses
from api.routes import reports

app = FastAPI()

app.include_router(reports.router, prefix="", tags=["reports"])
app.include_router(calc_expenses.router, prefix="", tags=["calc_expenses"])


@app.get("/")
async def root():
    return {"message": "Welcome to the LTC API"}


