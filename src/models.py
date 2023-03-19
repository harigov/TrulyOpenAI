from datetime import datetime
import enum
from marshmallow import Schema, fields
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, func
from uuid import uuid4

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ChatSessionModel(Base):
    __tablename__ = 'chat_sessions'

    id = Column(String, primary_key=True, default=lambda: uuid4().hex)
    name = Column(String, nullable=False)
    create_timestamp = Column(DateTime, server_default=func.now())
    update_timestamp = Column(DateTime, server_default=func.now(), onupdate=func.now())
    is_archived = Column(Boolean, default=False)

    def __repr__(self):
        return f'Session({self.id}, {self.status})'

class MessageRole(enum.Enum):
    USER = 'user'
    ASSISTANT = 'assistant'

class ChatMessageModel(Base):
    __tablename__ = 'messages'

    id = Column(String, primary_key=True, default=lambda: uuid4().hex)
    chat_session_id = Column(String, ForeignKey('chat_sessions.id'))
    timestamp = Column(DateTime, server_default=func.now())
    role = Column(Enum(MessageRole))
    content = Column(String)

    def __repr__(self):
        return f'Message({self.id}, {self.role}, {self.content})'

class ChatSessionSchema(Schema):
    id = fields.String()
    name = fields.String()
    create_timestamp = fields.DateTime()
    update_timestamp = fields.DateTime()
    is_archived = fields.Boolean()

class ChatMessageSchema(Schema):
    id = fields.String()
    chat_session_id = fields.String()
    timestamp = fields.DateTime()
    role = fields.Str()
    content = fields.String()
