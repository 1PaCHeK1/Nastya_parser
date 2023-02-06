from pydantic import BaseModel


class WordCreateSchema(BaseModel):
    word: str
    translate_words: list[str]


