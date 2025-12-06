# ...existing code...
import psycopg2


def ConnectToPostgres():
    try:
        conn = psycopg2.connect(
            dbname="LTC",
            user="postgres",
            password="noskash228",
            host="localhost",
            port="5432"
        )
        conn.autocommit = False
        return conn
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)
        return None


def create_tables(conn):
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        phone TEXT PRIMARY KEY,
        fullname TEXT NOT NULL,
        tarif_id TEXT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS tarifs(
        tarif_id TEXT PRIMARY KEY,
        tar_name TEXT NOT NULL,
        tar_price NUMERIC NOT NULL,
        tar_minutes INTEGER NOT NULL,
        tar_sms INTEGER NOT NULL,
        tar_megabytes BIGINT NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS payments_monthly_expenses(
        phone TEXT,
        megabytes_used BIGINT NOT NULL,
        minutes_used INTEGER NOT NULL,
        sms_used INTEGER NOT NULL,
        tarif_id TEXT NOT NULL,
        date TIMESTAMP NOT NULL
    )""")
    cur.execute("""CREATE TABLE IF NOT EXISTS reports(
        report_id SERIAL PRIMARY KEY,
        phone TEXT NOT NULL,
        report_date TIMESTAMP NOT NULL,
        category_id INTEGER NOT NULL,
        details TEXT NOT NULL,
        stars UINT NOT NULL
    )""")
    conn.commit()
    cur.close()


if __name__ == "__main__":
    conn = ConnectToPostgres()
    if conn:
        create_tables(conn)
        conn.close()