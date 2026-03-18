import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from .logger import logger
from .metrics import REQUEST_COUNT, REQUEST_ERRORS, observe_latency

class MonitoringMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        REQUEST_COUNT.inc()
        start = time.time()
        try:
            response = await call_next(request)
            latency = time.time() - start
            observe_latency(start)
            logger.info(
                {
                    "event": "request_completed",
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": response.status_code,
                    "latency_ms": round(latency * 1000, 2),
                }
            )
            return response
        except Exception as ex:
            REQUEST_ERRORS.inc()
            latency = time.time() - start
            logger.error(
                {
                    "event": "request_failed",
                    "path": request.url.path,
                    "method": request.method,
                    "error": str(ex),
                    "latency_ms": round(latency * 1000, 2),
                }
            )
            raise
