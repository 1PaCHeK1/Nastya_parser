from typing import Annotated

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column

int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

str_128 = Annotated[str, mapped_column(String(128))]
text = Annotated[str, mapped_column(Text)]
