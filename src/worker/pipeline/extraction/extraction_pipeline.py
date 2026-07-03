from worker.pipeline.pipeline import Pipeline

from .extraction_context import PdfType
from .ocr.engine import get_ocr_engine
from .pdf.parser import get_pdf_parser
from .stages.digital_detection_stage import DigitalDetectionStage
from .stages.digital_extraction_stage import DigitalExtractionStage
from .stages.extraction_router_stage import ExtractionRouterStage
from .stages.persist_extraction_stage import PersistExtractionStage
from .stages.scanned_extraction_stage import ScannedExtractionStage


def build_extraction_pipeline(extraction_repository) -> Pipeline:
    pdf_parser = get_pdf_parser()
    return Pipeline(
        [
            DigitalDetectionStage(pdf_parser),
            ExtractionRouterStage(
                {
                    PdfType.DIGITAL: DigitalExtractionStage(),
                    PdfType.SCANNED: ScannedExtractionStage(pdf_parser, get_ocr_engine),
                }
            ),
            PersistExtractionStage(extraction_repository),
        ]
    )
