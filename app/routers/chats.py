from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
import logging

from app.database import get_db
from app import schemas, crud
from app.config import settings

router = APIRouter(prefix="/chats")
logger = logging.getLogger(__name__)

@router.post("/", response_model=schemas.ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat: schemas.ChatCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat"""
    logger.info(f"Creating chat with title: {chat.title}")
    return crud.ChatCRUD.create_chat(db, chat)

@router.post("/{chat_id}/messages/", response_model=schemas.MessageResponse)
async def create_message(
    chat_id: int,
    message: schemas.MessageCreate,
    db: Session = Depends(get_db)
):
    """Send message to chat"""
    logger.info(f"Creating message in chat {chat_id}")
    db_message = crud.MessageCRUD.create_message(db, chat_id, message)
    if db_message is None:
        logger.warning(f"Chat {chat_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return db_message

@router.get("/{chat_id}", response_model=schemas.ChatWithMessages)
async def get_chat_with_messages(
    chat_id: int,
    limit: int = Query(
        default=settings.DEFAULT_MESSAGE_LIMIT,
        ge=1,
        le=settings.MAX_MESSAGE_LIMIT,
        description=f"Number of messages (1-{settings.MAX_MESSAGE_LIMIT})"
    ),
    db: Session = Depends(get_db)
):
    """Get chat with latest messages"""
    logger.info(f"Getting chat {chat_id} with {limit} messages")
    chat = crud.MessageCRUD.get_chat_with_messages(db, chat_id, limit)
    if not chat:
        logger.warning(f"Chat {chat_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return chat

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    db: Session = Depends(get_db)
):
    """Delete chat with all messages"""
    logger.info(f"Deleting chat {chat_id}")
    if not crud.ChatCRUD.delete_chat(db, chat_id):
        logger.warning(f"Chat {chat_id} not found for deletion")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat not found"
        )
    return None