from typing import Any, Self

from pydantic import BaseModel, ConfigDict


class BaseDto(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm_list(cls, objs: list[Any]) -> list[Self]:
        return [cls.model_validate(obj) for obj in objs]

    @classmethod
    def parse_obj_list(cls, objs: list[Any]) -> list[Self]:
        return [cls.model_validate(obj) for obj in objs]
