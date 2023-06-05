from collections.abc import Sequence
from typing import Any
from typing_extensions import Self
from pydantic import BaseModel, BaseConfig


class BaseSchema(BaseModel):
    class Config(BaseConfig):
        orm_mode = True

    @classmethod
    def from_orm_list(cls, objs: Sequence[Any]) -> list[Self]:
        return [cls.from_orm(item) for item in objs]
