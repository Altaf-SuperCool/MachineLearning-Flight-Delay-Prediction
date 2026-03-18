from fastapi import Request
from fastapi.responses import JSONResponse
from .logger import logger

async def error_middleware(request: Request, call_next):
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Unhandled error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)},
        )
