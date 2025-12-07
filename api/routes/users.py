from fastapi import APIRouter, HTTPException

from db import postgres

router = APIRouter()


@router.post("/user_log_in")
async def user_log_in(phone: str):
    conn = postgres.get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT phone FROM users WHERE phone = %s", (phone,))
        result = cur.fetchone()
        if result:
            return {"message": "User logged in successfully", "ok": True}
        else:
            raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Failed to log in user")
    finally:
        cur.close()


@router.post("/admin_log_in")
async def admin_log_in(password: str):
    ADMIN_PASSWORD = "admin"  # Example admin password
    if password == ADMIN_PASSWORD:
        return {"message": "Admin logged in successfully", "ok": True}
    else:
        raise HTTPException(status_code=401, detail="Invalid admin password")
