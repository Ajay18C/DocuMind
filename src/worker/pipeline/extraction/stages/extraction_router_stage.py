from worker.pipeline.stage import Stage

from ..extraction_context import ExtractionContext, PdfType


class UnsupportedPdfTypeError(Exception):
    def __init__(self, pdf_type: PdfType):
        super().__init__(f"No extraction stage registered for pdf_type: {pdf_type}")
        self.pdf_type = pdf_type


class ExtractionRouterStage:
    def __init__(self, routes: dict[PdfType, Stage]):
        self.routes = routes

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        stage = self.routes.get(ctx.pdf_type)
        if stage is None:
            raise UnsupportedPdfTypeError(ctx.pdf_type)
        return await stage.process(ctx)
