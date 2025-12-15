import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai

from db import postgres

router = APIRouter()

load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_GEMINI_API_KEY"))


def get_recommendations(reports: list) -> str:
    reports_text = "\n".join(
        [
            f"- Категория: {r['category']}, Оценка: {r['stars']}/5, Описание: {r['details']}"
            for r in reports
        ]
    )

    prompt = f"""Ты — аналитик мобильного оператора. Проанализируй последние жалобы клиентов и дай конкретные рекомендации по оптимизации работы компании.

    Жалобы клиентов:
    {reports_text}

    Задача:
    1. Определи основные проблемы клиентов
    2. Предложи конкретные действия для решения каждой проблемы
    3. Приоритизируй рекомендации по важности
    4. Укажи какие отделы должны заняться решением

    Формат ответа:
    ## Анализ проблем
    [Краткий обзор основных проблем]

    ## Рекомендации по оптимизации
    [Конкретные действия с указанием приоритета и ответственного отдела, отвечай как чат бот]

    ## Ожидаемый эффект
    [Какие улучшения принесут эти действия]"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
    )
    return response.text


@router.get("/recommend")
async def get_optimization_recommendations():
    conn = postgres.get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            """SELECT category, details, stars 
               FROM reports 
               ORDER BY report_date DESC 
               LIMIT 20"""
        )
        results = cur.fetchall()

        if not results:
            return {"recommendations": "Нет жалоб для анализа"}

        reports = [
            {"category": row[0], "details": row[1], "stars": row[2]} for row in results
        ]

        recommendations = get_recommendations(reports)

        return {"recommendations": recommendations, "analyzed_reports_count": len(reports)}

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail="Не удалось получить рекомендации"
        )
    finally:
        cur.close()
