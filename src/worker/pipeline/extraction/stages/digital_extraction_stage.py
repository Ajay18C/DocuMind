from ..extraction_context import ExtractionContext


class DigitalExtractionStage:
    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        ctx.extracted_text = "\n".join(page.text for page in ctx.pages)
        return ctx
