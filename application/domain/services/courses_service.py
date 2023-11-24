import asyncio
from logging import Logger
from typing import Iterable, Callable

from application.domain.models.course import Course
from application.infrastructure.adapters.base import BaseExchangerAdapter
from application.infrastructure.repositories.course import CourseRepository
from application.infrastructure.db_context import DBContextFactory, DBContext


class CoursesService:
    def __init__(
            self,
            adapters_mapping: dict[str, BaseExchangerAdapter],
            course_repository: CourseRepository,
            logger: Logger,
            db_context_factory: DBContextFactory,
    ):
        self._adapters_mapping = adapters_mapping
        self._course_repository = course_repository
        self._db_context_factory = db_context_factory
        self._logger = logger

    async def get_courses(self) -> list[Course]:
        async with self._db_context_factory.create_context() as db_context:
            return await self._course_repository.get_all(connection=db_context.connection)

    async def fetch_courses(self, courses: Iterable[Course], db_context: DBContext) -> list[Course]:
        tasks = []

        for course in courses:
            adapter = self._adapters_mapping.get(course.exchanger)
            if adapter is None:
                raise Exception(f"No adapter for {course.exchanger} exchanger")

            tasks.append(adapter.fetch_rate(from_currency=course.from_currency, to_currency=course.to_currency))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        courses_resp = []
        for course, result in zip(courses, results):
            if isinstance(result, Exception):
                self._logger.error(f"Could not fetch course {course.id}. {result}")
                continue

            course.value = result
            await self._course_repository.update(course, connection=db_context.connection)

            courses_resp.append(course)

        return courses_resp
