from fastapi import APIRouter, HTTPException

router = APIRouter()

@router.get('/ping')
async def timeout_ping():
    return {"message": "Pinged succesefuly", "ok": True}
