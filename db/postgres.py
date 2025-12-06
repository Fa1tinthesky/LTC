import psycopg2


def ConnectToPostgres():
    try:
        conn = psycopg2.connect(
            user="prime",
            password="sPELypo3KLyvEY2HHtrOgYwI3mrYFgF1",
            host="dpg-d4q1f7adbo4c73bjpogg-a.singapore-postgres.render.com",
            dbname="ftc_c4oc",
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
        return None


def create_tables(conn):
    cur = conn.cursor()
    # users table
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        phone TEXT PRIMARY KEY,
        fullname TEXT NOT NULL,
        tarif TEXT NOT NULL
    )""")
    # tarifs table (use numeric/integer types)
    cur.execute("""CREATE TABLE IF NOT EXISTS tarifs(
        tarif TEXT PRIMARY KEY,
        tar_name TEXT NOT NULL,
        tar_price NUMERIC NOT NULL,
        tar_minutes INTEGER NOT NULL,
        tar_sms INTEGER NOT NULL,
        tar_megabytes BIGINT NOT NULL
    )""")
    # payments_monthly_expenses table (fixed name & types)
    cur.execute("""CREATE TABLE IF NOT EXISTS payments_monthly_expenses(
        phone TEXT,
        megabytes_used BIGINT NOT NULL,
        minutes_used INTEGER NOT NULL,
        sms_used INTEGER NOT NULL,
        tarif TEXT NOT NULL,
        date TIMESTAMP NOT NULL
    )""")
    # reports table
    cur.execute("""CREATE TABLE IF NOT EXISTS reports(
        report_id SERIAL PRIMARY KEY,
        phone TEXT NOT NULL,
        report_date TIMESTAMP NOT NULL,
        category TEXT NOT NULL,
        details TEXT NOT NULL,
        stars INT NOT NULL
    )""")
    conn.commit()
    cur.close()


if __name__ == "__main__":
    conn = ConnectToPostgres()
    if conn:
        create_tables(conn)
        conn.close()
