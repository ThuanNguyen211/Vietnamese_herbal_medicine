from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import MapResponse
from app.services.ai_service import process_map

router = APIRouter(prefix="/api/map", tags=["map"])
legacy_router = APIRouter(prefix="/api/chatbot", tags=["chatbot-legacy"])


@router.post("/chat", response_model=MapResponse)
@legacy_router.post("/chat", response_model=MapResponse)
async def map_chat(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Map endpoint: nhận triệu chứng (text) và/hoặc ảnh cây thuốc.
    Trả về danh sách cây thuốc nam phù hợp cùng thông tin phân bố.
    """
    image_bytes = None
    if image:
        image_bytes = await image.read()

    result = process_map(
        message=message,
        image_bytes=image_bytes,
        db=db
    )

    return MapResponse(
        reply=result["reply"],
        recommended_plants=result["recommended_plants"],
        session_id=result["session_id"],
    )
