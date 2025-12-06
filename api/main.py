from fastapi import FastAPI

from api.routes import calculator, reports, users

app = FastAPI(
    title="LTC API",
    version="1.0.0",
)

app.include_router(reports.router, prefix="", tags=["reports"])
app.include_router(calc_expenses.router, prefix="", tags=["calc_expenses"])
app.include_router(calculator.router, prefix="", tags=["calculator"])
app.include_router(users.router, prefix="", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to the LTC API"}


