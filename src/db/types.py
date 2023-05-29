from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Text

from typing import Annotated


int_pk = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]

str_128 = Annotated[str, mapped_column(String(128))]
text = Annotated[str, mapped_column(Text)]
