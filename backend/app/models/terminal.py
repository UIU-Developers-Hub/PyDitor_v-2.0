# 2. Terminal Model (backend/app/models/terminal.py)
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from app.core.database import Base

class TerminalSession(Base):
    __tablename__ = "terminal_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    terminal_id = Column(String, unique=True)
    history = Column(Text, default="")
    current_directory = Column(String, default="~/")
    
    class Config:
        orm_mode = True