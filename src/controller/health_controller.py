from fastapi import Depends, APIRouter, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from config.settings import settings
from config.database import get_session

router = APIRouter(
    prefix="/api", tags=["Health Check"]
)

@router.get("/health")
async def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "healthy", "debug": settings.DEBUG}
    )

@router.get("/db-health")
async def db_health_check(db_session=Depends(get_session)):
    try:
        result = await db_session.execute(text('SELECT 1'))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"status": "database healthy"}
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "database unhealthy", "error": str(e)}
        )
