from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date

from core.database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel):
    __tablename__ = "users"
    
    username = Column(String(length=128))
    email = Column(String(length=128), unique=True)
    tg_id = Column(Integer, unique=True)
    create_at = Column(Date, default=date.today)

    favorite_words = relationship("FavoriteWord")
