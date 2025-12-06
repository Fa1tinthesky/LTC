from datetime import datetime

import psycopg2
from fastapi import APIRouter, HTTPException
from google import genai
from pydantic import BaseModel

from db import postgres

router = APIRouter()


class ReportCategory(BaseModel):
    phone: str
    details: str
    stars: int


class Category(BaseModel):
    category: str


client = genai.Client(api_key="AIzaSyDyDtuIZ6zZ9JVemh8pf1gTb-H1gp8go38")


def classify(content: str):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""Classify this review into one of the suggested categories. Return only one word in your answer that indicates the name of the category.
            Review:{content}
            Categories: connection, speed, support, price, coverage.""",
    )
    return response.text


@router.post("/report_write")
async def write_report(data: ReportCategory):
    category = classify(data.details)
    now = datetime.now()
    conn = postgres.ConnectToPostgres()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO reports (phone, report_date, category, details, stars) VALUES (%s, %s, %s, %s, %s)",
            (data.phone, now, category, data.details, data.stars),
        )
        conn.commit()

    except Exception as e:
        print(e)
        conn.rollback()
        raise HTTPException(status_code=500, detail="Failed to write report")
    finally:
        cur.close()
        conn.close()


@router.get("/view_categories")
async def view_categories():
    conn = postgres.ConnectToPostgres()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT category, COUNT(*) as count FROM reports GROUP BY category"""
        )
        results = cur.fetchall()
        categories = [{"category": row[0], "count": row[1]} for row in results]
        return {"categories": categories}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to retrieve categories")
    finally:
        cur.close()
        conn.close()


@router.post("/view_by_category")
async def view_by_category(data: Category):
    conn = postgres.ConnectToPostgres()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT phone, report_date, details, stars FROM reports WHERE category = %s""",
            (data.category,),
        )
        results = cur.fetchall()
        reports = [
            {"phone": row[0], "report_date": row[1], "details": row[2], "stars": row[3]}
            for row in results
        ]
        return {"reports": reports}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Failed to retrieve reports by category"
        )
    finally:
        cur.close()
        conn.close()
