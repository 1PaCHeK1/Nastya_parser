from typing import Any
from typing_extensions import Self
from pydantic import BaseModel, BaseConfig


class BaseDto(BaseModel):
    class Config(BaseConfig):
        orm_mode = True

    @classmethod
    def from_orm_list(cls, objs: list[Any]) -> list[Self]:
        return [cls.from_orm(obj) for obj in objs]

    @classmethod
    def parse_obj_list(cls, objs: list[Any]) -> list[Self]:
        return [cls.parse_obj(obj) for obj in objs]
