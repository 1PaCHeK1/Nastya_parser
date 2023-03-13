from enum import Enum
import json
from dataclasses import dataclass, asdict


class CallbakDataEnum(str, Enum):
    favorites = "favorites"
    favorite_word = "favorite-word"
    save_favorite = "save-favorite"
    remove_favorite = "remove-favorite"

    registration = "registration"


@dataclass
class CallbackData:
    enum: CallbakDataEnum
    data: str|None = None

    def to_json(self) -> str:
        return json.dumps(asdict(self))

    @classmethod
    def from_json(cls, s: str) -> "CallbackData":
        obj = json.loads(s)
        return CallbackData(enum=obj["enum"], data=obj["data"])
