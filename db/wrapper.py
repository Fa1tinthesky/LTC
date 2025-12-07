from db import postgres


def wrapper(query: str):
    conn = postgres.get_connection()
    cur = conn.cursor()
    cur.execute(query)
    answ = None
    try:
        answ = cur.fetchall()
    except Exception as e:
        print(f"Error fetching data: {e}")

    conn.commit()
    cur.close()

    return answ
