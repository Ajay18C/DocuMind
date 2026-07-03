from worker.pipeline.pipeline import Pipeline

from .digital_detection_stage import DigitalDetectionStage
from .digital_extraction_stage import DigitalExtractionStage
from .extraction_router_stage import ExtractionRouterStage
from .persist_extraction_stage import PersistExtractionStage


def build_extraction_pipeline(extraction_repository) -> Pipeline:
    return Pipeline(
        [
            DigitalDetectionStage(),
            ExtractionRouterStage({"Digital": DigitalExtractionStage()}),
            PersistExtractionStage(extraction_repository),
        ]
    )
