from core.dto.base import BaseDto


class WordCreateSchema(BaseDto):
    word: str
    translate_words: list[str]


class QuestionType(BaseDto):
    question: str
    answer_one: str
    answer_two: str
    answer_three: str
    right_answer: str
