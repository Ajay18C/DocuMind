from typing import Protocol
from .context import Context


class Stage(Protocol):
    async def process(self, ctx: Context) -> Context: ...
