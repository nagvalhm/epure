
from typing import Any, Callable
from ..node.node import *

class ECommand:
    script = "it's script for something"

    def __init__(self, foo:Callable[[Node],Any]) -> None:
        return super().__init__()

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass
    
    def __str__(self) -> str:
        return self.script