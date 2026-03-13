from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.schemas import ChatResponse
from app.services.ai_service import process_chat

router = APIRouter(prefix="/api/chatbot", tags=["chatbot"])


@router.post("/chat", response_model=ChatResponse)
async def chat(
    message: Optional[str] = Form(None),
    image: Optional[UploadFile] = File(None),
    session_id: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Chatbot endpoint: nhận triệu chứng (text) và/hoặc ảnh cây thuốc.
    Trả về danh sách cây thuốc nam phù hợp cùng thông tin phân bố.
    """
    image_bytes = None
    if image:
        image_bytes = await image.read()

    result = process_chat(
        message=message,
        image_bytes=image_bytes,
        db=db
    )

    return ChatResponse(
        reply=result["reply"],
        recommended_plants=result["recommended_plants"],
        session_id=result["session_id"],
    )
