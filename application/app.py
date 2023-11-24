import asyncio

import uvicorn
from fastapi import FastAPI
from aiohttp import TCPConnector
import logging

from application.container import CompositionContainer
from application.config import AppConfig
from application.api import router


def init_container() -> CompositionContainer:
    config = AppConfig()

    connector = TCPConnector()

    logger = logging.getLogger("root_logger")
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(config.log_level)

    container = CompositionContainer(
        config=config,
        http_connector=connector,
        logger=logger
    )
    container.make_dependencies()

    return container


def create_fastapi() -> FastAPI:
    container = init_container()

    fastapi_app = FastAPI(
        debug=container.config.debug,
        title="Currency API",
        docs_url="/api/docs" if container.config.debug else None,
    )
    fastapi_app.include_router(router, prefix="/api")
    fastapi_app.container = container

    @fastapi_app.on_event("shutdown")
    async def shutdown_db():
        await container.connection_pool.close()

    return fastapi_app


def create_runners() -> None:
    container = init_container()

    runners = [container.courses_runner]

    async def start_tasks():
        tasks = []
        for runner in runners:
            tasks.append(asyncio.create_task(runner.run()))
        await asyncio.wait(tasks)

    asyncio.get_event_loop().run_until_complete(start_tasks())


def run_api():
    uvicorn.run("application.app:create_fastapi", host="0.0.0.0", port=8000)
