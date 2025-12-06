import psycopg2


def wrapper(query: str):
    conn = psycopg2.connect(
        user="prime",
        password="sPELypo3KLyvEY2HHtrOgYwI3mrYFgF1",
        host="dpg-d4q1f7adbo4c73bjpogg-a.singapore-postgres.render.com",
        dbname="ftc_c4oc",
    )
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
