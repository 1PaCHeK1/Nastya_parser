import enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Text, Boolean, DateTime, Enum
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


class FavoriteWord(BaseModel):
    __tablename__ = "favoriteword"

    user_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    word_id = Column(ForeignKey("words.id", ondelete="CASCADE"))

    user = relationship("User")


class Post(BaseModel):
    __tablename__ = "post"

    title = Column(String)
    body = Column(Text)
    author_id = Column(ForeignKey("users.id", ondelete="CASCADE"))
    is_publish = Column(Boolean)
    publish_date = Column(DateTime)


class Tag(BaseModel):
    __tablename__ = "tag"

    name = Column(String)
    rating = Column(Integer)


class PostTags(BaseModel):
    __tablename__ = "posttags"

    tag_id = Column(ForeignKey("tag.id", ondelete="CASCADE"))
    post_id = Column(ForeignKey("post.id", ondelete="CASCADE"))


class RightAnswerEnum(int, enum.Enum):
    answer_one = 1
    answer_two = 2
    answer_three = 3


class QuizQuestion(BaseModel):
    __tablename__ = "quizquestions"

    question = Column(String)
    theme_id = Column(ForeignKey('quiztheme.id', ondelete="CASCADE"))
    answer_one = Column(String)
    answer_two = Column(String)
    answer_three = Column(String)
    right_answer = Column(Enum(RightAnswerEnum, default=1, native_enum=False))


class QuizTheme(BaseModel):
    __tablename__ = "quiztheme"

    name = Column(String)

# alembic revision --autogenerate
# alembic upgrade head
