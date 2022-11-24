from datetime import date
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from core.database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)


class Language(BaseModel):
    __tablename__ = "languages"

    name = Column(String)
    order = Column(Integer, default=1)


class Translate(BaseModel):
    __tablename__ = "translates"

    from_language_id = Column(ForeignKey("languages.id", ondelete="CASCADE"))
    to_language_id = Column(ForeignKey("languages.id", ondelete="CASCADE"))


class Word(BaseModel):
    __tablename__ = "words"

    text = Column(String)
    translate = Column(String)


class FavoriteWord(BaseModel):
    __tablename__ = "favoriteword"
    
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    word_id = Column(ForeignKey("words.id", ondelete="CASCADE"))
    translate_id = Column(ForeignKey("translates.id", ondelete="CASCADE"))

    user = relationship("User")
