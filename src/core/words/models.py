from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey
from core.database import Base


class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, autoincrement=True)


class Language(BaseModel):
    __tablename__ = "languages"

    name = Column(String)
    order = Column(Integer, default=1)



class Word(BaseModel):
    __tablename__ = "words"

    text = Column(String)
    language_id = Column(ForeignKey("languages.id", ondelete="CASCADE"))


class WordTranslate(Base):
    __tablename__ = "wordtranslates"

    word_from_id: int = Column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)
    word_to_id: int = Column(ForeignKey("words.id", ondelete="CASCADE"), primary_key=True)


class Translate(BaseModel):
    __tablename__ = "translates"

    from_language_id = Column(ForeignKey("languages.id", ondelete="CASCADE"))
    to_language_id = Column(ForeignKey("languages.id", ondelete="CASCADE"))

# Привет -> Hello
# Hi -> Привет
# Привет -> Hello, Hi

class FavoriteWord(BaseModel):
    __tablename__ = "favoriteword"
    
    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    word_id = Column(ForeignKey("words.id", ondelete="CASCADE"))

    user = relationship("User")
