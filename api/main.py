from fastapi import FastAPI

from api.routes import reports

app = FastAPI()

app.include_router(reports.router, prefix="", tags=["reports"])


@app.get("/")
async def root():
    return {"message": "Welcome to the LTC API"}
