import inspect
from typing import Annotated


annotated_string = "asdasd"

def test(a: Annotated[str, int]) -> int:
    ...


annotations = inspect.get_annotations(test)
