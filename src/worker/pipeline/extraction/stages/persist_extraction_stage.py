from model.extraction_model import ExtractionStatus

from ..extraction_context import ExtractionContext


class PersistExtractionStage:
    def __init__(self, extraction_repository):
        self.extraction_repository = extraction_repository

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        extraction = await self.extraction_repository.get(ctx.extraction_id)
        if extraction is None:
            raise LookupError(f"Extraction {ctx.extraction_id} not found")
        extraction.extraction_result = {"extracted_text": ctx.extracted_text}
        extraction.status = ExtractionStatus.COMPLETED
        await self.extraction_repository.update(extraction)
        return ctx
