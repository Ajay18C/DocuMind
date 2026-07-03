from collections.abc import Sequence

from .context import Context
from .stage import Stage


class Pipeline:
    def __init__(self, stages: Sequence[Stage]):
        self.stages = stages

    async def run(self, ctx: Context) -> Context:
        for stage in self.stages:
            ctx = await stage.process(ctx)
        return ctx
