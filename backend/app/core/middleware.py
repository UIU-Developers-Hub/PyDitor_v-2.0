# File: app/core/middleware.py
from fastapi import FastAPI, Request, Response
from typing import Awaitable, Callable
from datetime import datetime
from starlette.middleware.base import BaseHTTPMiddleware
import logging

logger = logging.getLogger(__name__)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, 
        request: Request, 
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = datetime.now()
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds()
        response.headers["X-Process-Time"] = str(process_time)
        return response

class DatabaseMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        app: FastAPI,
        db_session_maker: Callable
    ):
        super().__init__(app)
        self.db_session_maker = db_session_maker

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        async with self.db_session_maker() as session:
            request.state.db = session
            try:
                response = await call_next(request)
                await session.commit()
                return response
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()