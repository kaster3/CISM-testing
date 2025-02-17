import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from api import router as api_router
from core import settings
from core.taskiq.broker import broker


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(
        level=logging.INFO,
        format=settings.logging.log_format,
    )
    if not broker.is_worker_process:
        await broker.startup()
    logging.info("Application starts successfully!")
    yield
    if not broker.is_worker_process:
        await broker.shutdown()
    logging.info("Application ends successfully!")


application = FastAPI(
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

application.include_router(
    router=api_router,
)


def main() -> None:
    uvicorn.run(
        app=settings.conf.app,
        host=settings.conf.host,
        port=settings.conf.port,
        workers=settings.conf.workers,
        reload=settings.conf.reload,
    )


if __name__ == "__main__":
    main()
