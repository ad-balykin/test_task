import asyncio
from logging import Logger

from .base import BaseRunner
from application.config import AppConfig
from application.domain.services.courses_service import CoursesService
from application.infrastructure.repositories.course import CourseRepository
from application.infrastructure.db_context import DBContextFactory


class CourseRunner(BaseRunner):
    def __init__(
            self,
            courses_service: CoursesService,
            course_repository: CourseRepository,
            logger: Logger,
            config: AppConfig,
            db_context_factory: DBContextFactory,
    ):
        self._courses_service = courses_service
        self._course_repository = course_repository
        self._db_context_factory = db_context_factory
        self._logger = logger

        self._iteration_delay = config.courses_runner_config.iteration_delay

    async def run(self) -> None:
        while True:
            await self.run_once()
            await asyncio.sleep(self._iteration_delay)

    async def run_once(self) -> None:
        async with self._db_context_factory.create_context() as db_context:
            tasks = await self._course_repository.get_all(db_context.connection)
            if tasks:
                self._logger.info(f"Found {len(tasks)} active course update tasks")
                await self._courses_service.fetch_courses(tasks, db_context=db_context)
                self._logger.info(f"Course update tasks processed successfully")
