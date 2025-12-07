import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import calculator, reports, users


async def lifespan(app: FastAPI):
    load_dotenv()
    yield
    # Add any shutdown tasks here


app = FastAPI(title="LTC API", version="1.0.0", lifespan=lifespan)

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router, prefix="", tags=["reports"])
app.include_router(calculator.router, prefix="", tags=["calculator"])
app.include_router(users.router, prefix="", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "Welcome to the LTC API"}
