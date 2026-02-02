from pydantic import BaseModel, Field, field_validator, ConfigDict  # Добавьте ConfigDict
from datetime import datetime
from typing import List

class ChatBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    
    @field_validator('title')
    @classmethod
    def trim_title(cls, v: str) -> str:
        return v.strip()

class MessageBase(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)
    
    @field_validator('text')
    @classmethod
    def trim_text(cls, v: str) -> str:
        return v.strip()

class ChatCreate(ChatBase):
    pass

class MessageCreate(MessageBase):
    pass

class MessageResponse(MessageBase):
    id: int
    chat_id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ChatResponse(ChatBase):
    id: int
    created_at: datetime
    messages: List[MessageResponse] = []
    
    model_config = ConfigDict(from_attributes=True)

class ChatWithMessages(BaseModel):
    id: int
    title: str
    created_at: datetime
    messages: List[MessageResponse]
    
    model_config = ConfigDict(from_attributes=True)