from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import desc

from app import models, schemas
from app.config import settings

class ChatCRUD:
    @staticmethod
    def get_chat(db: Session, chat_id: int) -> Optional[models.Chat]:
        return db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    
    @staticmethod
    def get_chats(db: Session, skip: int = 0, limit: int = 100) -> List[models.Chat]:
        return db.query(models.Chat).offset(skip).limit(limit).all()
    
    @staticmethod
    def create_chat(db: Session, chat: schemas.ChatCreate) -> models.Chat:
        db_chat = models.Chat(title=chat.title)
        db.add(db_chat)
        db.commit()
        db.refresh(db_chat)
        return db_chat
    
    @staticmethod
    def delete_chat(db: Session, chat_id: int) -> bool:
        db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        if db_chat:
            db.delete(db_chat)
            db.commit()
            return True
        return False

class MessageCRUD:
    @staticmethod
    def get_messages_by_chat(
        db: Session, 
        chat_id: int, 
        limit: int = settings.DEFAULT_MESSAGE_LIMIT,
        offset: int = 0
    ) -> List[models.Message]:
        return db.query(models.Message)\
            .filter(models.Message.chat_id == chat_id)\
            .order_by(desc(models.Message.created_at))\
            .offset(offset)\
            .limit(limit)\
            .all()
    
    @staticmethod
    def create_message(
        db: Session, 
        chat_id: int, 
        message: schemas.MessageCreate
    ) -> Optional[models.Message]:

        chat = ChatCRUD.get_chat(db, chat_id)
        if not chat:
            return None
        
        db_message = models.Message(
            chat_id=chat_id,
            text=message.text
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message
    
    @staticmethod
    def get_chat_with_messages(
        db: Session,
        chat_id: int,
        limit: int = settings.DEFAULT_MESSAGE_LIMIT
    ) -> Optional[models.Chat]:
        chat = ChatCRUD.get_chat(db, chat_id)
        if chat:

            messages = MessageCRUD.get_messages_by_chat(db, chat_id, limit)
            chat.messages = messages
        return chat