from collections.abc import Sequence
from typing import Any
from typing_extensions import Self
from pydantic import BaseModel, ConfigDict


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate_list(cls, objs: Sequence[Any]) -> list[Self]:
        return [cls.model_validate(item) for item in objs]
