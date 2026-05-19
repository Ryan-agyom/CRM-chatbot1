from fastapi import APIRouter
from app.models.schemas import ChatRequest
from app.services.chatbot_service import process_chat

router = APIRouter(prefix="/api")

@router.post("/chat")
async def chat(request:ChatRequest):
    return await process_chat(
        request.message,
        request.sessionId
    )
